CREATE TABLE `groups` (
      `group_id`    BIGINT UNSIGNED     NOT NULL AUTO_INCREMENT,
      `group_name`  varchar(100)        NOT NULL,
      `group_owner` BIGINT              NOT NULL,
      `is_deleted`  BOOLEAN             NOT NULL,
      `created_at`  DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `updated_at`  DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`group_id`,`group_name`),
      INDEX `index_group_name` (`group_name`),
      INDEX `index_created_at` (`created_at`),
      INDEX `index_updated_at` (`updated_at`)
) ENGINE=InnoDB

CREATE TABLE `users` (
      `user_id`     BIGINT UNSIGNED     NOT NULL AUTO_INCREMENT ,
      `user_name`   varchar(100)        NOT NULL,
      `password`    varchar(100)        NOT NULL,
      `create_at`   DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `updated_at`  DATETIME            NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`user_id`,`user_name`),
      INDEX `index_group_name` (`group_name`),
      INDEX `index_created_at` (`created_at`),
      INDEX `index_updated_at` (`updated_at`)
) ENGINE=InnoDB


