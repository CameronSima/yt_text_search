from tortoise import Tortoise, run_async
from constants import DATABASE_PASSWORD, DATABASE_HOST, DATABASE_USERNAME, DATABASE_NAME


def connection_str(user, password, host, database):
    return f'mysql://{user}:{password}@{host}/{database}?ssl=True'
    # return f'mysql://dfm29o9xvqvwskcxo5kv:************@aws.connect.psdb.cloud/cam_mysql?sslaccept=strict'


async def init():
    db_url = connection_str(DATABASE_USERNAME, DATABASE_PASSWORD,
                            DATABASE_HOST, DATABASE_NAME)
    print(db_url)
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['db.models.video']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()

if __name__ == '__main__':
    run_async(init())