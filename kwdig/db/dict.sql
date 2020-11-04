-- MySQL dump 10.13  Distrib 8.0.22, for Linux (aarch64)
--
-- Host: localhost    Database: patent
-- ------------------------------------------------------
-- Server version	8.0.22-0ubuntu0.20.04.2

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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywords`
--

LOCK TABLES `keywords` WRITE;
/*!40000 ALTER TABLE `keywords` DISABLE KEYS */;
INSERT INTO `keywords` VALUES (1,'network','测试 注释中文'),(2,'device','设备终端'),(3,'dynamic signaling','动态指令'),(4,'different frequency resource','不同频率源'),(5,'radio resource control','测试系统'),(6,'aspect of the present','这是一个测试'),(7,'the method of claim','所声明之方法'),(8,'according to','依据'),(10,'computer program','计算机程序'),(11,'according to embodiments of the present','测试中文'),(12,'an identification of the network','测试中文'),(13,'embodiments of the present','测试中文'),(14,'when number of symbols in one slot is configured with','测试中文'),(15,'code division multiple access','测试中文,haha'),(16,'an identification of','测算'),(17,'this is a test','添加测试，必须小写'),(18,'as illustrated in',''),(20,'human mind deep learning','人脑深度学习');
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
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phrase_omit`
--

LOCK TABLES `phrase_omit` WRITE;
/*!40000 ALTER TABLE `phrase_omit` DISABLE KEYS */;
INSERT INTO `phrase_omit` VALUES (60,'according to'),(56,'an error'),(45,'an index of'),(116,'and by'),(52,'and in'),(42,'and so'),(4,'and the'),(6,'and type'),(21,'as an'),(122,'as in'),(111,'as the'),(84,'as time'),(62,'as to'),(47,'as used'),(72,'at least'),(86,'at the'),(93,'at the same'),(109,'at the time'),(85,'at the time of'),(73,'at this'),(61,'based on'),(7,'but the'),(2,'by the'),(57,'by using'),(24,'can be'),(67,'degree of'),(78,'due to'),(77,'each of'),(103,'for all'),(49,'for another'),(48,'for each'),(18,'for the'),(23,'from the'),(30,'if the'),(40,'in an'),(36,'in another'),(39,'in one'),(63,'in order to'),(41,'in other'),(38,'in some'),(25,'in step'),(27,'in such'),(87,'in such an'),(120,'in that'),(28,'in the'),(112,'in the case'),(121,'in the case of'),(98,'in the first'),(130,'in the second'),(129,'in the step'),(8,'in this'),(43,'in time'),(59,'in which'),(124,'included in'),(1,'is a'),(126,'is able to'),(125,'is an'),(101,'is not'),(113,'is then'),(31,'is to'),(19,'it can'),(26,'it can be'),(34,'it is'),(102,'it is possible to'),(17,'it was'),(9,'it will be'),(94,'like to'),(128,'limited to'),(10,'may be'),(117,'not less than'),(114,'not only'),(32,'of such'),(29,'of the'),(5,'on the'),(110,'on the other'),(64,'on this'),(33,'or an'),(53,'or by'),(44,'or in'),(35,'or more'),(68,'or the'),(127,'part of'),(119,'plurality of'),(106,'possible to'),(123,'result of'),(54,'so as to'),(104,'so that'),(22,'such as'),(65,'such as an'),(66,'such as the'),(131,'that are'),(46,'that is'),(55,'the first'),(69,'the item'),(105,'the same'),(11,'there are'),(15,'there can be'),(58,'there is'),(3,'to a'),(50,'to as'),(12,'to be'),(90,'to each other'),(107,'to have'),(13,'to the'),(14,'to those'),(71,'used as'),(51,'used by'),(108,'value of'),(97,'variable of'),(20,'wherein the ue is'),(115,'which are'),(100,'which has'),(74,'which is'),(118,'which is the'),(16,'which may be'),(75,'with another'),(96,'with each'),(79,'with the');
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
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `word_omit`
--

LOCK TABLES `word_omit` WRITE;
/*!40000 ALTER TABLE `word_omit` DISABLE KEYS */;
INSERT INTO `word_omit` VALUES (1,'a'),(254,'able'),(169,'about'),(92,'above'),(261,'according'),(64,'after'),(26,'all'),(22,'also'),(5,'am'),(2,'an'),(10,'and'),(139,'and/or'),(40,'another'),(38,'any'),(6,'are'),(51,'as'),(8,'at'),(76,'based'),(35,'be'),(245,'because'),(91,'been'),(115,'before'),(83,'being'),(260,'below'),(100,'between'),(134,'body'),(125,'but'),(39,'by'),(60,'can'),(117,'case'),(136,'center'),(195,'color'),(253,'common'),(159,'could'),(84,'cpu'),(160,'daily'),(68,'data'),(237,'date'),(140,'day'),(229,'depth'),(232,'detail'),(241,'different'),(208,'does'),(156,'down'),(258,'due'),(28,'each'),(255,'eight'),(79,'end'),(58,'error'),(130,'etc'),(110,'example'),(263,'examples'),(189,'feature'),(242,'fifth'),(95,'fig'),(53,'first'),(236,'flag'),(9,'for'),(238,'form'),(126,'forth'),(214,'four'),(183,'fourth'),(49,'from'),(248,'further'),(146,'get'),(56,'has'),(46,'have'),(173,'having'),(206,'here'),(143,'high'),(144,'however'),(90,'id'),(43,'if'),(11,'in'),(190,'include'),(213,'included'),(209,'includes'),(193,'including'),(103,'index'),(227,'inter'),(44,'into'),(4,'is'),(19,'it'),(197,'key'),(215,'known'),(199,'large'),(247,'larger'),(256,'later'),(94,'least'),(223,'less'),(203,'light'),(65,'like'),(240,'likely'),(178,'limited'),(250,'list'),(196,'long'),(212,'low'),(194,'lower'),(102,'many'),(174,'map'),(17,'may'),(216,'mean'),(71,'means'),(224,'medium'),(210,'method'),(34,'more'),(116,'move'),(207,'new'),(87,'next'),(104,'no'),(243,'normalized'),(27,'not'),(166,'note'),(171,'now'),(148,'number'),(217,'object'),(7,'of'),(59,'on'),(20,'one'),(42,'only'),(18,'or'),(41,'other'),(149,'out'),(70,'output'),(204,'over'),(201,'own'),(202,'pair'),(88,'part'),(230,'parts'),(239,'point'),(69,'program'),(161,'public'),(257,'reason'),(157,'result'),(228,'right'),(170,'row'),(50,'same'),(200,'say'),(251,'screen'),(73,'second'),(54,'set'),(163,'short'),(244,'showing'),(75,'since'),(185,'six'),(33,'size'),(62,'small'),(105,'so'),(48,'some'),(264,'specify'),(179,'sql'),(265,'stably'),(218,'start'),(72,'status'),(61,'step'),(219,'steps'),(118,'still'),(23,'such'),(259,'sum'),(231,'system'),(108,'table'),(249,'tag'),(188,'temp'),(32,'than'),(57,'that'),(3,'the'),(145,'their'),(141,'them'),(86,'then'),(36,'there'),(262,'thereby'),(96,'therefore'),(133,'these'),(138,'they'),(99,'third'),(30,'this'),(63,'those'),(220,'three'),(128,'through'),(154,'thus'),(52,'time'),(221,'times'),(55,'to'),(153,'together'),(114,'too'),(78,'top'),(191,'total'),(225,'tree'),(106,'true'),(25,'two'),(187,'type'),(235,'typical'),(131,'up'),(29,'use'),(21,'used'),(162,'user'),(211,'uses'),(67,'using'),(233,'value'),(176,'variable'),(234,'vector'),(198,'very'),(82,'view'),(45,'was'),(205,'water'),(175,'way'),(252,'web'),(31,'when'),(85,'where'),(192,'wherein'),(226,'whether'),(24,'which'),(81,'while'),(246,'whose'),(37,'will'),(47,'with'),(182,'within'),(89,'without'),(93,'yes'),(66,'yet'),(222,'yield');
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

-- Dump completed on 2020-11-04  9:55:07
