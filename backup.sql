-- MySQL dump 10.13  Distrib 5.1.39, for Win64 (unknown)
--
-- Host: localhost    Database: shinkey
-- ------------------------------------------------------
-- Server version	5.1.39-community-log

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `email` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `firstName` varchar(32) NOT NULL,
  `lastName` varchar(32) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('dfg','dfg','dfg','dfg'),('shin','8631','Shin','Guo');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clef`
--

DROP TABLE IF EXISTS `clef`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clef` (
  `keyNumber` varchar(32) NOT NULL,
  `copyNumber` int(11) NOT NULL,
  `depositValue` int(11) NOT NULL,
  `opens` varchar(32) NOT NULL,
  `status` varchar(32) NOT NULL,
  PRIMARY KEY (`keyNumber`,`copyNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clef`
--

LOCK TABLES `clef` WRITE;
/*!40000 ALTER TABLE `clef` DISABLE KEYS */;
INSERT INTO `clef` VALUES ('A2N1',0,20,'door','lost'),('A2N1',1,20,'door','lost'),('A2N1',2,20,'door','lost'),('A2N1',3,20,'door','lost'),('A2N1',4,20,'door','lost'),('A2N1',5,20,'door','available'),('A2N1',6,20,'door','lent'),('A2N1',7,20,'door','available'),('A2N1',8,20,'door','available'),('A2N1',9,20,'door','available'),('A2N1',10,20,'door','available'),('A2N1',11,20,'door','available'),('A2N1',12,20,'door','available'),('A2N1',13,20,'door','available'),('A2N1',14,20,'door','available'),('A2N1',15,20,'door','available'),('A2N1',16,20,'door','available'),('A2N1',17,20,'door','available'),('A2N1',18,20,'door','available'),('A2N1',19,20,'door','available'),('A2N6',1,20,'door','available'),('A2N6',2,20,'door','lost'),('A2N6',3,20,'door','lost'),('A2N6',4,20,'door','available'),('A2N6',5,20,'door','lost'),('A2N6',6,20,'door','available'),('A2N6',7,20,'door','available'),('A2N6',8,20,'door','available'),('A2N6',9,20,'door','available'),('A2N6',10,20,'door','available'),('A2N6',11,20,'door','available'),('A2N6',12,20,'door','available'),('A2N6',13,20,'door','available'),('A2N6',14,20,'door','available'),('A2N6',15,20,'door','available'),('A2N6',16,20,'door','available'),('A2N6',17,20,'door','available'),('A2N6',18,20,'door','available'),('A2N7',1,20,'mailBox','available'),('A2N7',2,20,'mailBox','available'),('A2N7',3,20,'mailBox','available'),('A2N7',4,20,'mailBox','available'),('A2N7',5,20,'mailBox','available'),('A2N7',6,20,'mailBox','available'),('A2N7',7,20,'mailBox','available'),('A2N7',8,20,'mailBox','available'),('A2N7',9,20,'mailBox','available'),('A2N7',10,20,'mailBox','available'),('A2N7',11,20,'mailBox','available'),('A2N7',12,20,'mailBox','available'),('A2N8',1,20,'door','available'),('A2N8',2,20,'door','available'),('A2N8',3,20,'door','available'),('A2N8',4,20,'door','available'),('sdf',123,20,'door','available');
/*!40000 ALTER TABLE `clef` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client` (
  `email` varchar(32) NOT NULL,
  `firstName` varchar(32) NOT NULL,
  `lastName` varchar(32) NOT NULL,
  `address` varchar(32) NOT NULL,
  `city` varchar(32) NOT NULL,
  `province` varchar(32) NOT NULL,
  `postcode` varchar(32) NOT NULL,
  `phoneNumber` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES ('123','123','123','123','123','123','123','123'),('coruea@ualberta.ca','amandine','corue','main campus','edmonton111','alberta111','T5K111','(780)710-1234'),('desrochers@ualberta.ca123','M','Desrochers123','Campus Saint-Jean123','Edmonto','Albert','T6C4G','(780)465-8700'),('lemieux@ualberta.ca','H','Lemieux','Campus Saint-Jean','Edmonton','Alberta','T6C4G9','(780)465-8700'),('pellerin@ualberta.ca','M','Pellerin','Campus Saint-Jean','Edmonton','Alberta','T6C4G9','(780)465-8700'),('roy@ualberta.ca123','Mark','Roy','Canf','Edmonton','Alberta','T5K2P9','(780)7100-4657');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lent`
--

DROP TABLE IF EXISTS `lent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lent` (
  `keyNumber` varchar(32) NOT NULL,
  `copyNumber` int(11) NOT NULL,
  `email` varchar(32) NOT NULL,
  `lendDate` date NOT NULL,
  `paymentMethod` varchar(32) NOT NULL,
  `expectedReturnDate` date NOT NULL,
  PRIMARY KEY (`keyNumber`,`copyNumber`),
  KEY `email` (`email`),
  CONSTRAINT `lent_ibfk_1` FOREIGN KEY (`email`) REFERENCES `client` (`email`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lent`
--

LOCK TABLES `lent` WRITE;
/*!40000 ALTER TABLE `lent` DISABLE KEYS */;
INSERT INTO `lent` VALUES ('A2N1',6,'123','2017-08-08','debit','2017-08-14');
/*!40000 ALTER TABLE `lent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `losshistory`
--

DROP TABLE IF EXISTS `losshistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `losshistory` (
  `keyNumber` varchar(32) NOT NULL,
  `copyNumber` int(11) NOT NULL,
  `email` varchar(32) NOT NULL,
  `lendDate` date NOT NULL,
  `lossDate` date NOT NULL,
  `payMethod` varchar(32) NOT NULL,
  PRIMARY KEY (`keyNumber`,`copyNumber`),
  KEY `email` (`email`),
  CONSTRAINT `losshistory_ibfk_1` FOREIGN KEY (`email`) REFERENCES `client` (`email`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `losshistory`
--

LOCK TABLES `losshistory` WRITE;
/*!40000 ALTER TABLE `losshistory` DISABLE KEYS */;
INSERT INTO `losshistory` VALUES ('A2N1',0,'lemieux@ualberta.ca','2017-07-24','2017-07-24','credit'),('A2N1',1,'desrochers@ualberta.ca123','2017-07-24','2017-07-24','debit'),('A2N1',2,'coruea@ualberta.ca','2017-08-08','2017-08-08','debit'),('A2N1',3,'desrochers@ualberta.ca123','2017-07-24','2017-07-24','debit'),('A2N1',4,'lemieux@ualberta.ca','2017-07-24','2017-07-25','cash'),('A2N6',2,'coruea@ualberta.ca','2017-07-24','2017-07-24','debit'),('A2N6',3,'desrochers@ualberta.ca123','2017-07-24','2017-07-25','credit'),('A2N6',5,'coruea@ualberta.ca','2017-07-24','2017-07-24','debit');
/*!40000 ALTER TABLE `losshistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returnhistory`
--

DROP TABLE IF EXISTS `returnhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `returnhistory` (
  `returnId` int(11) NOT NULL AUTO_INCREMENT,
  `keyNumber` varchar(32) NOT NULL,
  `copyNumber` int(11) DEFAULT NULL,
  `email` varchar(32) NOT NULL,
  `lendDate` date NOT NULL,
  `returnDate` date NOT NULL,
  `lendPaymentMethod` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`returnId`),
  KEY `email` (`email`),
  CONSTRAINT `returnhistory_ibfk_1` FOREIGN KEY (`email`) REFERENCES `client` (`email`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returnhistory`
--

LOCK TABLES `returnhistory` WRITE;
/*!40000 ALTER TABLE `returnhistory` DISABLE KEYS */;
INSERT INTO `returnhistory` VALUES (26,'A2N1',0,'desrochers@ualberta.ca123','2017-07-24','2017-07-24','debit'),(27,'A2N1',1,'desrochers@ualberta.ca123','2017-07-24','2017-07-24','debit'),(28,'A2N6',5,'roy@ualberta.ca123','2017-07-24','2017-07-24','debit'),(29,'A2N8',1,'coruea@ualberta.ca','2017-07-24','2017-07-24','debit'),(30,'A2N1',2,'coruea@ualberta.ca','2017-07-24','2017-07-25','debit'),(31,'A2N1',2,'coruea@ualberta.ca','2017-07-25','2017-07-25','debit'),(32,'A2N1',2,'desrochers@ualberta.ca123','2017-07-25','2017-08-08','debit'),(33,'A2N1',2,'coruea@ualberta.ca','2017-08-08','2017-08-08','credit'),(34,'A2N1',7,'coruea@ualberta.ca','2017-08-08','2017-08-08','credit'),(35,'A2N1',5,'123','2017-08-08','2017-08-08','debit');
/*!40000 ALTER TABLE `returnhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room` (
  `keyNumber` varchar(32) NOT NULL,
  `room` varchar(32) NOT NULL,
  PRIMARY KEY (`keyNumber`,`room`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES ('A2N1',''),('A2N7','ghj'),('A2N8','3-12'),('sdf','123');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `value`
--

DROP TABLE IF EXISTS `value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `value` (
  `depositValue` int(11) NOT NULL,
  `penaltyValue` int(11) NOT NULL,
  PRIMARY KEY (`depositValue`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `value`
--

LOCK TABLES `value` WRITE;
/*!40000 ALTER TABLE `value` DISABLE KEYS */;
INSERT INTO `value` VALUES (20,100),(80,500);
/*!40000 ALTER TABLE `value` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-08 11:39:09
