-- MySQL dump 10.13  Distrib 8.0.21, for Linux (aarch64)
--
-- Host: localhost    Database: patent
-- ------------------------------------------------------
-- Server version	8.0.21-0ubuntu0.20.04.4

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
-- Table structure for table `keywords`
--

DROP TABLE IF EXISTS `keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keywords` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `words` varchar(512) NOT NULL,
  `descr` text,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `words` (`words`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywords`
--

LOCK TABLES `keywords` WRITE;
/*!40000 ALTER TABLE `keywords` DISABLE KEYS */;
INSERT INTO `keywords` VALUES (1,'network','测试 注释中文'),(2,'device','设备终端'),(3,'dynamic signaling','动态指令'),(4,'different frequency resource','不同频率源'),(5,'radio resource control','测试系统'),(6,'aspect of the present','这是一个测试'),(7,'the method of claim','所声明之方法'),(8,'according to','测试'),(10,'computer program','测试3'),(11,'according to embodiments of the present','测试中文'),(12,'an identification of the network','测试中文'),(13,'embodiments of the present','测试中文'),(14,'when number of symbols in one slot is configured with','测试中文'),(15,'code division multiple access','测试中文,haha'),(16,'an identification of','测算');
/*!40000 ALTER TABLE `keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phrase_omit`
--

DROP TABLE IF EXISTS `phrase_omit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phrase_omit` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `phrase` varchar(512) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `phrase` (`phrase`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phrase_omit`
--

LOCK TABLES `phrase_omit` WRITE;
/*!40000 ALTER TABLE `phrase_omit` DISABLE KEYS */;
INSERT INTO `phrase_omit` VALUES (56,'an error'),(45,'an index of'),(52,'and in'),(42,'and so'),(4,'and the'),(6,'and type'),(21,'as an'),(47,'as used'),(7,'but the'),(2,'by the'),(57,'by using'),(24,'can be'),(49,'for another'),(48,'for each'),(18,'for the'),(23,'from the'),(30,'if the'),(40,'in an'),(36,'in another'),(39,'in one'),(41,'in other'),(38,'in some'),(25,'in step'),(27,'in such'),(28,'in the'),(8,'in this'),(43,'in time'),(1,'is a'),(31,'is to'),(19,'it can'),(26,'it can be'),(34,'it is'),(17,'it was'),(9,'it will be'),(10,'may be'),(32,'of such'),(29,'of the'),(5,'on the'),(33,'or an'),(53,'or by'),(44,'or in'),(35,'or more'),(54,'so as to'),(22,'such as'),(46,'that is'),(55,'the first'),(11,'there are'),(15,'there can be'),(58,'there is'),(3,'to a'),(50,'to as'),(12,'to be'),(13,'to the'),(14,'to those'),(51,'used by'),(20,'wherein the ue is'),(16,'which may be');
/*!40000 ALTER TABLE `phrase_omit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `word_omit`
--

DROP TABLE IF EXISTS `word_omit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `word_omit` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(64) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `word_omit`
--

LOCK TABLES `word_omit` WRITE;
/*!40000 ALTER TABLE `word_omit` DISABLE KEYS */;
INSERT INTO `word_omit` VALUES (1,'a'),(64,'after'),(26,'all'),(22,'also'),(5,'am'),(2,'an'),(10,'and'),(40,'another'),(38,'any'),(6,'are'),(51,'as'),(8,'at'),(35,'be'),(39,'by'),(60,'can'),(68,'data'),(28,'each'),(58,'error'),(53,'first'),(9,'for'),(49,'from'),(56,'has'),(46,'have'),(43,'if'),(11,'in'),(44,'into'),(4,'is'),(19,'it'),(65,'like'),(17,'may'),(71,'means'),(34,'more'),(27,'not'),(7,'of'),(59,'on'),(20,'one'),(42,'only'),(18,'or'),(41,'other'),(70,'output'),(69,'program'),(50,'same'),(54,'set'),(33,'size'),(62,'small'),(48,'some'),(61,'step'),(23,'such'),(32,'than'),(57,'that'),(3,'the'),(36,'there'),(30,'this'),(63,'those'),(52,'time'),(55,'to'),(25,'two'),(29,'use'),(21,'used'),(67,'using'),(45,'was'),(31,'when'),(24,'which'),(37,'will'),(47,'with'),(66,'yet');
/*!40000 ALTER TABLE `word_omit` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-02 21:23:01
