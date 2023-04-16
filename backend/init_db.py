from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import register_tortoise
from constants import DATABASE_PASSWORD, DATABASE_HOST, DATABASE_USERNAME, DATABASE_NAME

db_url = f'mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}?ssl=True'

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": ["db.models.video", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['db.models.video']}
    )


def init_db(app):
    register_tortoise(
        app,
        db_url=db_url,
        modules={'models': ['db.models.video']},
        generate_schemas=True,
        add_exception_handlers=True
    )


async def generate_schema():
    # Generate the schema
    await init()
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(generate_schema())
