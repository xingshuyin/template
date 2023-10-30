from models_tortoise import *
import asyncio
from tortoise import Tortoise


async def init_user():
    for i in [
        {'username': 'admin', 'password': 'admin'},
    ]:
        u, is_create = await user.update_or_create(defaults=i, **i)
        await u.set_password(i['passwod'])
        await user_info.update_or_create(defaults={'user': u}, user=u)


async def init():
    await Tortoise.init(
        db_url='sqlite://tortoise.sql',
        modules={'models': ['models_tortoise']}
    )
    await Tortoise.generate_schemas()

    u = await user_info.get(id=1)
    await u.follow_user.add(await user_info.get(id=2))

    # i = await user_info.all().filter(id=3).first()
    # follw = await user_info.all().filter(id=5).first()
    # await i.follow_user.add(follw)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.close()
