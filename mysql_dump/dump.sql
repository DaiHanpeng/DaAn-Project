-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: 192.168.0.104    Database: daan
-- ------------------------------------------------------
-- Server version	5.7.14

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `table_last_update_timestamp`
--

DROP TABLE IF EXISTS `table_last_update_timestamp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `table_last_update_timestamp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `table_name` varchar(24) NOT NULL,
  `update_timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`,`table_name`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `table_name_UNIQUE` (`table_name`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_last_update_timestamp`
--

LOCK TABLES `table_last_update_timestamp` WRITE;
/*!40000 ALTER TABLE `table_last_update_timestamp` DISABLE KEYS */;
INSERT INTO `table_last_update_timestamp` VALUES (9,'Control','2000-01-01 01:01:01'),(10,'Calibration','2010-12-12 10:12:22');
/*!40000 ALTER TABLE `table_last_update_timestamp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'daan'
--

--
-- Dumping routines for database 'daan'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-30 14:33:20
