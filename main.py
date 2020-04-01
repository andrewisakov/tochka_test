import asyncio
from models import db, User, create_init
from config import BIND


async def main():
    await db.set_bind(BIND)
    await db.gino.create_all()
    await create_init()
    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())
