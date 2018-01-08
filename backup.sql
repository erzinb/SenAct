-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: senact
-- ------------------------------------------------------
-- Server version	5.5.41-0+wheezy1

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
-- Table structure for table `activator_states`
--

DROP TABLE IF EXISTS `activator_states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activator_states` (
  `state` tinyint(2) NOT NULL,
  `description` varchar(16) NOT NULL,
  PRIMARY KEY (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator_states`
--

LOCK TABLES `activator_states` WRITE;
/*!40000 ALTER TABLE `activator_states` DISABLE KEYS */;
INSERT INTO `activator_states` VALUES (0,'OFF'),(1,'ON_TOGGLE_OFF'),(2,'OFF_TOGGLE_ON'),(3,'ON_TOGGLE_ON');
/*!40000 ALTER TABLE `activator_states` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activator_types`
--

DROP TABLE IF EXISTS `activator_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activator_types` (
  `type` tinyint(4) NOT NULL,
  `description` varchar(16) NOT NULL,
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activator_types`
--

LOCK TABLES `activator_types` WRITE;
/*!40000 ALTER TABLE `activator_types` DISABLE KEYS */;
INSERT INTO `activator_types` VALUES (0,'COMMON'),(1,'TOGGLE');
/*!40000 ALTER TABLE `activator_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activators`
--

DROP TABLE IF EXISTS `activators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activators` (
  `id` tinyint(3) NOT NULL AUTO_INCREMENT,
  `gpio` smallint(6) NOT NULL,
  `name` varchar(16) DEFAULT NULL,
  `type` tinyint(4) NOT NULL,
  `toggle_time_ms` int(11) DEFAULT NULL,
  `state` tinyint(2) NOT NULL,
  `block_till` datetime DEFAULT NULL,
  `blocking` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activators`
--

LOCK TABLES `activators` WRITE;
/*!40000 ALTER TABLE `activators` DISABLE KEYS */;
INSERT INTO `activators` VALUES (1,8,'GORILEC',1,2000,0,'2015-07-25 10:59:46',0),(2,9,'PUMPA_VODA',0,0,0,'2015-07-25 10:59:55',0),(3,7,'PUMPA_STANOVANJE',0,0,0,'2015-07-24 17:18:09',0),(4,0,'VENTIL-ODPIRANJE',0,0,0,'2015-07-24 17:18:09',0),(5,2,'VENTIL-ZAPIRANJE',0,0,0,'2015-07-24 17:18:07',0),(6,3,'LUC',0,0,0,'2015-07-24 17:18:11',0);
/*!40000 ALTER TABLE `activators` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programs` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `activatorId` smallint(6) DEFAULT NULL,
  `sensorId` smallint(6) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `stop_time` time DEFAULT NULL,
  `month` tinyint(1) DEFAULT NULL,
  `week` tinyint(1) DEFAULT NULL,
  `day` tinyint(4) DEFAULT NULL,
  `dayinweek` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programs`
--

LOCK TABLES `programs` WRITE;
/*!40000 ALTER TABLE `programs` DISABLE KEYS */;
INSERT INTO `programs` VALUES (1,1,1,'10:15:00','20:20:00',7,NULL,NULL,NULL),(2,2,2,'11:00:00','20:20:00',7,NULL,NULL,NULL);
/*!40000 ALTER TABLE `programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_types`
--

DROP TABLE IF EXISTS `sensor_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_types` (
  `id` int(11) DEFAULT NULL,
  `type` varchar(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_types`
--

LOCK TABLES `sensor_types` WRITE;
/*!40000 ALTER TABLE `sensor_types` DISABLE KEYS */;
INSERT INTO `sensor_types` VALUES (1,'RC'),(16,'DS18S20'),(40,'DS18B20'),(34,'DS1822');
/*!40000 ALTER TABLE `sensor_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensors`
--

DROP TABLE IF EXISTS `sensors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensors` (
  `id` smallint(6) NOT NULL AUTO_INCREMENT,
  `sensorId` varchar(12) DEFAULT NULL,
  `name` varchar(16) NOT NULL,
  `type` varchar(16) NOT NULL,
  `TL` decimal(5,1) DEFAULT NULL,
  `TH` decimal(5,1) DEFAULT NULL,
  `T` decimal(5,1) DEFAULT NULL,
  `k` float DEFAULT NULL,
  `n` float DEFAULT NULL,
  `gpio` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensors`
--

LOCK TABLES `sensors` WRITE;
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;
INSERT INTO `sensors` VALUES (1,'1','T1','RC',20.5,21.0,25.5,0.255,-58.5,13),(125,'0008026ed6bd','TX','DS18S20',NULL,NULL,25.6,NULL,NULL,0),(126,'0008026ef3e1','TX','DS18S20',NULL,NULL,25.5,NULL,NULL,0);
/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-07-25 13:00:24
