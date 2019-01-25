-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: new_courts_data
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.10.2

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
-- Table structure for table `alerts`
--

DROP TABLE IF EXISTS `alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `court_name` varchar(100) DEFAULT NULL COMMENT '	',
  `bench` varchar(25) DEFAULT NULL,
  `start_date` varchar(25) DEFAULT NULL,
  `end_date` varchar(25) DEFAULT NULL,
  `error_message` longtext,
  `case_id` varchar(100) DEFAULT NULL,
  `page_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gst_advance_authority`
--

DROP TABLE IF EXISTS `gst_advance_authority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gst_advance_authority` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `s_no` varchar(100) DEFAULT NULL,
  `state_ut` varchar(200) DEFAULT NULL,
  `name_of_applicant` varchar(200) DEFAULT NULL,
  `questions` longtext,
  `case_id` varchar(100) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `category_as_per_sgst_act` varchar(300) DEFAULT NULL,
  `pdf_url` text,
  `pdf_filename` text,
  `text_filename` text,
  `text_data` longtext,
  `is_json` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kolkata`
--

DROP TABLE IF EXISTS `kolkata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kolkata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` varchar(100) DEFAULT NULL,
  `judgment_date` varchar(100) DEFAULT NULL,
  `pdf_url` text,
  `pdf_filename` text,
  `text_filename` text,
  `text_data` longtext,
  `is_json` tinyint(4) DEFAULT '0',
  `case_type` varchar(25) DEFAULT NULL,
  `case_no` varchar(100) DEFAULT NULL,
  `case_year` varchar(100) DEFAULT NULL,
  `bench` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tracker`
--

DROP TABLE IF EXISTS `tracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tracker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `court_name` varchar(25) DEFAULT NULL,
  `bench` varchar(25) DEFAULT NULL,
  `start_date` varchar(25) DEFAULT NULL,
  `end_date` varchar(25) DEFAULT NULL,
  `no_tries` int(11) DEFAULT '0',
  `total_cases` int(11) DEFAULT '0',
  `inserted_cases` int(11) DEFAULT '0',
  `no_nodata` int(11) DEFAULT '0',
  `no_alerts` int(11) DEFAULT '0',
  `no_pdf` int(11) DEFAULT '0',
  `no_text` int(11) DEFAULT '0',
  `no_json` int(11) DEFAULT '0',
  `transferred_pdf` int(11) DEFAULT '0',
  `transferred_text` int(11) DEFAULT '0',
  `transferred_json` int(11) DEFAULT '0',
  `emergency_exit` tinyint(1) DEFAULT '0',
  `status` varchar(25) DEFAULT NULL,
  `page_no` mediumint(9) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`court_name`),
  KEY `bench` (`bench`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tracker_history`
--

DROP TABLE IF EXISTS `tracker_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tracker_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `court_name` varchar(25) DEFAULT NULL,
  `bench` varchar(25) DEFAULT NULL,
  `start_date` varchar(25) DEFAULT NULL,
  `end_date` varchar(25) DEFAULT NULL,
  `no_tries` int(11) DEFAULT NULL,
  `total_cases` int(11) DEFAULT NULL,
  `inserted_cases` int(11) DEFAULT NULL,
  `no_nodata` int(11) DEFAULT NULL,
  `no_alerts` int(11) DEFAULT NULL,
  `no_pdf` int(11) DEFAULT NULL,
  `no_text` int(11) DEFAULT NULL,
  `no_json` int(11) DEFAULT NULL,
  `transferred_pdf` int(11) DEFAULT NULL,
  `transferred_text` int(11) DEFAULT NULL,
  `transferred_json` int(11) DEFAULT NULL,
  `emergency_exit` tinyint(1) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-01-25 13:12:04
