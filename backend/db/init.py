from tortoise import Tortoise, run_async


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.video']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(init())
