/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : doubanf

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-07-20 18:36:41
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for movie_type
-- ----------------------------
DROP TABLE IF EXISTS `movie_type`;
CREATE TABLE `movie_type` (
  `type_id` int(11) NOT NULL,
  `movie_id` varchar(20) NOT NULL,
  `rank` int(11) NOT NULL,
  PRIMARY KEY (`type_id`,`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
