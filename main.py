import asyncio
from aiohttp import web
from models import db, create_init
from config import BIND
from handlers import setup as route_setup


async def main():
    await db.set_bind(BIND)
    await db.gino.create_all()
    await create_init()
    # await db.pop_bind().close()

asyncio.get_event_loop().run_until_complete(main())
app = web.Application()
route_setup(app)
web.run_app(app, host='0.0.0.0', port=8080)
