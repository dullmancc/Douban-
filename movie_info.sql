/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : doubanf

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-07-20 18:36:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for movie_info
-- ----------------------------
DROP TABLE IF EXISTS `movie_info`;
CREATE TABLE `movie_info` (
  `movie_id` varchar(20) NOT NULL,
  `movie_title` varchar(20) NOT NULL,
  `actors` text NOT NULL,
  `regions` varchar(20) DEFAULT NULL,
  `release_date` varchar(50) DEFAULT NULL,
  `synopsis` text,
  `cover_url` varchar(100) DEFAULT NULL,
  `score` float NOT NULL,
  `rating` int(11) NOT NULL,
  `vote_count` bigint(20) NOT NULL,
  `url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
