import asyncio
from aiohttp import web
from models import db, create_init
from config import BIND, REFRESH_HOLDS_SLEEP, HOST, PORT
from handlers import setup as route_setup, refresh_users_hold


async def refresh_holds():
    while True:
        await refresh_users_hold()
        await asyncio.sleep(REFRESH_HOLDS_SLEEP)


async def main():
    await db.set_bind(BIND)
    await db.gino.create_all()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
task = loop.create_task(refresh_holds())
app = web.Application(loop=loop)
route_setup(app)
web.run_app(app, host=HOST, port=PORT)
