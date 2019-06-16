/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : doubanf

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-07-20 18:36:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hot_topic
-- ----------------------------
DROP TABLE IF EXISTS `hot_topic`;
CREATE TABLE `hot_topic` (
  `topic_id` int(11) NOT NULL,
  `topic_name` varchar(100) NOT NULL,
  `label` varchar(20) NOT NULL,
  `card_subtitle` varchar(50) NOT NULL,
  `participant_count` int(11) NOT NULL,
  `post_count` int(11) NOT NULL,
  `subscription_count` int(11) NOT NULL,
  `url` varchar(100) NOT NULL,
  `movie_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`topic_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `hot_topic_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie_info` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
