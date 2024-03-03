-- MySQL dump 10.13  Distrib 8.0.36, for Linux (aarch64)
--
-- Host: localhost    Database: ecomddb
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB-1:11.2.2+maria~ubu2204

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `ecomddb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ecomddb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `ecomddb`;

--
-- Table structure for table `conso_maison`
--

DROP TABLE IF EXISTS `conso_maison`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conso_maison` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_MAISON` int(11) DEFAULT NULL,
  `CONSO` int(11) DEFAULT 0,
  `PROD` int(11) DEFAULT 0,
  `HORODATAGE` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_MAISON` (`ID_MAISON`),
  CONSTRAINT `FK_conso_maison_maison` FOREIGN KEY (`ID_MAISON`) REFERENCES `maison` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conso_maison`
--

LOCK TABLES `conso_maison` WRITE;
/*!40000 ALTER TABLE `conso_maison` DISABLE KEYS */;
INSERT INTO `conso_maison` VALUES (1,1,1709,1400,'2023-12-07 09:00:00'),(2,2,2000,1452,'2023-12-07 10:00:00'),(3,1,1200,1478,'2023-12-07 11:00:00'),(4,2,600,1524,'2023-12-07 12:00:00'),(5,1,1000,1587,'2023-12-07 13:00:00'),(6,2,1000,1200,'2023-12-07 14:00:00'),(7,1,600,806,'2023-12-07 15:00:00'),(8,2,400,754,'2023-12-07 16:00:00'),(9,1,1500,625,'2023-12-07 17:00:00'),(10,2,0,0,'2023-12-07 09:00:00');
/*!40000 ALTER TABLE `conso_maison` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maison`
--

DROP TABLE IF EXISTS `maison`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maison` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ADRESSE` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maison`
--

LOCK TABLES `maison` WRITE;
/*!40000 ALTER TABLE `maison` DISABLE KEYS */;
INSERT INTO `maison` VALUES (1,'8A Rue Jean Pierson'),(2,'Rue Saint Jean XXVI');
/*!40000 ALTER TABLE `maison` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mesures`
--

DROP TABLE IF EXISTS `mesures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mesures` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_OBJETS` int(11) DEFAULT NULL,
  `HORODATAGE` timestamp NULL DEFAULT NULL,
  `VALEUR` varchar(240) DEFAULT NULL,
  `UNITE` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_OBJETS` (`ID_OBJETS`),
  CONSTRAINT `FK_mesures_objets` FOREIGN KEY (`ID_OBJETS`) REFERENCES `objets` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=475 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mesures`
--

LOCK TABLES `mesures` WRITE;
/*!40000 ALTER TABLE `mesures` DISABLE KEYS */;
INSERT INTO `mesures` VALUES (1,1,'2023-12-01 14:11:06','140',NULL),(6,1,'2023-12-04 10:03:24','42','VA'),(7,1,'2023-12-04 10:38:20','10','W'),(8,1,'2023-12-04 10:39:48','4100','KW'),(9,2,'2023-12-05 09:45:59','170','W'),(10,2,'2023-12-05 09:52:19','100','W'),(11,3,'2023-12-05 09:58:37','14','W'),(12,3,'2023-12-05 09:59:37','13','W'),(13,3,'2023-12-05 09:59:37','235','V'),(14,3,'2023-12-05 09:59:37','0','A'),(16,3,'2023-12-05 10:01:49','235','V'),(17,3,'2023-12-05 10:01:49','0','A'),(18,3,'2023-12-05 10:02:38','235','V'),(19,3,'2023-12-05 10:02:40','0','A'),(20,3,'2023-12-05 10:03:15','235','V'),(21,3,'2023-12-05 10:03:15','0','A'),(22,3,'2023-12-05 10:03:33','18','W'),(23,3,'2023-12-05 10:03:34','235','V'),(24,3,'2023-12-05 10:03:34','0','A'),(25,5,'2023-12-06 13:31:09','0','W'),(26,4,'2023-12-06 13:32:40','25','W'),(27,4,'2023-12-06 13:32:40','233','V'),(28,4,'2023-12-06 13:32:40','0','A'),(29,5,'2023-12-06 13:32:40','0','W'),(30,5,'2023-12-06 13:32:40','233','V'),(31,5,'2023-12-06 13:32:40','0','A'),(32,4,'2023-12-06 13:37:12','22','W'),(33,4,'2023-12-06 13:37:12','234','V'),(34,4,'2023-12-06 13:37:12','0','A'),(35,5,'2023-12-06 13:37:12','0','W'),(36,5,'2023-12-06 13:37:12','233','V'),(37,5,'2023-12-06 13:37:12','0','A'),(38,4,'2023-12-06 13:39:51','0','W'),(39,4,'2023-12-06 13:39:52','233','V'),(40,4,'2023-12-06 13:39:52','0','A'),(41,5,'2023-12-06 13:39:54','0','W'),(42,5,'2023-12-06 13:39:54','233','V'),(43,5,'2023-12-06 13:39:54','0','A'),(44,3,'2023-12-06 13:40:01','30','W'),(45,3,'2023-12-06 13:40:01','233','V'),(46,3,'2023-12-06 13:40:01','0','A'),(47,3,'2023-12-07 10:09:37','28','W'),(48,3,'2023-12-07 10:09:37','233','V'),(49,3,'2023-12-07 10:09:37','0','A'),(50,3,'2023-12-07 10:10:36','28','W'),(51,3,'2023-12-07 10:10:36','233','V'),(52,3,'2023-12-07 10:10:36','0','A'),(53,3,'2023-12-07 10:14:45','26','W'),(54,3,'2023-12-07 10:14:45','233','V'),(55,3,'2023-12-07 10:14:45','0','A'),(56,4,'2023-12-07 12:40:49','0','W'),(57,4,'2023-12-07 12:40:49','237','V'),(58,4,'2023-12-07 12:40:49','0','A'),(59,5,'2023-12-07 12:40:49','0','W'),(60,5,'2023-12-07 12:40:49','236','V'),(61,5,'2023-12-07 12:40:49','0','A'),(62,4,'2023-12-07 12:41:33','0','W'),(63,4,'2023-12-07 12:41:34','237','V'),(64,4,'2023-12-07 12:41:34','0','A'),(65,5,'2023-12-07 12:41:34','0','W'),(66,5,'2023-12-07 12:41:34','237','V'),(67,5,'2023-12-07 12:41:35','0','A'),(68,3,'2023-12-07 12:41:43','0','W'),(69,3,'2023-12-07 12:41:43','235','V'),(70,3,'2023-12-07 12:41:43','0','A'),(71,4,'2023-12-07 12:43:45','0','W'),(72,4,'2023-12-07 12:43:45','237','V'),(73,4,'2023-12-07 12:43:45','0','A'),(74,5,'2023-12-07 12:43:45','0','W'),(75,5,'2023-12-07 12:43:45','237','V'),(76,5,'2023-12-07 12:43:45','0','A'),(77,4,'2023-12-07 12:47:16','0','W'),(78,4,'2023-12-07 12:47:16','237','V'),(79,4,'2023-12-07 12:47:16','0','A'),(80,5,'2023-12-07 12:47:16','0','W'),(81,5,'2023-12-07 12:47:16','237','V'),(82,5,'2023-12-07 12:47:16','0','A'),(83,4,'2023-12-07 12:50:55','0','W'),(84,4,'2023-12-07 12:50:55','237','V'),(85,4,'2023-12-07 12:50:55','0','A'),(86,5,'2023-12-07 12:50:55','0','W'),(87,5,'2023-12-07 12:50:55','236','V'),(88,5,'2023-12-07 12:50:55','0','A'),(89,3,'2023-12-07 12:51:00','0','W'),(90,3,'2023-12-07 12:51:01','235','V'),(91,3,'2023-12-07 12:51:01','0','A'),(92,4,'2023-12-07 12:53:01','0','W'),(93,4,'2023-12-07 12:53:01','236','V'),(94,4,'2023-12-07 12:53:01','0','A'),(95,5,'2023-12-07 12:53:01','0','W'),(96,5,'2023-12-07 12:53:01','236','V'),(97,5,'2023-12-07 12:53:01','0','A'),(98,4,'2023-12-07 12:54:27','0','W'),(99,4,'2023-12-07 12:54:27','236','V'),(100,4,'2023-12-07 12:54:27','0','A'),(101,5,'2023-12-07 12:54:27','0','W'),(102,5,'2023-12-07 12:54:27','236','V'),(103,5,'2023-12-07 12:54:27','0','A'),(104,4,'2023-12-07 12:56:59','0','W'),(105,4,'2023-12-07 12:56:59','237','V'),(106,4,'2023-12-07 12:56:59','0','A'),(107,5,'2023-12-07 12:56:59','0','W'),(108,5,'2023-12-07 12:56:59','236','V'),(109,5,'2023-12-07 12:56:59','0','A'),(110,3,'2023-12-07 12:57:04','0','W'),(111,3,'2023-12-07 12:57:04','235','V'),(112,3,'2023-12-07 12:57:04','0','A'),(113,4,'2023-12-07 13:00:08','0','W'),(114,4,'2023-12-07 13:00:08','236','V'),(115,4,'2023-12-07 13:00:08','0','A'),(116,5,'2023-12-07 13:00:08','0','W'),(117,5,'2023-12-07 13:00:08','236','V'),(118,5,'2023-12-07 13:00:08','0','A'),(119,3,'2023-12-07 13:00:14','0','W'),(120,3,'2023-12-07 13:00:14','235','V'),(121,3,'2023-12-07 13:00:14','0','A'),(122,2,'2023-12-07 13:14:21','155955590','W\''),(123,4,'2023-12-07 13:15:07','0','W'),(124,4,'2023-12-07 13:15:07','237','V'),(125,4,'2023-12-07 13:15:07','0','A'),(126,5,'2023-12-07 13:15:07','0','W'),(127,5,'2023-12-07 13:15:07','237','V'),(128,5,'2023-12-07 13:15:07','0','A'),(129,3,'2023-12-07 13:15:13','0','W'),(130,3,'2023-12-07 13:15:13','235','V'),(131,3,'2023-12-07 13:15:13','0','A'),(132,4,'2023-12-07 13:30:07','0','W'),(133,4,'2023-12-07 13:30:07','237','V'),(134,4,'2023-12-07 13:30:07','0','A'),(135,5,'2023-12-07 13:30:08','0','W'),(136,5,'2023-12-07 13:30:08','237','V'),(137,5,'2023-12-07 13:30:08','0','A'),(138,3,'2023-12-07 13:30:13','30','W'),(139,3,'2023-12-07 13:30:13','237','V'),(140,3,'2023-12-07 13:30:13','0','A'),(141,4,'2023-12-07 13:45:09','0','W'),(142,4,'2023-12-07 13:45:09','237','V'),(143,4,'2023-12-07 13:45:09','0','A'),(144,5,'2023-12-07 13:45:09','0','W'),(145,5,'2023-12-07 13:45:09','237','V'),(146,5,'2023-12-07 13:45:09','0','A'),(147,3,'2023-12-07 13:45:16','37','W'),(148,3,'2023-12-07 13:45:16','235','V'),(149,3,'2023-12-07 13:45:16','0','A'),(150,4,'2023-12-07 14:00:07','0','W'),(151,4,'2023-12-07 14:00:07','238','V'),(152,4,'2023-12-07 14:00:07','0','A'),(153,5,'2023-12-07 14:00:07','0','W'),(154,5,'2023-12-07 14:00:07','238','V'),(155,5,'2023-12-07 14:00:07','0','A'),(156,3,'2023-12-07 14:00:13','35','W'),(157,3,'2023-12-07 14:00:13','237','V'),(158,3,'2023-12-07 14:00:13','0','A'),(159,4,'2023-12-07 14:15:07','0','W'),(160,4,'2023-12-07 14:15:07','238','V'),(161,4,'2023-12-07 14:15:07','0','A'),(162,5,'2023-12-07 14:15:07','0','W'),(163,5,'2023-12-07 14:15:07','238','V'),(164,5,'2023-12-07 14:15:07','0','A'),(165,3,'2023-12-07 14:15:12','31','W'),(166,3,'2023-12-07 14:15:12','237','V'),(167,3,'2023-12-07 14:15:12','0','A'),(168,4,'2023-12-07 14:30:08','0','W'),(169,4,'2023-12-07 14:30:08','238','V'),(170,4,'2023-12-07 14:30:08','0','A'),(171,5,'2023-12-07 14:30:08','0','W'),(172,5,'2023-12-07 14:30:08','238','V'),(173,5,'2023-12-07 14:30:08','0','A'),(174,3,'2023-12-07 14:30:13','33','W'),(175,3,'2023-12-07 14:30:13','237','V'),(176,3,'2023-12-07 14:30:13','0','A'),(177,4,'2023-12-07 14:40:04','0','W'),(178,4,'2023-12-07 14:40:04','237','V'),(179,4,'2023-12-07 14:40:04','0','A'),(180,5,'2023-12-07 14:40:04','0','W'),(181,5,'2023-12-07 14:40:04','237','V'),(182,5,'2023-12-07 14:40:04','0','A'),(183,3,'2023-12-07 14:40:10','33','W'),(184,3,'2023-12-07 14:40:10','235','V'),(185,3,'2023-12-07 14:40:10','0','A'),(186,4,'2023-12-07 14:40:44','0','W'),(187,4,'2023-12-07 14:40:44','237','V'),(188,4,'2023-12-07 14:40:44','0','A'),(189,5,'2023-12-07 14:40:45','0','W'),(190,5,'2023-12-07 14:40:45','237','V'),(191,5,'2023-12-07 14:40:45','0','A'),(192,3,'2023-12-07 14:40:50','32','W'),(193,3,'2023-12-07 14:40:50','235','V'),(194,3,'2023-12-07 14:40:50','0','A'),(195,4,'2023-12-07 14:41:32','0','W'),(196,4,'2023-12-07 14:41:32','237','V'),(197,4,'2023-12-07 14:41:32','0','A'),(198,5,'2023-12-07 14:41:32','0','W'),(199,5,'2023-12-07 14:41:34','237','V'),(200,5,'2023-12-07 14:41:34','0','A'),(201,4,'2023-12-07 14:44:46','0','W'),(202,4,'2023-12-07 14:44:46','237','V'),(203,4,'2023-12-07 14:44:46','0','A'),(204,5,'2023-12-07 14:44:47','0','W'),(205,5,'2023-12-07 14:44:47','236','V'),(206,5,'2023-12-07 14:44:47','0','A'),(207,4,'2023-12-07 14:45:21','0','W'),(208,4,'2023-12-07 14:45:21','237','V'),(209,4,'2023-12-07 14:45:21','0','A'),(210,5,'2023-12-07 14:45:21','0','W'),(211,5,'2023-12-07 14:45:22','237','V'),(212,5,'2023-12-07 14:45:22','0','A'),(213,4,'2023-12-07 14:45:37','0','W'),(214,4,'2023-12-07 14:45:37','237','V'),(215,4,'2023-12-07 14:45:37','0','A'),(216,5,'2023-12-07 14:45:38','0','W'),(217,5,'2023-12-07 14:45:38','237','V'),(218,5,'2023-12-07 14:45:38','0','A'),(219,4,'2023-12-07 14:46:00','0','W'),(220,4,'2023-12-07 14:46:00','237','V'),(221,4,'2023-12-07 14:46:00','0','A'),(222,5,'2023-12-07 14:46:00','0','W'),(223,5,'2023-12-07 14:46:00','237','V'),(224,5,'2023-12-07 14:46:00','0','A'),(225,4,'2023-12-07 14:46:14','0','W'),(226,4,'2023-12-07 14:46:14','237','V'),(227,4,'2023-12-07 14:46:14','0','A'),(228,5,'2023-12-07 14:46:14','0','W'),(229,5,'2023-12-07 14:46:14','237','V'),(230,5,'2023-12-07 14:46:14','0','A'),(231,7,'2023-12-07 14:46:14','82','W\''),(232,4,'2023-12-07 14:52:51','0','W'),(233,4,'2023-12-07 14:52:51','237','V'),(234,4,'2023-12-07 14:52:51','0','A'),(235,5,'2023-12-07 14:52:51','0','W'),(236,5,'2023-12-07 14:52:51','237','V'),(237,5,'2023-12-07 14:52:51','0','A'),(238,7,'2023-12-07 14:52:51','95','W\''),(239,4,'2023-12-07 14:54:51','0','W'),(240,4,'2023-12-07 14:54:51','237','V'),(241,4,'2023-12-07 14:54:51','0','A'),(242,5,'2023-12-07 14:54:52','0','W'),(243,5,'2023-12-07 14:54:52','237','V'),(244,5,'2023-12-07 14:54:52','0','A'),(245,7,'2023-12-07 14:54:53','48','W\''),(246,4,'2023-12-07 15:00:03','0','W'),(247,4,'2023-12-07 15:00:03','237','V'),(248,4,'2023-12-07 15:00:03','0','A'),(249,5,'2023-12-07 15:00:03','0','W'),(250,5,'2023-12-07 15:00:03','237','V'),(251,5,'2023-12-07 15:00:03','0','A'),(252,4,'2023-12-07 15:00:32','0','W'),(253,4,'2023-12-07 15:00:32','238','V'),(254,4,'2023-12-07 15:00:32','0','A'),(255,5,'2023-12-07 15:00:33','0','W'),(256,5,'2023-12-07 15:00:33','238','V'),(257,5,'2023-12-07 15:00:33','0','A'),(258,4,'2023-12-07 15:15:02','0','W'),(259,4,'2023-12-07 15:15:02','237','V'),(260,4,'2023-12-07 15:15:02','0','A'),(261,5,'2023-12-07 15:15:02','0','W'),(262,5,'2023-12-07 15:15:02','237','V'),(263,5,'2023-12-07 15:15:02','0','A'),(264,4,'2023-12-07 15:21:25','0','W'),(265,4,'2023-12-07 15:21:25','237','V'),(266,4,'2023-12-07 15:21:25','0','A'),(267,5,'2023-12-07 15:21:25','0','W'),(268,5,'2023-12-07 15:21:25','237','V'),(269,5,'2023-12-07 15:21:25','0','A'),(270,4,'2023-12-07 15:30:03','0','W'),(271,4,'2023-12-07 15:30:03','237','V'),(272,4,'2023-12-07 15:30:03','0','A'),(273,5,'2023-12-07 15:30:03','0','W'),(274,5,'2023-12-07 15:30:03','237','V'),(275,5,'2023-12-07 15:30:03','0','A'),(276,4,'2023-12-07 15:45:03','0','W'),(277,4,'2023-12-07 15:45:03','236','V'),(278,4,'2023-12-07 15:45:03','0','A'),(279,5,'2023-12-07 15:45:03','0','W'),(280,5,'2023-12-07 15:45:03','236','V'),(281,5,'2023-12-07 15:45:03','0','A'),(282,4,'2023-12-07 16:00:04','0','W'),(283,4,'2023-12-07 16:00:04','236','V'),(284,4,'2023-12-07 16:00:04','0','A'),(285,5,'2023-12-07 16:00:04','0','W'),(286,5,'2023-12-07 16:00:04','236','V'),(287,5,'2023-12-07 16:00:04','0','A'),(288,4,'2023-12-07 16:15:03','0','W'),(289,4,'2023-12-07 16:15:03','237','V'),(290,4,'2023-12-07 16:15:03','0','A'),(291,5,'2023-12-07 16:15:03','0','W'),(292,5,'2023-12-07 16:15:03','237','V'),(293,5,'2023-12-07 16:15:03','0','A'),(294,4,'2023-12-07 17:45:14','0','W'),(295,4,'2023-12-07 17:45:14','232','V'),(296,4,'2023-12-07 17:45:14','0','A'),(297,5,'2023-12-07 17:45:14','0','W'),(298,5,'2023-12-07 17:45:14','232','V'),(299,5,'2023-12-07 17:45:14','0','A'),(300,4,'2023-12-08 08:00:07','0','W'),(301,4,'2023-12-08 08:00:07','234','V'),(302,4,'2023-12-08 08:00:07','0','A'),(303,5,'2023-12-08 08:00:08','0','W'),(304,5,'2023-12-08 08:00:08','234','V'),(305,5,'2023-12-08 08:00:08','0','A'),(306,4,'2023-12-08 09:06:19','3','W'),(307,4,'2023-12-08 09:06:19','232','V'),(308,4,'2023-12-08 09:06:19','0','A'),(309,5,'2023-12-08 09:06:19','0','W'),(310,5,'2023-12-08 09:06:19','232','V'),(311,5,'2023-12-08 09:06:19','0','A'),(312,7,'2023-12-08 09:06:19','35','W\''),(313,4,'2023-12-08 09:14:32','3','W'),(314,4,'2023-12-08 09:14:32','233','V'),(315,4,'2023-12-08 09:14:32','0','A'),(316,5,'2023-12-08 09:14:33','0','W'),(317,5,'2023-12-08 09:14:33','233','V'),(318,5,'2023-12-08 09:14:33','0','A'),(319,7,'2023-12-08 09:14:33','27','W\''),(320,4,'2023-12-08 09:15:05','3','W'),(321,4,'2023-12-08 09:15:05','233','V'),(322,4,'2023-12-08 09:15:05','0','A'),(323,5,'2023-12-08 09:15:05','0','W'),(324,5,'2023-12-08 09:15:05','233','V'),(325,5,'2023-12-08 09:15:05','0','A'),(326,4,'2023-12-08 09:30:04','3','W'),(327,4,'2023-12-08 09:30:04','233','V'),(328,4,'2023-12-08 09:30:04','0','A'),(329,5,'2023-12-08 09:30:05','0','W'),(330,5,'2023-12-08 09:30:05','233','V'),(331,5,'2023-12-08 09:30:05','0','A'),(332,7,'2023-12-08 09:30:05','98','W\''),(333,4,'2023-12-08 09:48:16','3','W'),(334,4,'2023-12-08 09:48:16','234','V'),(335,4,'2023-12-08 09:48:16','0','A'),(336,5,'2023-12-08 09:48:16','0','W'),(337,5,'2023-12-08 09:48:16','234','V'),(338,5,'2023-12-08 09:48:16','0','A'),(339,7,'2023-12-08 09:48:16','99','W\''),(340,4,'2023-12-08 09:49:05','3','W'),(341,4,'2023-12-08 09:49:05','234','V'),(342,4,'2023-12-08 09:49:05','0','A'),(343,5,'2023-12-08 09:49:05','0','W'),(344,5,'2023-12-08 09:49:05','234','V'),(345,5,'2023-12-08 09:49:05','0','A'),(346,7,'2023-12-08 09:49:05','43','W\''),(347,4,'2023-12-08 10:00:07','0','W'),(348,4,'2023-12-08 10:00:07','233','V'),(349,4,'2023-12-08 10:00:07','0','A'),(350,5,'2023-12-08 10:00:07','0','W'),(351,5,'2023-12-08 10:00:07','233','V'),(352,5,'2023-12-08 10:00:07','0','A'),(353,7,'2023-12-08 10:00:07','19','W\''),(354,4,'2023-12-08 10:15:07','3','W'),(355,4,'2023-12-08 10:15:07','232','V'),(356,4,'2023-12-08 10:15:07','0','A'),(357,5,'2023-12-08 10:15:07','0','W'),(358,5,'2023-12-08 10:15:07','232','V'),(359,5,'2023-12-08 10:15:07','0','A'),(360,7,'2023-12-08 10:15:07','24','W\''),(361,4,'2023-12-08 10:30:07','3','W'),(362,4,'2023-12-08 10:30:07','232','V'),(363,4,'2023-12-08 10:30:07','0','A'),(364,5,'2023-12-08 10:30:07','0','W'),(365,5,'2023-12-08 10:30:07','232','V'),(366,5,'2023-12-08 10:30:07','0','A'),(367,4,'2023-12-08 10:45:06','3','W'),(368,4,'2023-12-08 10:45:06','232','V'),(369,4,'2023-12-08 10:45:06','0','A'),(370,5,'2023-12-08 10:45:06','0','W'),(371,5,'2023-12-08 10:45:06','232','V'),(372,5,'2023-12-08 10:45:06','0','A'),(373,4,'2023-12-08 11:00:07','3','W'),(374,4,'2023-12-08 11:00:07','232','V'),(375,4,'2023-12-08 11:00:07','0','A'),(376,5,'2023-12-08 11:00:07','0','W'),(377,5,'2023-12-08 11:00:07','232','V'),(378,5,'2023-12-08 11:00:07','0','A'),(379,4,'2023-12-08 11:15:07','3','W'),(380,4,'2023-12-08 11:15:07','233','V'),(381,4,'2023-12-08 11:15:07','0','A'),(382,5,'2023-12-08 11:15:07','0','W'),(383,5,'2023-12-08 11:15:07','233','V'),(384,5,'2023-12-08 11:15:07','0','A'),(385,4,'2023-12-08 11:30:06','3','W'),(386,4,'2023-12-08 11:30:06','234','V'),(387,4,'2023-12-08 11:30:06','0','A'),(388,5,'2023-12-08 11:30:06','0','W'),(389,5,'2023-12-08 11:30:06','234','V'),(390,5,'2023-12-08 11:30:06','0','A'),(391,4,'2024-02-08 09:14:12','26','W'),(392,4,'2024-02-08 09:14:12','235','V'),(393,4,'2024-02-08 09:14:12','0','A'),(394,5,'2024-02-08 09:14:12','0','W'),(395,5,'2024-02-08 09:14:12','234','V'),(396,5,'2024-02-08 09:14:13','0','A'),(397,4,'2024-02-08 09:15:03','25','W'),(398,4,'2024-02-08 09:15:03','235','V'),(399,4,'2024-02-08 09:15:03','0','A'),(400,5,'2024-02-08 09:15:04','0','W'),(401,5,'2024-02-08 09:15:04','235','V'),(402,4,'2024-02-08 09:15:04','26','W'),(403,5,'2024-02-08 09:15:04','0','A'),(404,4,'2024-02-08 09:15:04','235','V'),(405,4,'2024-02-08 09:15:04','0','A'),(406,5,'2024-02-08 09:15:05','0','W'),(407,5,'2024-02-08 09:15:05','235','V'),(408,5,'2024-02-08 09:15:05','0','A'),(409,4,'2024-02-08 09:16:26','24','W'),(410,4,'2024-02-08 09:16:26','234','V'),(411,4,'2024-02-08 09:16:26','0','A'),(412,5,'2024-02-08 09:16:26','0','W'),(413,5,'2024-02-08 09:16:26','234','V'),(414,5,'2024-02-08 09:16:26','0','A'),(415,4,'2024-02-08 09:30:02','22','W'),(416,4,'2024-02-08 09:30:03','235','V'),(417,4,'2024-02-08 09:30:03','0','A'),(418,5,'2024-02-08 09:30:03','0','W'),(419,5,'2024-02-08 09:30:03','235','V'),(420,5,'2024-02-08 09:30:03','0','A'),(421,4,'2024-02-08 09:31:07','21','W'),(422,4,'2024-02-08 09:31:08','235','V'),(423,4,'2024-02-08 09:31:08','0','A'),(424,5,'2024-02-08 09:31:08','0','W'),(425,5,'2024-02-08 09:31:08','235','V'),(426,5,'2024-02-08 09:31:08','0','A'),(427,4,'2024-02-08 09:32:40','0','W'),(428,4,'2024-02-08 09:32:40','234','V'),(429,4,'2024-02-08 09:32:40','0','A'),(430,5,'2024-02-08 09:32:41','0','W'),(431,5,'2024-02-08 09:32:41','234','V'),(432,5,'2024-02-08 09:32:41','0','A'),(433,4,'2024-02-08 09:33:49','21','W'),(434,4,'2024-02-08 09:33:50','234','V'),(435,4,'2024-02-08 09:33:50','0','A'),(436,5,'2024-02-08 09:33:50','0','W'),(437,5,'2024-02-08 09:33:50','234','V'),(438,5,'2024-02-08 09:33:50','0','A'),(439,4,'2024-02-08 09:39:37','0','W'),(440,4,'2024-02-08 09:39:37','235','V'),(441,4,'2024-02-08 09:39:38','0','A'),(442,5,'2024-02-08 09:39:38','0','W'),(443,5,'2024-02-08 09:39:38','234','V'),(444,5,'2024-02-08 09:39:38','0','A'),(445,4,'2024-02-08 09:44:29','0','W'),(446,4,'2024-02-08 09:44:29','234','V'),(447,4,'2024-02-08 09:44:29','0','A'),(448,5,'2024-02-08 09:44:29','0','W'),(449,5,'2024-02-08 09:44:29','234','V'),(450,5,'2024-02-08 09:44:29','0','A'),(451,4,'2024-02-08 09:45:01','0','W'),(452,4,'2024-02-08 09:45:01','234','V'),(453,4,'2024-02-08 09:45:01','0','A'),(454,5,'2024-02-08 09:45:02','0','W'),(455,5,'2024-02-08 09:45:02','235','V'),(456,5,'2024-02-08 09:45:02','0','A'),(457,4,'2024-02-08 09:45:08','24','W'),(458,4,'2024-02-08 09:45:08','234','V'),(459,4,'2024-02-08 09:45:08','0','A'),(460,5,'2024-02-08 09:45:08','0','W'),(461,5,'2024-02-08 09:45:08','234','V'),(462,5,'2024-02-08 09:45:08','0','A'),(463,4,'2024-02-08 09:46:02','22','W'),(464,4,'2024-02-08 09:46:02','234','V'),(465,4,'2024-02-08 09:46:02','0','A'),(466,5,'2024-02-08 09:46:03','0','W'),(467,5,'2024-02-08 09:46:03','234','V'),(468,5,'2024-02-08 09:46:03','0','A'),(469,4,'2024-02-08 09:47:38','20','W'),(470,4,'2024-02-08 09:47:39','234','V'),(471,4,'2024-02-08 09:47:39','0','A'),(472,5,'2024-02-08 09:47:39','0','W'),(473,5,'2024-02-08 09:47:39','234','V'),(474,5,'2024-02-08 09:47:39','0','A');
/*!40000 ALTER TABLE `mesures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objets`
--

DROP TABLE IF EXISTS `objets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `objets` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ID_MAISON` int(11) DEFAULT NULL,
  `NOM` varchar(50) DEFAULT NULL,
  `ETAT` varchar(50) DEFAULT NULL,
  `TYPE` varchar(50) DEFAULT NULL,
  `IP` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID_MAISON` (`ID_MAISON`),
  CONSTRAINT `FK_objets_maison` FOREIGN KEY (`ID_MAISON`) REFERENCES `maison` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objets`
--

LOCK TABLES `objets` WRITE;
/*!40000 ALTER TABLE `objets` DISABLE KEYS */;
INSERT INTO `objets` VALUES (1,1,'Prise2','false','CONSO','192.168.1.154'),(2,2,'Ventilo','true','CONSO','192.168.1.164'),(3,1,'Prise1','true','CONSO','Prise1'),(4,1,'Prise_shelly0','true','CONSO','192.168.1.128,0'),(5,1,'Prise_shelly1','true','CONSO','192.168.1.128,1'),(6,1,'Onduleur','true','PROD','192.168.1.157'),(7,1,'esp1','true','CONSO','192.168.1.141');
/*!40000 ALTER TABLE `objets` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-08  9:49:14
