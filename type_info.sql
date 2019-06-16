/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50722
Source Host           : localhost:3306
Source Database       : doubanf

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-07-20 18:36:48
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for type_info
-- ----------------------------
DROP TABLE IF EXISTS `type_info`;
CREATE TABLE `type_info` (
  `type_id` int(11) NOT NULL,
  `type_name` varchar(10) NOT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
