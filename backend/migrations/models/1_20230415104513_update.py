from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `video` MODIFY COLUMN `title` VARCHAR(999) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `video` MODIFY COLUMN `title` VARCHAR(255) NOT NULL;"""
