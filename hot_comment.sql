/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : doubanf

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-07-20 18:36:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hot_comment
-- ----------------------------
DROP TABLE IF EXISTS `hot_comment`;
CREATE TABLE `hot_comment` (
  `comment_id` bigint(20) NOT NULL,
  `content` text NOT NULL,
  `totalcount` int(11) NOT NULL,
  `useful_count` int(11) NOT NULL,
  `useless_count` int(11) NOT NULL,
  `movie_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `hot_comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie_info` (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
