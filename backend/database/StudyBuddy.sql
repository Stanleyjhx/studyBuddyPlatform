/*
 Navicat Premium Data Transfer

 Source Server         : studybuddy
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : StudyBuddy

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 28/02/2023 19:12:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for courses
-- ----------------------------
DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of courses
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for enrolled
-- ----------------------------
DROP TABLE IF EXISTS `enrolled`;
CREATE TABLE `enrolled` (
  `user_id` bigint NOT NULL,
  `course_id` int NOT NULL,
  `current` tinyint NOT NULL DEFAULT '1' COMMENT '`0` for past. `1` for current.',
  PRIMARY KEY (`user_id`,`course_id`),
  KEY `course_id_fk1` (`course_id`),
  CONSTRAINT `course_id_fk1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `user_id_fk3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of enrolled
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for event_attendees
-- ----------------------------
DROP TABLE IF EXISTS `event_attendees`;
CREATE TABLE `event_attendees` (
  `event_id` bigint NOT NULL,
  `attendee_id` bigint NOT NULL,
  `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_deleted` boolean NOT NULL
  PRIMARY KEY (`event_id`,`attendee_id`),
  KEY `attendee_id_fk1` (`attendee_id`),
  CONSTRAINT `attendee_id_fk1` FOREIGN KEY (`attendee_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `event_id_fk1` FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of event_attendees
-- ----------------------------
BEGIN;
INSERT INTO `event_attendees` VALUES (1, 1, '2023-02-28 19:10:40');
INSERT INTO `event_attendees` VALUES (1, 2, '2023-02-28 19:10:40');
INSERT INTO `event_attendees` VALUES (1, 3, '2023-02-28 19:10:40');
INSERT INTO `event_attendees` VALUES (1, 4, '2023-02-28 19:10:40');
COMMIT;

-- ----------------------------
-- Table structure for events
-- ----------------------------
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `event_id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `event_holder` bigint NOT NULL,
  `event_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `event_description` varchar(255) DEFAULT NULL,
  `location` varchar(255) NOT NULL,
  `capacity` int NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `is_deleted` boolean NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_id`),
  KEY `event_holder_fk1` (`event_holder`),
  KEY `group_fk3` (`group_id`,`event_holder`),
  CONSTRAINT `group_fk3` FOREIGN KEY (`group_id`, `event_holder`) REFERENCES `group_members` (`group_id`, `user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of events
-- ----------------------------
BEGIN;
INSERT INTO `events` VALUES (1, 1, 1, 'weekly meeting 1', 'discuss db design', 'zoom', '2023-03-04 15:00:00', '2023-03-04 16:00:00', '2023-02-28 17:05:03', '2023-02-28 17:27:31');
COMMIT;

-- ----------------------------
-- Table structure for group_members
-- ----------------------------
DROP TABLE IF EXISTS `group_members`;
CREATE TABLE `group_members` (
  `group_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`group_id`,`user_id`),
  KEY `index_group_id` (`group_id`),
  KEY `index_user_id` (`user_id`),
  CONSTRAINT `group_id_fk2` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id_fk2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of group_members
-- ----------------------------
BEGIN;
INSERT INTO `group_members` VALUES (1, 1, '2023-02-28 17:02:49');
INSERT INTO `group_members` VALUES (1, 2, '2023-02-28 17:03:00');
INSERT INTO `group_members` VALUES (1, 3, '2023-02-28 17:03:04');
INSERT INTO `group_members` VALUES (1, 4, '2023-02-28 17:00:40');
INSERT INTO `group_members` VALUES (2, 7, '2023-02-28 17:25:48');
COMMIT;

-- ----------------------------
-- Table structure for groups
-- ----------------------------
DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `group_owner` bigint NOT NULL,
  `group_description` varchar(255) DEFAULT NULL,
  `is_deleted` boolean NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`group_id`),
  KEY `index_group_name` (`group_name`),
  KEY `fk_user_id` (`group_owner`),
  KEY `group_id` (`group_id`,`group_owner`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`group_owner`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of groups
-- ----------------------------
BEGIN;
INSERT INTO `groups` VALUES (1, 'studyBuddy', 4, 'Study Buddy dev group', '2023-02-28 16:58:46', '2023-02-28 16:58:46');
INSERT INTO `groups` VALUES (2, 'group2', 7, 'Another group', '2023-02-28 17:17:55', '2023-02-28 17:17:55');
COMMIT;

-- ----------------------------
-- Table structure for membership_requests
-- ----------------------------
DROP TABLE IF EXISTS `membership_requests`;
CREATE TABLE `membership_requests` (
  `membership_request_id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `group_owner_id` bigint NOT NULL,
  `requester_id` bigint NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '''-1'' for declined. `0` for pending. `1` for accepted.',
  `apply_reason` string NOT NULL DEFAULT '',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`membership_request_id`) USING BTREE,
  UNIQUE Ke
  KEY `indexgroup_owner_id` (`group_owner_id`),
  KEY `index_requester_id` (`requester_id`),
  KEY `index_group_id_fk1` (`group_id`),
  KEY `index_status` (`status`),
  KEY `group_fk1` (`group_id`,`group_owner_id`),
  CONSTRAINT `group_fk1` FOREIGN KEY (`group_id`, `group_owner_id`) REFERENCES `groups` (`group_id`, `group_owner`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `requester_id` FOREIGN KEY (`requester_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of membership_requests
-- ----------------------------
BEGIN;
INSERT INTO `membership_requests` VALUES (1, 1, 4, 5, 0, '', '2023-02-28 17:09:24', '2023-02-28 17:12:37');
INSERT INTO `membership_requests` VALUES (2, 1, 4, 6, 0, '', '2023-02-28 17:16:31', '2023-02-28 17:16:31');
INSERT INTO `membership_requests` VALUES (4, 2, 7, 5, 0, '', '2023-02-28 17:18:28', '2023-02-28 17:18:28');
INSERT INTO `membership_requests` VALUES (5, 2, 7, 2, 0, '', '2023-02-28 17:19:05', '2023-02-28 17:19:05');
INSERT INTO `membership_requests` VALUES (6, 1, 4, 7, 0, '', '2023-02-28 17:19:05', '2023-02-28 17:19:05');
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `student_id` varchar(100) NOT NULL,
  `major` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT ' `0` for pending. `1` for accepted.',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  KEY `index_user_name` (`user_name`) USING BTREE,
  KEY `index_created_at` (`created_at`),
  KEY `index_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (1, 'jia1', 'password1', 'Futao', 'Jia', 'A1234A', 'DSML', '', '2023-02-28 16:52:30', '2023-02-28 16:55:33');
INSERT INTO `users` VALUES (2, 'gao2', 'password2', 'Ya', 'Gao', 'A1234B', 'DSML', '', '2023-02-28 16:53:18', '2023-02-28 16:55:30');
INSERT INTO `users` VALUES (3, 'jiang3', 'password3', 'Hengxian', 'Jiang', 'A1234C', 'DSML', '', '2023-02-28 16:54:08', '2023-02-28 16:55:36');
INSERT INTO `users` VALUES (4, 'ye4', 'password4', 'Yujia', 'Ye', 'A1234D', 'DSML', '', '2023-02-28 16:55:10', '2023-02-28 16:55:38');
INSERT INTO `users` VALUES (5, 'wong5', 'password5', 'Alice', 'Wong', 'A1234E', 'STAT', '', '2023-02-28 17:06:33', '2023-02-28 17:07:19');
INSERT INTO `users` VALUES (6, 'lee6', 'password6', 'Sin', 'Lee', 'A1234F', 'Mfin', '', '2023-02-28 17:07:12', '2023-02-28 17:07:21');
INSERT INTO `users` VALUES (7, 'zhou7', 'password7', 'Zhou', 'Zhou', 'A1234G', 'DSML', '', '2023-02-28 17:17:23', '2023-02-28 17:17:23');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
