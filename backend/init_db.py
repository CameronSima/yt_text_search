from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from constants import DATABASE_PASSWORD, DATABASE_HOST, DATABASE_USERNAME, DATABASE_NAME


async def init():
    db_url = f'mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?ssl=True'
    print(db_url)
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['db.models.video']}
    )


def init_db(app):
    db_url = f'mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?ssl=True'
    register_tortoise(
        app,
        db_url=db_url,
        modules={'models': ['db.models.video']},
        generate_schemas=True,
        add_exception_handlers=True
    )


async def generate_schema():
    # Generate the schema
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(init())
