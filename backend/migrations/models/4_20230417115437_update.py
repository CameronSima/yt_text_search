from tortoise import BaseDBAsyncClient


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `video` DROP INDEX `idx_video_yt_chan_2c9bc1`;
        ALTER TABLE `video` DROP INDEX `idx_video_yt_vide_be41cd`;
        ALTER TABLE `video` DROP INDEX `idx_video_title_540bf8`;
        ALTER TABLE `video` MODIFY COLUMN `title` VARCHAR(999) NOT NULL;
        """


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `video` MODIFY COLUMN `title` VARCHAR(500) NOT NULL;
        ALTER TABLE `video` ADD INDEX `idx_video_title_540bf8` (`title`);
        ALTER TABLE `video` ADD INDEX `idx_video_yt_vide_be41cd` (`yt_video_id`);
        ALTER TABLE `video` ADD INDEX `idx_video_yt_chan_2c9bc1` (`yt_channel_id`);"""
