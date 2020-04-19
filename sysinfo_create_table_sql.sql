/*
 Navicat Premium Data Transfer

 Source Server         : servername
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : 127.0.0.1
 Source Schema         : servername

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 19/04/2020 13:40:34
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tablename
-- ----------------------------
DROP TABLE IF EXISTS `tablename`;
CREATE TABLE `tablename`  (
  `RowGuid` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '主键id',
  `tstamp` datetime(0) NULL DEFAULT NULL COMMENT '数据时间',
  `cpuPercent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'CPU使用率（%）',
  `memoryPercent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '内存使用率（%）',
  `memoryUsage` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '内存使用情况（M）',
  `totalBytesSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '发送总字节数（B|K|M|G|T|P|E|Z|Y）',
  `totalBytesReceived` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接收总字节数（B|K|M|G|T|P|E|Z|Y）',
  `totalPacketsSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '发送总数据包数',
  `totalPacketsReceived` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '接收总数据包数',
  `loTotalBytesSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo发送总字节数（B|K|M|G|T|P|E|Z|Y）',
  `loPerSecBytesSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo每秒发送字节数（（B|K|M|G|T|P|E|Z|Y）/s）',
  `loTotalBytesRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo接收总字节数（B|K|M|G|T|P|E|Z|Y）',
  `loPerSecBytesRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo每秒接收字节数（（B|K|M|G|T|P|E|Z|Y）/s）',
  `loTotalPktsSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo发送总数据包数',
  `loPerSecPktsSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo每秒发送数据包数',
  `loTotalPktsRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo接收总数据包数',
  `loPerSecPktsRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'lo每秒接收数据包数',
  `eth0TotalBytesSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0发送总字节数（B|K|M|G|T|P|E|Z|Y）',
  `eth0PerSecBytesSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0每秒发送字节数（（B|K|M|G|T|P|E|Z|Y）/s）',
  `eth0TotalBytesRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0接收总字节数（B|K|M|G|T|P|E|Z|Y）',
  `eth0PerSecBytesRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0每秒接收字节数（（B|K|M|G|T|P|E|Z|Y）/s）',
  `eth0TotalPktsSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0发送总数据包数',
  `eth0PerSecPktsSent` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0每秒发送数据包数',
  `eth0TotalPktsRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0接收总数据包数',
  `eth0PerSecPktsRecv` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'eth0每秒接收数据包数',
  `isDeleted` bit(1) NOT NULL COMMENT '假删字段（true，false）',
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '新增人',
  `createDate` datetime(0) NOT NULL COMMENT '新增日期',
  `modifier` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '修改人',
  `modifyDate` datetime(0) NOT NULL COMMENT '修改日期',
  PRIMARY KEY (`RowGuid`) USING BTREE,
  INDEX `RowGuid`(`RowGuid`) USING BTREE,
  INDEX `tstamp`(`tstamp`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
