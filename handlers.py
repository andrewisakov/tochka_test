import uuid
import ujson
import decimal
import datetime
from aiohttp.web import json_response
from models import User


async def ping(request):
    return json_response(data={'message': 'pong'})


async def get_user(user_id):
    if user_id:
        user_id = uuid.UUID(user_id)
        user = await User.select('id', 'name', 'account', 'hold', 'status') \
            .where(User.id == user_id).with_for_update().gino.one_or_none()
    return user


async def add(request):
    data = await request.json()
    user_id = data.get('id')
    user = await get_user(user_id)
    add_summ = data.get('sum', 0)
    response = {}
    if user and user.status:
        new_account = user.account+decimal.Decimal(add_summ)
        result = await User.update.values(account=new_account).where(User.id == user_id).gino.status()
        result = result[0].split()
        response = {
            'result': result,
            'description': 'Баланс {}пополнен.'.format('' if result[0] == 'UPDATE' and int(result[1]) else 'не '),
        }
        code = 200 if int(result[1]) else 401
    elif user:
        response = {
            'result': 'NOT ALLOWED',
            'description': 'Cant modify because user.status is closed.',
        }
        code = 400
    else:
        response = {
            'addition': {'id': user_id},
            'result': 'NOT FOUND',
        }
        code = 404
    response.update(status=code)
    if code != 404:
        response.update(
            addition={
                'id': str(user.id),
                'name': user.name,
                'status': ('closed', 'open')[user.status],
                'account': user.account,
                'hold': user.hold,
            },
        )
    response = ujson.dumps(response)
    return json_response(body=response, status=code)


async def substract(request):
    data = await request.json()
    user_id = data.get('id')

    sub_summ = data.get('sum', 0)
    user = await get_user(user_id)

    if user and user.status:
        sub_summ = decimal.Decimal(sub_summ)
        new_hold = user.hold + sub_summ
        holding_allow = user.account >= new_hold
        if holding_allow:
            
            result = await User.update.values(hold=new_hold).where(User.id == user_id).gino.status()
            result = result[0].split()
            response = {
                'result': result,
                'description': 'Списание {}зарезервировано.'.format(
                    '' if result[0] == 'UPDATE' and int(result[1]) else 'не '
                ),
            }
            code = 200 if int(result[1]) else 415
            user = await get_user(user_id)
        else:
            response = {
                'result': 'Недостаточно средств!',
                'description': 'Списание не выполнено.',
            }
            code = 415

    elif user:
        response = {
            'result': 'NOT ALLOWED',
            'description': 'Списание {}выполнено.'.format('' if result[0] == 'UPDATE' and int(result[1]) else 'не '),
        }
        code = 405
    else:
        response = {
            'addition': {'id': user_id},
            'result': 'NOT FOUND',
        }
        code = 404

    response.update(status=code)
    if code != 404:
        response.update(
            addition={
                'id': str(user.id),
                'name': user.name,
                'status': ('closed', 'open')[user.status],
                'account': user.account,
                'hold': user.hold,
            },
        )
    response = ujson.dumps(response)
    return json_response(body=response, status=code)


async def status(request):
    user_id = request.match_info.get('id')

    if user_id:
        # user_id = uuid.UUID(user_id)
        user = await get_user(user_id)
        if user:
            code = 200
            response = {
                'addition': {
                    'status': ('closed', 'open')[user.status],
                    'account': user.account,
                    'name': user.name,
                    'hold': user.hold,
                    'id': str(user.id),
                },
                'result': 'success',
                'status': code,
            }
        else:
            code = 404
            response = {
                'addition': {
                    'id': user_id,
                },
                'result': 'NOT FOUND',
                'status': code,
            }
    else:
        response = {'id': user_id, 'status': 401, 'result': 'error'}
        code = 401
    response = ujson.dumps(response)
    return json_response(body=response, status=code)


async def refresh_users_hold():
    users = await User.select('id', 'hold', 'account', 'status')\
        .where(User.status)\
        .where(User.hold > 0)\
        .where(User.account >= User.hold)\
        .with_for_update().gino.all()
    results = []
    for user in users:
        new_account = user.account - user.hold
        result = await User.update.values(account=new_account, hold=0).where(User.id == user.id).gino.status()
        results.append(result)


def setup(app):
    app.router.add_get('/api/status/{id}', status)
    app.router.add_post('/api/add', add)
    app.router.add_post('/api/substract', substract)
    app.router.add_post('/api/ping', ping)
