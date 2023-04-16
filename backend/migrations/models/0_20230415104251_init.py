from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `video` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `yt_video_id` VARCHAR(255) NOT NULL,
    `yt_channel_id` VARCHAR(255) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `url` VARCHAR(255) NOT NULL,
    `published_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `text_segments` JSON NOT NULL,
    KEY `idx_video_yt_vide_be41cd` (`yt_video_id`),
    KEY `idx_video_yt_chan_2c9bc1` (`yt_channel_id`),
    KEY `idx_video_title_540bf8` (`title`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
