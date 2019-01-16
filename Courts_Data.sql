-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 21, 2018 at 11:26 PM
-- Server version: 5.7.23-0ubuntu0.16.04.1
-- PHP Version: 7.0.32-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Courts_Data`
--

-- --------------------------------------------------------

--
-- Table structure for table `Appellate_Tribunal`
--
-- Creation: Oct 21, 2018 at 05:43 PM
--

CREATE TABLE `Appellate_Tribunal` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) NOT NULL,
  `date_of_order` varchar(100) DEFAULT NULL,
  `appellant` text,
  `respondent` text,
  `appeal_type` varchar(100) DEFAULT NULL,
  `pdf_file` text,
  `pdf_filename` text,
  `pdf_data` longtext CHARACTER SET utf8mb4,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Arunachal_Pradesh`
--
-- Creation: Oct 21, 2018 at 05:43 PM
--

CREATE TABLE `Arunachal_Pradesh` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `subject` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Bombay`
--
-- Creation: Oct 21, 2018 at 05:44 PM
--

CREATE TABLE `Bombay` (
  `id` int(11) NOT NULL,
  `m_sideflg` varchar(200) DEFAULT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `coram` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Calcutta`
--
-- Creation: Oct 21, 2018 at 05:44 PM
--

CREATE TABLE `Calcutta` (
  `id` int(11) NOT NULL,
  `court_id` int(11) DEFAULT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `judgment_date` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Chattisgarh`
--
-- Creation: Oct 21, 2018 at 05:45 PM
--

CREATE TABLE `Chattisgarh` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `text_data` longtext CHARACTER SET latin1,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Customs_Excise_And_Service_Tax_Appellate_Tribunal`
--
-- Creation: Oct 21, 2018 at 05:45 PM
--

CREATE TABLE `Customs_Excise_And_Service_Tax_Appellate_Tribunal` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) NOT NULL,
  `bench_code` varchar(1000) DEFAULT NULL,
  `petitioner` text,
  `respondent` text,
  `judge_name` text,
  `judgment_date` text,
  `pdf_file` text,
  `pdf_filename` text,
  `pdf_data` longtext CHARACTER SET utf8mb4,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Delhi`
--
-- Creation: Oct 21, 2018 at 05:46 PM
--

CREATE TABLE `Delhi` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `corrigendum` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Gauhati`
--
-- Creation: Oct 21, 2018 at 05:47 PM
--

CREATE TABLE `Gauhati` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `subject` text CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` text CHARACTER SET latin1,
  `pdf_data` text CHARACTER SET latin1,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Goa`
--
-- Creation: Oct 21, 2018 at 05:47 PM
--

CREATE TABLE `Goa` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge` text CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` text CHARACTER SET latin1,
  `pdf_data` text CHARACTER SET latin1,
  `reportable` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Himachal_Pradesh`
--
-- Creation: Oct 21, 2018 at 05:48 PM
--

CREATE TABLE `Himachal_Pradesh` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `judgment_date` text CHARACTER SET latin1,
  `coram` text CHARACTER SET latin1,
  `type` text CHARACTER SET latin1,
  `status` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Hyderabad`
--
-- Creation: Oct 21, 2018 at 05:48 PM
--

CREATE TABLE `Hyderabad` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `text_data` longtext CHARACTER SET latin1,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Income_Tax_Appellate`
--
-- Creation: Oct 21, 2018 at 05:54 PM
--

CREATE TABLE `Income_Tax_Appellate` (
  `id` int(11) NOT NULL,
  `appeal_no` varchar(500) NOT NULL,
  `appellant` text,
  `respondent` text,
  `date_of_order` text,
  `filed_by` text,
  `pdf_file` text,
  `pdf_data` longtext,
  `pdf_filename` text,
  `bench_code` varchar(100) DEFAULT NULL,
  `filed_on` varchar(100) DEFAULT NULL,
  `assessment_year` varchar(100) DEFAULT NULL,
  `bench_allotted` varchar(100) DEFAULT NULL,
  `case_status` varchar(500) DEFAULT NULL,
  `order_type` text,
  `date_of_first_hearing` varchar(100) DEFAULT NULL,
  `date_of_last_hearing` varchar(100) DEFAULT NULL,
  `date_of_next_hearing` varchar(100) DEFAULT NULL,
  `date_of_final_hearing` varchar(100) DEFAULT NULL,
  `date_of_tribunal_order` varchar(100) DEFAULT NULL,
  `date_of_pronouncement` varchar(100) DEFAULT NULL,
  `order_result` text,
  `is_json` tinyint(1) NOT NULL DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Jammu_Srinagar`
--
-- Creation: Oct 21, 2018 at 05:49 PM
--

CREATE TABLE `Jammu_Srinagar` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `corrigendum` text,
  `text_data` longtext CHARACTER SET latin1,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Karnataka`
--
-- Creation: Oct 21, 2018 at 05:49 PM
--

CREATE TABLE `Karnataka` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `bench` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Kerala`
--
-- Creation: Oct 21, 2018 at 05:49 PM
--

CREATE TABLE `Kerala` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `text_data` longtext CHARACTER SET latin1,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Madhya_Pradesh`
--
-- Creation: Oct 21, 2018 at 05:49 PM
--

CREATE TABLE `Madhya_Pradesh` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `petitioner_advocate` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `respondent_advocate` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `disposal_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `bench` varchar(5) CHARACTER SET latin1 DEFAULT NULL,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Madras`
--
-- Creation: Oct 21, 2018 at 05:40 PM
--

CREATE TABLE `Madras` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `text_data` longtext CHARACTER SET latin1,
  `text_file` text CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Manipur`
--
-- Creation: Oct 21, 2018 at 05:50 PM
--

CREATE TABLE `Manipur` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` varchar(200) CHARACTER SET latin1 DEFAULT NULL,
  `judge_name` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Meghalaya`
--
-- Creation: Oct 21, 2018 at 05:50 PM
--

CREATE TABLE `Meghalaya` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `corrigendum` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Mizoram`
--
-- Creation: Oct 21, 2018 at 05:50 PM
--

CREATE TABLE `Mizoram` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text,
  `pdf_data` longtext,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Nagaland`
--
-- Creation: Oct 21, 2018 at 05:50 PM
--

CREATE TABLE `Nagaland` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `judgment_date` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `National_Company_Law_Tribunal`
--
-- Creation: Oct 21, 2018 at 05:51 PM
--

CREATE TABLE `National_Company_Law_Tribunal` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) NOT NULL,
  `date_of_order` varchar(50) DEFAULT NULL,
  `description` text,
  `section` varchar(1000) DEFAULT NULL,
  `bench_code` varchar(500) DEFAULT NULL,
  `pdf_file` text,
  `pdf_filename` text,
  `pdf_data` longtext,
  `is_json` tinyint(1) DEFAULT NULL,
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Orissa`
--
-- Creation: Oct 21, 2018 at 05:51 PM
--

CREATE TABLE `Orissa` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `corrigendum` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Punjab_Haryana`
--
-- Creation: Oct 21, 2018 at 05:51 PM
--

CREATE TABLE `Punjab_Haryana` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Sikkim`
--
-- Creation: Oct 21, 2018 at 05:51 PM
--

CREATE TABLE `Sikkim` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Supreme_Court`
--
-- Creation: Oct 21, 2018 at 05:52 PM
--

CREATE TABLE `Supreme_Court` (
  `id` int(11) NOT NULL,
  `diary_number` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `petitioner_advocate` varchar(500) CHARACTER SET latin1 DEFAULT NULL,
  `respondent_advocate` varchar(500) CHARACTER SET latin1 DEFAULT NULL,
  `judgment_date` text CHARACTER SET latin1,
  `bench` mediumtext CHARACTER SET latin1,
  `judge_name` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `Tracker`
--
-- Creation: Aug 21, 2018 at 07:40 PM
-- Last update: Oct 21, 2018 at 01:04 PM
--

CREATE TABLE `Tracker` (
  `id` int(11) NOT NULL,
  `Name` varchar(500) DEFAULT NULL,
  `bench` varchar(50) DEFAULT NULL,
  `No_Cases` int(11) DEFAULT NULL,
  `Start_Date` varchar(40) DEFAULT NULL,
  `End_Date` varchar(40) DEFAULT NULL,
  `No_Error` int(11) DEFAULT NULL,
  `No_Year_Error` int(11) DEFAULT NULL,
  `No_Year_NoData` int(11) DEFAULT NULL,
  `emergency_exit` tinyint(1) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Tracker`
--

INSERT INTO `Tracker` (`id`, `Name`, `bench`, `No_Cases`, `Start_Date`, `End_Date`, `No_Error`, `No_Year_Error`, `No_Year_NoData`, `emergency_exit`, `status`) VALUES
(1, 'Arunachal_Pradesh', '0', 0, 'oct11', 'Sep18', 31, 0, 0, 1, 'IN_SUCCESS'),
(2, 'Bombay', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 0, 'IN_FAILED'),
(3, 'Calcutta', '3', 5253, '07/04/2018', '04/10/2018', 0, 0, 35, 0, 'IN_BUCKET_TRANSFER'),
(4, 'Chattisgarh', 'None', 0, '30/11/2017', '29/05/2018', 0, 0, 10, 1, 'IN_SUCCESS'),
(5, 'Delhi', 'None', 3, '03/01/2018', '04/01/2018', 0, 1, 7, 1, 'IN_FAILED'),
(6, 'Himachal_Pradesh', '0', 4987, '03-09-2018', '04-09-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(7, 'Hyderabad', '0', 28, '01/08/2018', '28/01/2019', 0, 0, 0, 1, 'IN_SUCCESS'),
(8, 'Jammu_Srinagar', '3', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(9, 'Karnataka', 'None', 0, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(10, 'Kerala', '0', 4608, '30/06/2018', '27/12/2018', 1, 0, 0, 1, 'IN_SUCCESS'),
(11, 'Madhya_Pradesh', 'None', 0, '08-09-2000', '09-09-2000', 0, 1, 228, 1, 'IN_FAILED'),
(12, 'Madras', '0', 0, '01/07/2017', '28/12/2017', 0, 0, 0, 1, 'IN_ABORT'),
(13, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(14, 'Mizoram', '0', 0, 'Feb2018', 'Aug2018', 0, 0, 0, 1, 'IN_ABORT'),
(15, 'Nagaland', '0', 884, '012010', '04/09/2018', 0, 0, 41, 1, 'IN_SUCCESS'),
(16, 'Orissa', 'None', 29, '31/12/2005', '01/01/2006', 0, 0, 237, 1, 'IN_SUCCESS'),
(17, 'Punjab_Haryana', 'None', 0, '09/02/2000', '10/02/2000', 0, 1, 0, 1, 'IN_FAILED'),
(18, 'Sikkim', 'None', 38, '1213', '1213', 0, 0, 0, 1, 'IN_SUCCESS'),
(19, 'Supreme_Court', 'None', 180, '01-01-2009', '30-06-2009', 0, 0, 0, 1, 'IN_SUCCESS'),
(20, 'Uttaranchal', 'None', 299, '12/01/2018', '13/01/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(21, 'Meghalaya', 'None', 0, '31/12/2010', '01/01/2011', 0, 0, 159, 1, 'IN_SUCCESS'),
(22, 'Goa', 'None', 104, '01-01-2006', '02-01-2006', 0, 0, 240, 1, 'IN_SUCCESS'),
(23, 'Gauhati', '0', 5948, 'Dec17', 'Dec17', 10, 0, 0, 1, 'IN_SUCCESS'),
(24, 'Income_Tax_Appellate', '201', 53, '07/09/2018', '08/09/2018', 0, 0, 0, 0, 'IN_RUNNING'),
(25, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', 'Mumbai', 199, '2018-08-30', '2018-09-29', 0, 0, 0, 1, 'IN_SUCCESS'),
(26, 'National_Company_Law_Tribunal', 'Principal_Bench_New Delhi_Bench', 88, '2014', '2014', 1, 0, 0, 1, 'IN_BUCKET_TRANSFER'),
(27, 'Appellate_Tribunal', 'None', 86, '062017', '062017', 0, 0, 245, 1, 'IN_ABORT');

-- --------------------------------------------------------

--
-- Table structure for table `Tracker_History`
--
-- Creation: Aug 21, 2018 at 07:40 PM
-- Last update: Oct 21, 2018 at 12:33 PM
--

CREATE TABLE `Tracker_History` (
  `id` int(11) NOT NULL,
  `Name` varchar(500) DEFAULT NULL,
  `bench` varchar(50) DEFAULT NULL,
  `No_Cases` int(11) DEFAULT NULL,
  `Start_Date` varchar(40) DEFAULT NULL,
  `End_Date` varchar(40) DEFAULT NULL,
  `No_Error` int(11) DEFAULT NULL,
  `No_Year_Error` int(11) DEFAULT NULL,
  `No_Year_NoData` int(11) DEFAULT NULL,
  `emergency_exit` tinyint(1) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Tracker_History`
--

INSERT INTO `Tracker_History` (`id`, `Name`, `bench`, `No_Cases`, `Start_Date`, `End_Date`, `No_Error`, `No_Year_Error`, `No_Year_NoData`, `emergency_exit`, `status`) VALUES
(2, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(3, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(4, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(5, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(6, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(7, 'Manipur', '0', 30, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(8, 'Manipur', '0', 40, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(9, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(10, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(11, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(12, 'Manipur', '0', 13, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(13, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(14, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(15, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 1, 'IN_FAILED'),
(16, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(17, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(18, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(19, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(20, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(21, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(22, 'Manipur', '0', 36, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(23, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 2, 0, 0, 1, 'IN_SUCCESS'),
(24, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 1, 'IN_FAILED'),
(25, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 1, 'IN_FAILED'),
(26, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 2, 0, 0, 1, 'IN_SUCCESS'),
(27, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 2, 0, 0, 1, 'IN_SUCCESS'),
(28, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 2, 0, 0, 1, 'IN_SUCCESS'),
(29, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(30, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(31, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(32, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(33, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(34, 'Chattisgarh', '0', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(35, 'Hyderabad', '0', 5, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_ABORT'),
(36, 'Hyderabad', '0', 19, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_ABORT'),
(37, 'Hyderabad', '0', 8, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_ABORT'),
(38, 'Hyderabad', '0', 4, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_ABORT'),
(39, 'Jammu_Srinagar', '0', 4, '01/01/2017', '30/06/2017', 0, 0, 0, 1, 'IN_ABORT'),
(40, 'Jammu_Srinagar', '0', 11, '01/01/2017', '30/06/2017', 0, 0, 0, 1, 'IN_ABORT'),
(41, 'Kerala', '0', 0, '01/01/2017', '30/06/2017', 0, 0, 0, 1, 'IN_ABORT'),
(42, 'Delhi', '0', 0, '08/04/2018', '09/04/2018', 0, 0, 98, 1, 'IN_ABORT'),
(43, 'Delhi', '0', 0, '17/03/2017', '18/03/2017', 0, 0, 3, 1, 'IN_SUCCESS'),
(44, 'Delhi', '0', 0, '17/03/2017', '18/03/2017', 0, 0, 3, 1, 'IN_SUCCESS'),
(45, 'Delhi', '0', 24, '15/03/2017', '16/03/2017', 0, 0, 0, 1, 'IN_ABORT'),
(46, 'Delhi', '0', 0, '16/03/2017', '17/03/2017', 0, 0, 2, 1, 'IN_ABORT'),
(47, 'Delhi', '0', 0, '17/03/2017', '18/03/2017', 0, 0, 3, 1, 'IN_SUCCESS'),
(48, 'Bombay', '0', 32, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(49, 'Bombay', '0', 34, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(50, 'Bombay', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 1, 'IN_FAILED'),
(51, 'Bombay', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 1, 'IN_FAILED'),
(52, 'Bombay', '0', 0, '01-01-2018', '30-06-2018', 0, 2, 0, 1, 'IN_FAILED'),
(53, 'Bombay', '0', 2, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(54, 'Calcutta', '0', 42, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_ABORT'),
(55, 'Karnataka', '0', 16, '2014', '2014', 0, 0, 0, 1, 'IN_ABORT'),
(56, 'Karnataka', '0', 16, '2014', '2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(57, 'Karnataka', '0', 16, '2014', '2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(58, 'Arunachal_Pradesh', '0', 163, 'Dec17', 'Mar18', 1, 0, 0, 1, 'IN_SUCCESS'),
(59, 'Arunachal_Pradesh', '0', 0, 'Jan18', 'Mar18', 1, 0, 0, 1, 'IN_SUCCESS'),
(60, 'Arunachal_Pradesh', '0', 0, 'Jan18', 'Mar18', 1, 0, 0, 1, 'IN_SUCCESS'),
(61, 'Himachal_Pradesh', '0', 15, '04-01-2018', '05-01-2018', 0, 0, 0, 1, 'IN_ABORT'),
(62, 'Himachal_Pradesh', '0', 23, '04-01-2018', '05-01-2018', 0, 0, 0, 1, 'IN_ABORT'),
(63, 'Madhya_Pradesh', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(64, 'Madhya_Pradesh', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(65, 'Madhya_Pradesh', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(66, 'Madhya_Pradesh', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(67, 'Madhya_Pradesh', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(68, 'Madhya_Pradesh', '0', 31, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(69, 'Mizoram', '0', 32, 'Jan2018', 'Mar2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(70, 'Mizoram', '0', 8, 'Jan2018', 'Mar2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(71, 'Mizoram', '0', 32, 'Jan2018', 'Mar2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(72, 'Mizoram', '0', 8, 'Jan2018', 'Jan2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(73, 'Mizoram', '0', 8, 'Jan2018', 'Jan2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(74, 'Nagaland', '0', 0, '01-2018', '01/03/2018', 3, 0, 0, 1, 'IN_SUCCESS'),
(75, 'Nagaland', '0', 0, '01-2018', '01/03/2018', 3, 0, 0, 1, 'IN_SUCCESS'),
(76, 'Nagaland', '0', 0, '01-2018', '01/03/2018', 3, 0, 0, 1, 'IN_SUCCESS'),
(77, 'Nagaland', '0', 0, '01-2018', '01/03/2018', 0, 0, 3, 1, 'IN_SUCCESS'),
(78, 'Nagaland', '0', 6, '012018', '01/03/2018', 0, 0, 1, 1, 'IN_SUCCESS'),
(79, 'Nagaland', '0', 6, '012018', '01/03/2018', 0, 0, 1, 1, 'IN_SUCCESS'),
(80, 'Punjab_Haryana', '0', 8, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(81, 'Sikkim', '0', 0, '0118', '0318', 0, 1, 0, 1, 'IN_FAILED'),
(82, 'Sikkim', '0', 0, '0118', '0318', 0, 1, 0, 1, 'IN_FAILED'),
(83, 'Sikkim', '0', 0, '0118', '0318', 0, 1, 0, 1, 'IN_FAILED'),
(84, 'Sikkim', '0', 16, '0118', '0318', 0, 0, 0, 1, 'IN_SUCCESS'),
(85, 'Supreme_Court', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(86, 'Supreme_Court', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(87, 'Supreme_Court', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(88, 'Orissa', '0', 0, '01/01/2018', '30/06/2018', 0, 0, 1, 1, 'IN_SUCCESS'),
(89, 'Uttaranchal', '0', 49, '15/03/2018', '16/03/2018', 0, 0, 0, 1, 'IN_ABORT'),
(90, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(91, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(92, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(93, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(94, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(95, 'Manipur', '0', 0, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(96, 'Delhi', '0', 0, '16/01/2018', '17/01/2018', 0, 0, 16, 1, 'IN_ABORT'),
(97, 'Calcutta', '0', 5540, '01/01/2018', '30/06/2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(98, 'Bombay', '0', 0, '01-01-2018', '30-06-2018', 0, 1, 0, 1, 'IN_FAILED'),
(99, 'Madras', '0', 0, '01/03/1979', '28/08/1979', 0, 1, 59, 1, 'IN_FAILED'),
(100, 'Madras', '0', 0, '26/07/1980', '22/01/1981', 0, 0, 3, 1, 'IN_ABORT'),
(101, 'Madras', '0', 21042, '29/01/2014', '28/07/2014', 0, 0, 42, 1, 'IN_ABORT'),
(102, 'Madras', '0', 0, '12/01/2017', '11/07/2017', 0, 0, 0, 1, 'IN_ABORT'),
(103, 'Madras', '0', 0, '12/01/2017', '11/07/2017', 0, 0, 0, 1, 'IN_ABORT'),
(104, 'Delhi', '0', 0, '30/08/1961', '31/08/1961', 0, 1, 4259, 1, 'IN_FAILED'),
(105, 'Delhi', '0', 0, '12/10/2008', '13/10/2008', 0, 0, 3208, 1, 'IN_ABORT'),
(106, 'Karnataka', '0', 133, '2018', '2018', 0, 0, 0, 1, 'IN_CANCELLED'),
(107, 'Karnataka', '0', 133, '2018', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(108, 'Uttaranchal', '0', 290, '27/08/2018', '28/08/2018', 0, 0, 11, 1, 'IN_SUCCESS'),
(109, 'Sikkim', '0', 16, '0818', '0818', 0, 0, 0, 1, 'IN_SUCCESS'),
(110, 'Punjab_Haryana', '0', 0, '01/08/2018', '28/01/2019', 1, 0, 0, 1, 'IN_SUCCESS'),
(111, 'Punjab_Haryana', '0', 0, '30/06/2018', '27/12/2018', 2, 0, 0, 1, 'IN_SUCCESS'),
(112, 'Orissa', '0', 0, '01/08/2018', '28/01/2019', 0, 0, 1, 1, 'IN_SUCCESS'),
(113, 'Orissa', '0', 0, '01/08/2018', '28/01/2019', 0, 0, 1, 1, 'IN_SUCCESS'),
(114, 'Orissa', '0', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(115, 'Nagaland', '0', 29, '012018', '27/08/2018', 0, 0, 1, 1, 'IN_SUCCESS'),
(116, 'Mizoram', '0', 93, 'Jan2018', 'Aug2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(117, 'Manipur', '0', 0, '30-06-2018', '27-12-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(118, 'Madhya_Pradesh', '0', 0, '01-08-2018', '28-01-2019', 0, 0, 3, 1, 'IN_SUCCESS'),
(119, 'Mizoram', '0', 0, 'Feb2018', 'Aug2018', 0, 0, 0, 1, 'IN_ABORT'),
(120, 'Kerala', '0', 2209, '30/06/2018', '27/12/2018', 1, 1, 0, 1, 'IN_FAILED'),
(121, 'Kerala', '0', 4608, '30/06/2018', '27/12/2018', 1, 0, 0, 1, 'IN_SUCCESS'),
(122, 'Supreme_Court', '0', 1943, '26-11-2010', '25-05-2011', 0, 0, 0, 1, 'IN_ABORT'),
(123, 'Arunachal_Pradesh', '0', 0, 'Aug18', 'Aug18', 1, 0, 0, 1, 'IN_SUCCESS'),
(124, 'Arunachal_Pradesh', '0', 234, 'mar18', 'Aug18', 1, 0, 0, 1, 'IN_ABORT'),
(125, 'Madhya_Pradesh', '0', 1, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(126, 'Orissa', '0', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(127, 'Delhi', '0', 0, '20/01/2018', '21/01/2018', 0, 0, 20, 1, 'IN_ABORT'),
(128, 'Chattisgarh', '0', 0, '01/08/2018', '28/01/2019', 0, 0, 1, 1, 'IN_SUCCESS'),
(129, 'Chattisgarh', '0', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(130, 'Arunachal_Pradesh', '0', 4, 'Dec17', 'Dec17', 0, 0, 0, 1, 'IN_SUCCESS'),
(131, 'Himachal_Pradesh', '0', 57, '31-01-2018', '01-02-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(132, 'Hyderabad', '0', 28, '01/08/2018', '28/01/2019', 0, 0, 0, 1, 'IN_SUCCESS'),
(133, 'Jammu_Srinagar', '0', 0, '01/08/2018', '28/01/2019', 0, 0, 1, 1, 'IN_SUCCESS'),
(134, 'Jammu_Srinagar', '0', 0, '01/08/2018', '28/01/2019', 0, 0, 1, 1, 'IN_SUCCESS'),
(135, 'Karnataka', '0', 816, '2018', '2018', 1, 0, 0, 1, 'IN_SUCCESS'),
(136, 'Arunachal_Pradesh', '0', 359, 'Jan90', 'Aug18', 299, 0, 0, 1, 'IN_SUCCESS'),
(137, 'Madras', '0', 4253, '28/07/2014', '24/01/2015', 0, 0, 0, 1, 'IN_ABORT'),
(138, 'Supreme_Court', '0', 1270, '19-05-2012', '15-11-2012', 0, 0, 0, 1, 'IN_ABORT'),
(139, 'Jammu_Srinagar', '0', 3, '01/01/2015', '30/06/2015', 0, 0, 0, 1, 'IN_ABORT'),
(140, 'Jammu_Srinagar', '0', 4, '01/01/2015', '30/06/2015', 0, 0, 0, 1, 'IN_ABORT'),
(141, 'Delhi', '0', 0, '13/01/2018', '14/01/2018', 0, 0, 13, 1, 'IN_ABORT'),
(142, 'Jammu_Srinagar', '0', 1674, '03/07/2018', '30/12/2018', 0, 0, 113, 1, 'IN_SUCCESS'),
(143, 'Jammu_Srinagar', '0', 1278, '03/07/2018', '30/12/2018', 0, 0, 119, 1, 'IN_SUCCESS'),
(144, 'Supreme_Court', '0', 6010, '18-04-2018', '15-10-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(145, 'Madras', '0', 6906, '24/01/2015', '23/07/2015', 1, 0, 0, 1, 'IN_ABORT'),
(146, 'Madras', '0', 1779, '24/01/2015', '23/07/2015', 0, 0, 0, 1, 'IN_ABORT'),
(147, 'Orissa', '0', 0, '14/06/2018', '11/12/2018', 0, 0, 8, 1, 'IN_SUCCESS'),
(148, 'Orissa', '0', 0, '14/06/2018', '11/12/2018', 0, 0, 8, 1, 'IN_SUCCESS'),
(149, 'Himachal_Pradesh', '0', 0, '18-02-1990', '19-02-1990', 0, 0, 0, 1, 'IN_ABORT'),
(150, 'Orissa', '0', 0, '16/03/2017', '17/03/2017', 0, 0, 3, 1, 'IN_SUCCESS'),
(151, 'Meghalaya', '0', 74, '16/03/2017', '17/03/2017', 0, 0, 0, 1, 'IN_SUCCESS'),
(152, 'Punjab_Haryana', '0', 0, '14/02/2017', '15/02/2017', 11, 0, 0, 1, 'IN_ABORT'),
(153, 'Himachal_Pradesh', '0', 0, '11-11-1991', '12-11-1991', 0, 0, 0, 1, 'IN_ABORT'),
(154, 'Madhya_Pradesh', '0', 0, '21-01-2010', '22-01-2010', 0, 0, 0, 1, 'IN_ABORT'),
(155, 'Madhya_Pradesh', '0', 0, '11-01-2018', '12-01-2018', 0, 0, 0, 1, 'IN_ABORT'),
(156, 'Punjab_Haryana', '0', 0, '04/01/2018', '05/01/2018', 6, 1, 0, 1, 'IN_FAILED'),
(157, 'Himachal_Pradesh', '0', 0, '15-02-2010', '16-02-2010', 0, 0, 0, 1, 'IN_ABORT'),
(158, 'Himachal_Pradesh', '0', 0, '15-02-2010', '16-02-2010', 0, 0, 0, 1, 'IN_ABORT'),
(159, 'Punjab_Haryana', '0', 0, '17/01/2018', '18/01/2018', 10, 2, 0, 1, 'IN_FAILED'),
(160, 'Karnataka', '0', 16, '2000', '2014', 1, 0, 0, 1, 'IN_SUCCESS'),
(161, 'Karnataka', '0', 16, '2014', '2018', 1, 1, 0, 1, 'IN_FAILED'),
(162, 'Sikkim', '0', 0, '01/01/2000', '01/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(163, 'Sikkim', '0', 0, '01/01/2000', '01/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(164, 'Sikkim', '0', 0, '01/01/2000', '01/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(165, 'Uttaranchal', '0', 4, '05/10/2001', '06/10/2001', 0, 0, 397, 1, 'IN_ABORT'),
(166, 'Uttaranchal', '0', 0, '03/09/2000', '04/09/2000', 0, 0, 3, 1, 'IN_ABORT'),
(167, 'Uttaranchal', '0', 2864, '16/10/2012', '17/10/2012', 0, 0, 840, 1, 'IN_ABORT'),
(168, 'Madhya_Pradesh', '0', 0, '04-02-2018', '05-02-2018', 0, 0, 0, 1, 'IN_ABORT'),
(169, 'Punjab_Haryana', '0', 0, '06/01/2018', '07/01/2018', 5, 0, 0, 1, 'IN_ABORT'),
(170, 'Punjab_Haryana', '0', 0, '12/01/2000', '13/01/2000', 0, 0, 0, 1, 'IN_ABORT'),
(171, 'Punjab_Haryana', '0', 0, '09/01/2018', '10/01/2018', 6, 1, 0, 1, 'IN_FAILED'),
(172, 'Himachal_Pradesh', '0', 0, '18-01-2010', '19-01-2010', 0, 0, 0, 1, 'IN_ABORT'),
(173, 'Himachal_Pradesh', '0', 6, '02-01-2017', '03-01-2017', 0, 0, 0, 1, 'IN_ABORT'),
(174, 'Himachal_Pradesh', '0', 0, '21-04-2000', '22-04-2000', 0, 0, 0, 1, 'IN_ABORT'),
(175, 'Punjab_Haryana', '0', 0, '04/01/2018', '05/01/2018', 4, 0, 0, 1, 'IN_ABORT'),
(176, 'Himachal_Pradesh', '0', 5534, '27-02-2016', '28-02-2016', 0, 1, 0, 1, 'IN_FAILED'),
(177, 'Himachal_Pradesh', '0', 0, '28-02-2016', '29-02-2016', 0, 1, 0, 1, 'IN_FAILED'),
(178, 'Meghalaya', '0', 0, '08/01/2000', '09/01/2000', 0, 0, 8, 1, 'IN_ABORT'),
(179, 'Meghalaya', '0', 0, '16/04/2010', '17/04/2010', 0, 0, 106, 1, 'IN_ABORT'),
(180, 'Meghalaya', '0', 0, '11/01/2015', '12/01/2015', 0, 0, 11, 1, 'IN_ABORT'),
(181, 'Meghalaya', '0', 3, '03/03/2018', '04/03/2018', 0, 0, 60, 1, 'IN_ABORT'),
(182, 'Meghalaya', '0', 1, '07/02/2017', '08/02/2017', 0, 0, 0, 1, 'IN_ABORT'),
(183, 'Sikkim', '0', 0, '01/01/2010', '02/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(184, 'Sikkim', '0', 3, '0317', '0918', 0, 0, 0, 1, 'IN_ABORT'),
(185, 'Sikkim', '0', 0, '01/01/2010', '02/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(186, 'Sikkim', '0', 526, '0111', '0918', 0, 0, 0, 1, 'IN_SUCCESS'),
(187, 'Uttaranchal', '0', 4188, '20/11/2013', '21/11/2013', 0, 1, 142, 1, 'IN_FAILED'),
(188, 'Jammu_Srinagar', '0', 1677, '03/07/2018', '30/12/2018', 0, 0, 113, 1, 'IN_SUCCESS'),
(189, 'Jammu_Srinagar', '0', 1282, '27/03/2018', '23/09/2018', 0, 0, 16, 1, 'IN_SUCCESS'),
(190, 'Uttaranchal', '0', 0, '28/03/2016', '29/03/2016', 0, 0, 0, 1, 'IN_ABORT'),
(191, 'Himachal_Pradesh', '0', 4987, '03-09-2018', '04-09-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(192, 'Uttaranchal', '0', 7324, '04/09/2018', '05/09/2018', 0, 0, 252, 1, 'IN_SUCCESS'),
(193, 'Nagaland', '0', 0, '01/01/2000', '04/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(194, 'Nagaland', '0', 10, '052011', '04/09/2018', 0, 0, 12, 1, 'IN_ABORT'),
(195, 'Nagaland', '0', 0, '01/01/2005', '04/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(196, 'Nagaland', '0', 0, '01/01/2008', '04/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(197, 'Nagaland', '0', 0, '01/01/2009', '04/09/2018', 0, 0, 0, 1, 'IN_NO_DATA_FOUND'),
(198, 'Nagaland', '0', 884, '012010', '04/09/2018', 0, 0, 41, 1, 'IN_SUCCESS'),
(199, 'Karnataka', '0', 324, '2005', '2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(200, 'Karnataka', '0', 324, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(201, 'Karnataka', '0', 324, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(202, 'Chattisgarh', '0', 14, '01/01/2010', '30/06/2010', 0, 0, 0, 1, 'IN_ABORT'),
(203, 'Chattisgarh', '0', 9, '01/01/2008', '29/06/2008', 0, 0, 0, 1, 'IN_ABORT'),
(204, 'Chattisgarh', '0', 13, '01/01/2005', '30/06/2005', 0, 0, 0, 1, 'IN_ABORT'),
(205, 'Chattisgarh', '0', 787, '27/03/2018', '23/09/2018', 0, 0, 18, 1, 'IN_SUCCESS'),
(206, 'Madras', '0', 0, '24/01/2015', '23/07/2015', 0, 0, 0, 1, 'IN_ABORT'),
(207, 'Madras', '0', 0, '01/07/2015', '28/12/2015', 0, 0, 0, 1, 'IN_ABORT'),
(208, 'Madras', '0', 0, '01/08/2015', '28/01/2016', 0, 0, 0, 1, 'IN_ABORT'),
(209, 'Madras', '0', 10, '01/09/2018', '28/02/2019', 0, 0, 0, 1, 'IN_ABORT'),
(210, 'Madras', '0', 0, '01/06/2016', '28/11/2016', 0, 0, 0, 1, 'IN_ABORT'),
(211, 'Madras', '0', 0, '01/01/2017', '30/06/2017', 0, 0, 0, 1, 'IN_ABORT'),
(212, 'Meghalaya', '0', 0, '05/09/2018', '06/09/2018', 0, 0, 246, 1, 'IN_SUCCESS'),
(213, 'Madras', '0', 49374, '30/06/2018', '27/12/2018', 2, 0, 0, 1, 'IN_SUCCESS'),
(214, 'Madras', '0', 461, '28/12/2017', '26/06/2018', 1, 1, 0, 1, 'IN_FAILED'),
(215, 'Delhi', '0', 9, '15/03/2017', '16/03/2017', 0, 0, 0, 1, 'IN_ABORT'),
(216, 'Orissa', '0', 5, '15/03/2017', '16/03/2017', 0, 0, 0, 1, 'IN_ABORT'),
(217, 'Meghalaya', '0', 3, '16/03/2017', '17/03/2017', 0, 0, 0, 1, 'IN_SUCCESS'),
(218, 'Madhya_Pradesh', '0', 6, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(219, 'Punjab_Haryana', '0', 0, '01/02/2018', '02/02/2018', 10, 0, 0, 1, 'IN_ABORT'),
(220, 'Delhi', '0', 2549, '13/04/2018', '14/04/2018', 4, 0, 29, 1, 'IN_ABORT'),
(221, 'Delhi', '0', 120, '18/04/2018', '19/04/2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(222, 'Punjab_Haryana', '0', 0, '18/03/2017', '19/03/2017', 1, 0, 0, 1, 'IN_SUCCESS'),
(223, 'Madhya_Pradesh', '0', 452, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_ABORT'),
(224, 'Madhya_Pradesh', '0', 452, '01-01-2018', '30-06-2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(225, 'Orissa', '0', 476, '08/09/2018', '09/09/2018', 0, 0, 657, 1, 'IN_SUCCESS'),
(226, 'Meghalaya', '0', 0, '23/02/2018', '24/02/2018', 0, 0, 54, 1, 'IN_ABORT'),
(227, 'Meghalaya', '0', 0, '23/02/2018', '24/02/2018', 0, 0, 54, 1, 'IN_SUCCESS'),
(228, 'Meghalaya', '0', 0, '15/01/2017', '16/01/2017', 0, 0, 15, 1, 'IN_ABORT'),
(229, 'Meghalaya', '0', 0, '15/01/2017', '16/01/2017', 0, 0, 15, 1, 'IN_SUCCESS'),
(230, 'Madhya_Pradesh', '0', 1179, '28-09-2017', '27-03-2018', 0, 0, 84, 1, 'IN_ABORT'),
(231, 'Delhi', '0', 167, '23/08/2006', '24/08/2006', 0, 0, 4515, 1, 'IN_ABORT'),
(232, 'Punjab_Haryana', '0', 0, '05/01/2018', '06/01/2018', 8, 0, 0, 1, 'IN_ABORT'),
(233, 'Punjab_Haryana', '0', 0, '05/01/2018', '06/01/2018', 9, 0, 0, 1, 'IN_BUCKET_TRANSFER'),
(234, 'Punjab_Haryana', '0', 0, '05/01/2018', '06/01/2018', 9, 0, 0, 1, 'IN_SUCCESS'),
(235, 'Delhi', '0', 550, '21/05/2007', '22/05/2007', 2, 0, 164, 1, 'IN_ABORT'),
(236, 'Delhi', '0', 550, '21/05/2007', '22/05/2007', 2, 0, 164, 1, 'IN_SUCCESS'),
(237, 'Delhi', '0', 4, '22/05/2017', '23/05/2017', 0, 0, 1, 1, 'IN_ABORT'),
(238, 'Delhi', '0', 4, '22/05/2017', '23/05/2017', 0, 0, 1, 1, 'IN_SUCCESS'),
(239, 'Delhi', '0', 854, '22/09/2008', '23/09/2008', 6, 1, 49, 1, 'IN_FAILED'),
(240, 'Delhi', '0', 855, '22/09/2008', '23/09/2008', 6, 1, 49, 1, 'IN_FAILED'),
(241, 'Delhi', '0', 855, '22/09/2008', '23/09/2008', 6, 1, 49, 1, 'IN_SUCCESS'),
(242, 'Delhi', '0', 5217, '05/11/2009', '06/11/2009', 3, 0, 168, 1, 'IN_ABORT'),
(243, 'Delhi', '0', 743, '14/12/2009', '15/12/2009', 0, 0, 11, 1, 'IN_SUCCESS'),
(244, 'Delhi', '0', 744, '14/12/2009', '15/12/2009', 0, 0, 11, 1, 'IN_SUCCESS'),
(245, 'Delhi', '0', 744, '14/12/2009', '15/12/2009', 0, 0, 11, 1, 'IN_SUCCESS'),
(246, 'Delhi', '0', 17822, '31/08/2012', '01/09/2012', 24, 0, 370, 1, 'IN_ABORT'),
(247, 'Goa', '0', 2, '14-03-2017', '10-09-2017', 0, 0, 0, 1, 'IN_SUCCESS'),
(248, 'Goa', '0', 8, '16-03-2017', '17-03-2017', 1, 0, 0, 1, 'IN_SUCCESS'),
(249, 'Delhi', '0', 1, '31/08/2012', '01/09/2012', 0, 0, 0, 1, 'IN_ABORT'),
(250, 'Delhi', '0', 2665, '06/02/2013', '07/02/2013', 8, 0, 64, 1, 'IN_SUCCESS'),
(251, 'Delhi', '0', 2665, '06/02/2013', '07/02/2013', 8, 0, 64, 1, 'IN_SUCCESS'),
(252, 'Delhi', '0', 264, '19/02/2013', '20/02/2013', 1, 0, 3, 1, 'IN_SUCCESS'),
(253, 'Delhi', '0', 265, '19/02/2013', '20/02/2013', 1, 0, 3, 1, 'IN_SUCCESS'),
(254, 'Delhi', '0', 265, '19/02/2013', '20/02/2013', 1, 0, 3, 1, 'IN_SUCCESS'),
(255, 'Delhi', '0', 5581, '05/01/2014', '06/01/2014', 5, 0, 131, 1, 'IN_ABORT'),
(256, 'Goa', '0', 108, '12-09-2018', '13-09-2018', 0, 0, 141, 1, 'IN_SUCCESS'),
(257, 'Goa', '0', 4, '20-02-1995', '21-02-1995', 0, 0, 40, 1, 'IN_ABORT'),
(258, 'Goa', '0', 4, '20-02-1995', '21-02-1995', 0, 0, 40, 1, 'IN_SUCCESS'),
(259, 'Delhi', '0', 5581, '05/01/2014', '06/01/2014', 5, 0, 131, 1, 'IN_SUCCESS'),
(260, 'Goa', '0', 643, '31-01-1998', '01-02-1998', 0, 0, 615, 1, 'IN_SUCCESS'),
(261, 'Goa', '0', 417, '13-08-1999', '14-08-1999', 0, 0, 296, 1, 'IN_ABORT'),
(262, 'Goa', '0', 417, '13-08-1999', '14-08-1999', 0, 0, 296, 1, 'IN_SUCCESS'),
(263, 'Delhi', '0', 2184, '01/05/2014', '02/05/2014', 3, 0, 42, 1, 'IN_ABORT'),
(264, 'Delhi', '0', 39, '05/05/2014', '06/05/2014', 0, 0, 1, 1, 'IN_ABORT'),
(265, 'Arunachal_Pradesh', '0', 0, 'oct11', 'Sep18', 31, 0, 0, 1, 'IN_ABORT'),
(266, 'Arunachal_Pradesh', '0', 0, 'oct11', 'Sep18', 31, 0, 0, 1, 'IN_SUCCESS'),
(267, 'Delhi', '0', 322, '21/05/2014', '22/05/2014', 1, 0, 6, 1, 'IN_SUCCESS'),
(268, 'Delhi', '0', 323, '21/05/2014', '22/05/2014', 1, 0, 6, 1, 'IN_SUCCESS'),
(269, 'Delhi', '0', 323, '21/05/2014', '22/05/2014', 1, 0, 6, 1, 'IN_SUCCESS'),
(270, 'Delhi', '0', 0, '21/05/2014', '22/05/2014', 0, 0, 0, 1, 'IN_ABORT'),
(271, 'Delhi', '0', 0, '21/05/2014', '22/05/2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(272, 'Gauhati', '0', 187, 'Feb12', 'Dec17', 20, 0, 0, 1, 'IN_ABORT'),
(273, 'Gauhati', '0', 1, 'September10', 'Dec17', 8, 0, 0, 1, 'IN_ABORT'),
(274, 'Gauhati', '0', 1, 'September10', 'Dec17', 8, 0, 0, 1, 'IN_SUCCESS'),
(275, 'Gauhati', '0', 21, 'Feb11', 'Dec17', 10, 0, 0, 1, 'IN_ABORT'),
(276, 'Gauhati', '0', 21, 'Feb11', 'Dec17', 10, 0, 0, 1, 'IN_SUCCESS'),
(277, 'Gauhati', '0', 0, 'Jun10', 'Dec17', 5, 0, 0, 1, 'IN_ABORT'),
(278, 'Gauhati', '0', 0, 'Jun10', 'Dec17', 5, 0, 0, 1, 'IN_SUCCESS'),
(279, 'Gauhati', '0', 0, 'August10', 'Dec17', 6, 0, 0, 1, 'IN_ABORT'),
(280, 'Gauhati', '0', 0, 'August10', 'Dec17', 6, 0, 0, 1, 'IN_SUCCESS'),
(281, 'Gauhati', '0', 0, 'Sep18', 'Sep18', 9, 0, 0, 1, 'IN_SUCCESS'),
(282, 'Delhi', '0', 2806, '03/11/2014', '04/11/2014', 5, 0, 73, 1, 'IN_ABORT'),
(283, 'Gauhati', '0', 49, 'Mar11', 'Dec17', 2, 0, 0, 1, 'IN_ABORT'),
(284, 'Gauhati', '0', 49, 'Mar11', 'Dec17', 2, 0, 0, 1, 'IN_SUCCESS'),
(285, 'Gauhati', '0', 19, 'July10', 'Dec17', 0, 0, 0, 1, 'IN_ABORT'),
(286, 'Gauhati', '0', 19, 'July10', 'Dec17', 0, 0, 0, 1, 'IN_SUCCESS'),
(287, 'Gauhati', '0', 0, 'October10', 'Dec17', 9, 0, 0, 1, 'IN_ABORT'),
(288, 'Gauhati', '0', 0, 'October10', 'Dec17', 9, 0, 0, 1, 'IN_SUCCESS'),
(289, 'Gauhati', '0', 39, 'Feb11', 'Dec17', 2, 0, 0, 1, 'IN_ABORT'),
(290, 'Gauhati', '0', 39, 'Feb11', 'Dec17', 2, 0, 0, 1, 'IN_SUCCESS'),
(291, 'Gauhati', '0', 24, 'August10', 'Dec17', 0, 0, 0, 1, 'IN_ABORT'),
(292, 'Gauhati', '0', 24, 'August10', 'Dec17', 0, 0, 0, 1, 'IN_SUCCESS'),
(293, 'Gauhati', '0', 88, 'Mar11', 'Dec17', 2, 0, 0, 1, 'IN_ABORT'),
(294, 'Gauhati', '0', 2, 'Mar11', 'Dec17', 2, 0, 0, 1, 'IN_SUCCESS'),
(295, 'Gauhati', '0', 3, 'Mar11', 'Dec17', 2, 0, 0, 1, 'IN_SUCCESS'),
(296, 'Gauhati', '0', 3, 'Mar11', 'Dec17', 2, 0, 0, 1, 'IN_SUCCESS'),
(297, 'Gauhati', '0', 50, 'Mar12', 'Dec17', 0, 1, 0, 1, 'IN_FAILED'),
(298, 'Gauhati', '0', 51, 'Mar12', 'Dec17', 0, 1, 0, 1, 'IN_FAILED'),
(299, 'Gauhati', '0', 51, 'Mar12', 'Dec17', 0, 1, 0, 1, 'IN_SUCCESS'),
(300, 'Gauhati', '0', 5948, 'Dec17', 'Dec17', 10, 0, 0, 1, 'IN_SUCCESS'),
(301, 'Delhi', '0', 0, '24/03/2014', '25/03/2014', 0, 0, 5, 1, 'IN_ABORT'),
(302, 'Delhi', '0', 0, '24/03/2014', '25/03/2014', 0, 0, 5, 1, 'IN_BUCKET_TRANSFER'),
(303, 'Delhi', '0', 0, '02/07/2014', '03/07/2014', 1, 0, 25, 1, 'IN_ABORT'),
(304, 'Delhi', '0', 23, '15/05/2015', '16/05/2015', 0, 0, 0, 1, 'IN_ABORT'),
(305, 'Delhi', '0', 0, '06/01/2015', '07/01/2015', 0, 0, 4, 1, 'IN_ABORT'),
(306, 'Delhi', '0', 4, '06/04/2015', '07/04/2015', 0, 0, 5, 1, 'IN_ABORT'),
(307, 'Delhi', '0', 39, '29/05/2014', '30/05/2014', 0, 0, 0, 1, 'IN_ABORT'),
(308, 'Delhi', '0', 0, '03/01/2014', '04/01/2014', 0, 0, 1, 1, 'IN_ABORT'),
(309, 'Delhi', '0', 17, '10/03/2015', '11/03/2015', 1, 0, 3, 1, 'IN_SUCCESS'),
(310, 'Delhi', '0', 18, '10/03/2015', '11/03/2015', 1, 0, 3, 1, 'IN_SUCCESS'),
(311, 'Delhi', '0', 18, '10/03/2015', '11/03/2015', 1, 0, 3, 1, 'IN_SUCCESS'),
(312, 'Delhi', '0', 18, '10/03/2015', '11/03/2015', 1, 0, 3, 1, 'IN_SUCCESS'),
(313, 'Delhi', '0', 18, '10/03/2015', '11/03/2015', 1, 0, 3, 1, 'IN_SUCCESS'),
(314, 'Delhi', '0', 1011, '21/04/2015', '22/04/2015', 3, 1, 18, 1, 'IN_FAILED'),
(315, 'Delhi', '0', 0, '21/04/2018', '22/04/2018', 0, 0, 0, 1, 'IN_ABORT'),
(316, 'Delhi', '0', 0, '21/04/2018', '22/04/2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(317, 'Delhi', '0', 1082, '11/01/2017', '12/01/2017', 0, 1, 44, 1, 'IN_FAILED'),
(318, 'Delhi', '0', 1082, '11/01/2017', '12/01/2017', 0, 1, 44, 1, 'IN_FAILED'),
(319, 'Delhi', '0', 1083, '11/01/2017', '12/01/2017', 0, 1, 44, 1, 'IN_BUCKET_TRANSFER'),
(320, 'Delhi', '0', 1083, '11/01/2017', '12/01/2017', 0, 1, 44, 1, 'IN_SUCCESS'),
(321, 'Delhi', '0', 1485, '14/03/2017', '15/03/2017', 0, 0, 20, 1, 'IN_ABORT'),
(322, 'Karnataka', '0', 0, '1999', '2013', 0, 0, 0, 1, 'IN_SUCCESS'),
(323, 'Karnataka', '0', 0, '1999', '2013', 0, 0, 0, 1, 'IN_SUCCESS'),
(324, 'Delhi', '0', 1485, '14/03/2017', '15/03/2017', 0, 0, 20, 1, 'IN_SUCCESS'),
(325, 'Karnataka', '0', 260, '2014', '2014', 0, 0, 0, 1, 'IN_ABORT'),
(326, 'Karnataka', '0', 260, '2014', '2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(327, 'Karnataka', '0', 260, '2014', '2014', 0, 1, 0, 1, 'IN_FAILED'),
(328, 'Uttaranchal', '0', 114, '26/03/2001', '27/03/2001', 0, 0, 408, 1, 'IN_ABORT'),
(329, 'Uttaranchal', '0', 114, '26/03/2001', '27/03/2001', 0, 0, 408, 1, 'IN_SUCCESS'),
(330, 'Karnataka', '0', 611, '2015', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(331, 'Goa', '0', 741, '03-07-2014', '04-07-2014', 0, 0, 779, 1, 'IN_ABORT'),
(332, 'Income_Tax_Appellate', '0', 0, '05/09/2018', '15/09/2018', 0, 1, 0, 1, 'IN_FAILED'),
(333, 'Income_Tax_Appellate', '0', 4, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(334, 'Income_Tax_Appellate', '0', 531, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(335, 'Delhi', '0', 1310, '10/08/2017', '11/08/2017', 0, 0, 53, 1, 'IN_ABORT'),
(336, 'Delhi', '0', 0, '23/08/2017', '24/08/2017', 0, 0, 6, 1, 'IN_SUCCESS'),
(337, 'Delhi', '0', 0, '23/08/2017', '24/08/2017', 0, 0, 6, 1, 'IN_SUCCESS'),
(338, 'Delhi', '0', 0, '23/08/2017', '24/08/2017', 0, 0, 6, 1, 'IN_SUCCESS'),
(339, 'Income_Tax_Appellate', '209', 192, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(340, 'Meghalaya', 'None', 691, '01/09/2014', '02/09/2014', 0, 0, 1703, 1, 'IN_SUCCESS'),
(341, 'Delhi', 'None', 3, '03/01/2018', '04/01/2018', 0, 0, 7, 1, 'IN_ABORT'),
(342, 'Punjab_Haryana', 'None', 353, '01/04/2018', '02/04/2018', 0, 1, 0, 1, 'IN_FAILED'),
(343, 'Delhi', 'None', 3, '03/01/2018', '04/01/2018', 0, 1, 7, 1, 'IN_FAILED'),
(344, 'Punjab_Haryana', 'None', 1124, '01/07/2018', '02/07/2018', 0, 1, 0, 1, 'IN_FAILED'),
(345, 'Punjab_Haryana', 'None', 303, '07/09/2018', '08/09/2018', 0, 1, 0, 1, 'IN_FAILED'),
(346, 'Punjab_Haryana', 'None', 0, '09/09/2018', '10/09/2018', 0, 1, 0, 1, 'IN_FAILED'),
(347, 'Madhya_Pradesh', 'None', 2134, '16-01-2014', '17-01-2014', 0, 0, 0, 1, 'IN_ABORT'),
(348, 'Punjab_Haryana', 'None', 0, '22/01/2018', '23/01/2018', 0, 1, 0, 1, 'IN_FAILED'),
(349, 'Punjab_Haryana', 'None', 0, '12/02/2018', '13/02/2018', 0, 1, 0, 1, 'IN_FAILED'),
(350, 'Madhya_Pradesh', 'None', 1703, '05-02-2014', '06-02-2014', 0, 0, 2, 1, 'IN_ABORT'),
(351, 'Madhya_Pradesh', 'None', 882, '13-02-2014', '14-02-2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(352, 'Madhya_Pradesh', 'None', 882, '13-02-2014', '14-02-2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(353, 'Madhya_Pradesh', 'None', 0, '13-02-2014', '14-02-2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(354, 'Madhya_Pradesh', 'None', 0, '13-02-2014', '14-02-2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(355, 'Madhya_Pradesh', 'None', 0, '13-02-2014', '14-02-2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(356, 'Income_Tax_Appellate', '205', 0, '0', '0', 0, 1, 0, 1, 'IN_FAILED'),
(357, 'Income_Tax_Appellate', '205', 0, '0', '0', 0, 1, 0, 1, 'IN_FAILED'),
(358, 'Income_Tax_Appellate', '207', 1764, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(359, 'Income_Tax_Appellate', '205', 0, '0', '0', 0, 1, 0, 1, 'IN_FAILED'),
(360, 'Punjab_Haryana', 'None', 1, '05/02/2000', '06/02/2000', 2, 1, 0, 1, 'IN_FAILED'),
(361, 'Punjab_Haryana', 'None', 0, '09/02/2000', '10/02/2000', 0, 1, 0, 1, 'IN_FAILED'),
(362, 'Income_Tax_Appellate', '231', 716, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(363, 'Income_Tax_Appellate', '231', 717, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(364, 'Income_Tax_Appellate', '205', 0, '0', '0', 0, 1, 0, 1, 'IN_FAILED'),
(365, 'Calcutta', '1', 4, '29/06/2000', '26/12/2000', 0, 0, 0, 1, 'IN_ABORT'),
(366, 'Calcutta', '1', 4, '29/06/2000', '26/12/2000', 0, 0, 0, 1, 'IN_SUCCESS'),
(367, 'Calcutta', '1', 2, '21/12/1996', '19/06/1997', 0, 0, 3, 1, 'IN_ABORT'),
(368, 'Calcutta', '1', 2, '21/12/1996', '19/06/1997', 0, 0, 3, 1, 'IN_SUCCESS'),
(369, 'Income_Tax_Appellate', '205', 0, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(370, 'Income_Tax_Appellate', '205', 1, '0', '0', 0, 0, 0, 1, 'IN_SUCCESS'),
(371, 'Madhya_Pradesh', 'None', 0, '01-04-2000', '02-04-2000', 0, 1, 91, 1, 'IN_FAILED'),
(372, 'Madhya_Pradesh', 'None', 2, '11-01-2018', '12-01-2018', 0, 0, 2, 1, 'IN_ABORT'),
(373, 'Income_Tax_Appellate', '199', 206, '02/02/2004', '03/02/2004', 0, 0, 0, 1, 'IN_SUCCESS'),
(374, 'Income_Tax_Appellate', '199', 206, '02/02/2004', '03/02/2004', 0, 0, 0, 1, 'IN_SUCCESS'),
(375, 'Income_Tax_Appellate', '199', 206, '02/02/2004', '03/02/2004', 0, 0, 0, 1, 'IN_SUCCESS'),
(376, 'Income_Tax_Appellate', '199', 6362, '21/12/2006', '22/12/2006', 0, 0, 0, 1, 'IN_ABORT'),
(377, 'Income_Tax_Appellate', '199', 6362, '21/12/2006', '22/12/2006', 0, 0, 0, 1, 'IN_SUCCESS'),
(378, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', 'Mumbai', 1061, '2018-09-28', '2018-10-28', 0, 0, 1, 1, 'IN_SUCCESS'),
(379, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', 'Mumbai', 715, '2018-05-31', '2018-06-30', 0, 0, 0, 1, 'IN_ABORT'),
(380, 'Madhya_Pradesh', 'None', 0, '11-01-2000', '12-01-2000', 0, 0, 11, 1, 'IN_CANCELLED'),
(381, 'Madhya_Pradesh', 'None', 0, '11-01-2000', '12-01-2000', 0, 0, 11, 1, 'IN_SUCCESS'),
(382, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', 'Mumbai', 198, '2018-08-30', '2018-09-29', 0, 0, 0, 1, 'IN_SUCCESS'),
(383, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', 'Mumbai', 199, '2018-08-30', '2018-09-29', 0, 0, 0, 1, 'IN_SUCCESS'),
(384, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', 'Mumbai', 199, '2018-08-30', '2018-09-29', 0, 0, 0, 1, 'IN_SUCCESS'),
(385, 'Madhya_Pradesh', 'None', 0, '24-04-2000', '25-04-2000', 0, 0, 115, 1, 'IN_CANCELLED'),
(386, 'Madhya_Pradesh', 'None', 0, '24-04-2000', '25-04-2000', 0, 0, 115, 1, 'IN_SUCCESS'),
(387, 'Income_Tax_Appellate', '199', 5, '22/12/2006', '23/12/2006', 0, 0, 0, 1, 'IN_CANCELLED'),
(388, 'Income_Tax_Appellate', '199', 5, '22/12/2006', '23/12/2006', 0, 0, 0, 1, 'IN_SUCCESS'),
(389, 'Madhya_Pradesh', 'None', 2, '26-09-2002', '27-09-2002', 0, 1, 875, 1, 'IN_FAILED'),
(390, 'Madhya_Pradesh', 'None', 0, '21/05/2012', '29/09/2018', 0, 1, 0, 1, 'IN_FAILED'),
(391, 'Madhya_Pradesh', 'None', 0, '21/05/2012', '29/09/2018', 0, 1, 0, 1, 'IN_FAILED'),
(392, 'Madhya_Pradesh', 'None', 0, '21/05/2012', '29/09/2018', 0, 1, 0, 1, 'IN_SUCCESS'),
(393, 'Madhya_Pradesh', 'None', 3188, '31-07-2012', '01-08-2012', 0, 1, 14, 1, 'IN_FAILED'),
(394, 'Madhya_Pradesh', 'None', 1074, '13-08-2012', '14-08-2012', 0, 1, 4, 1, 'IN_FAILED'),
(395, 'Income_Tax_Appellate', '205', 6, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_FAILED'),
(396, 'Income_Tax_Appellate', '205', 7, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_ABORT'),
(397, 'Income_Tax_Appellate', '205', 7, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(398, 'Income_Tax_Appellate', '205', 7, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(399, 'Income_Tax_Appellate', '205', 7, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(400, 'Income_Tax_Appellate', '205', 7, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(401, 'Income_Tax_Appellate', '205', 7, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(402, 'Income_Tax_Appellate', '205', 8, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(403, 'Income_Tax_Appellate', '205', 8, '02/01/1999', '03/01/1999', 0, 1, 0, 1, 'IN_SUCCESS'),
(404, 'Income_Tax_Appellate', '205', 64, '03/04/1999', '04/04/1999', 0, 1, 0, 1, 'IN_FAILED'),
(405, 'Income_Tax_Appellate', '205', 9, '03/05/1999', '04/05/1999', 0, 1, 0, 1, 'IN_FAILED'),
(406, 'Income_Tax_Appellate', '205', 6978, '09/03/2004', '10/03/2004', 0, 0, 0, 1, 'IN_ABORT'),
(407, 'Income_Tax_Appellate', '205', 6978, '09/03/2004', '10/03/2004', 0, 0, 0, 1, 'IN_SUCCESS'),
(408, 'Appellate_Tribunal', 'None', 26, '042017', '042017', 0, 0, 0, 1, 'IN_SUCCESS'),
(409, 'Appellate_Tribunal', 'None', 26, '042017', '042017', 0, 0, 0, 1, 'IN_SUCCESS'),
(410, 'Appellate_Tribunal', 'None', 5, '032017', '032017', 0, 0, 0, 1, 'IN_ABORT'),
(411, 'Appellate_Tribunal', 'None', 21, '042017', '042017', 0, 0, 0, 1, 'IN_SUCCESS'),
(412, 'National_Company_Law_Tribunal', 'Principal_Bench_New Delhi_Bench', 88, '2014', '2014', 1, 0, 0, 1, 'IN_ABORT'),
(413, 'Appellate_Tribunal', 'None', 0, '012015', '012015', 0, 0, 0, 1, 'IN_ABORT'),
(414, 'Appellate_Tribunal', 'None', 0, '012015', '012015', 0, 0, 0, 1, 'IN_SUCCESS'),
(415, 'Appellate_Tribunal', 'None', 0, '052013', '052013', 0, 0, 0, 1, 'IN_ABORT'),
(416, 'Appellate_Tribunal', 'None', 0, '052013', '052013', 0, 0, 0, 1, 'IN_SUCCESS'),
(417, 'Madhya_Pradesh', 'None', 0, '20-02-2000', '21-02-2000', 0, 1, 150, 1, 'IN_FAILED'),
(418, 'Madhya_Pradesh', 'None', 0, '24-06-2000', '24-06-2000', 0, 1, 374, 1, 'IN_FAILED'),
(419, 'Madhya_Pradesh', 'None', 0, '08-09-2000', '09-09-2000', 0, 1, 228, 1, 'IN_FAILED'),
(420, 'Income_Tax_Appellate', '205', 5976, '06/04/2005', '07/04/2005', 0, 0, 0, 1, 'IN_ABORT'),
(421, 'Income_Tax_Appellate', '205', 5976, '06/04/2005', '07/04/2005', 0, 0, 0, 1, 'IN_SUCCESS'),
(422, 'Karnataka', 'None', 0, '2000', '2000', 0, 0, 0, 1, 'IN_SUCCESS'),
(423, 'Karnataka', 'None', 0, '2000', '2000', 0, 0, 0, 1, 'IN_SUCCESS'),
(424, 'Karnataka', 'None', 0, '2001', '2013', 0, 0, 0, 1, 'IN_SUCCESS'),
(425, 'Karnataka', 'None', 0, '2001', '2013', 0, 0, 0, 1, 'IN_SUCCESS'),
(426, 'Karnataka', 'None', 2, '2018', '2018', 1, 0, 0, 1, 'IN_SUCCESS'),
(427, 'Karnataka', 'None', 10, '2015', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(428, 'Uttaranchal', 'None', 0, '07/04/2000', '08/04/2000', 0, 0, 97, 1, 'IN_ABORT'),
(429, 'Uttaranchal', 'None', 0, '07/04/2000', '08/04/2000', 0, 0, 97, 1, 'IN_SUCCESS'),
(430, 'Uttaranchal', 'None', 183, '01/05/2001', '02/05/2001', 0, 0, 66, 1, 'IN_SUCCESS'),
(431, 'Uttaranchal', 'None', 299, '12/01/2018', '13/01/2018', 0, 0, 2, 1, 'IN_ABORT'),
(432, 'Uttaranchal', 'None', 299, '12/01/2018', '13/01/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(433, 'Chattisgarh', 'None', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(434, 'Sikkim', 'None', 134, '1018', '1018', 0, 0, 0, 1, 'IN_SUCCESS'),
(435, 'Sikkim', 'None', 1, '1212', '1212', 0, 0, 0, 1, 'IN_SUCCESS'),
(436, 'Sikkim', 'None', 38, '1213', '1213', 0, 0, 0, 1, 'IN_SUCCESS'),
(437, 'Chattisgarh', 'None', 10, '27/12/2010', '25/06/2011', 0, 0, 0, 1, 'IN_SUCCESS'),
(438, 'Chattisgarh', 'None', 0, '30/11/2017', '29/05/2018', 0, 0, 10, 1, 'IN_SUCCESS'),
(439, 'Jammu_Srinagar', '3', 0, '30/06/2018', '27/12/2018', 0, 0, 2, 1, 'IN_SUCCESS'),
(440, 'Orissa', 'None', 0, '02/04/2018', '03/04/2018', 0, 0, 35, 1, 'IN_ABORT'),
(441, 'Orissa', 'None', 6, '30/05/2005', '31/05/2005', 0, 0, 143, 1, 'IN_SUCCESS'),
(442, 'Orissa', 'None', 6, '30/05/2005', '31/05/2005', 0, 0, 144, 1, 'IN_SUCCESS'),
(443, 'Orissa', 'None', 6, '30/05/2005', '31/05/2005', 0, 0, 144, 1, 'IN_SUCCESS'),
(444, 'Orissa', 'None', 29, '31/12/2005', '01/01/2006', 0, 0, 237, 1, 'IN_SUCCESS'),
(445, 'Meghalaya', 'None', 0, '01/10/2018', '02/10/2018', 0, 0, 93, 1, 'IN_SUCCESS'),
(446, 'Meghalaya', 'None', 0, '31/12/2010', '01/01/2011', 0, 0, 159, 1, 'IN_SUCCESS'),
(447, 'Income_Tax_Appellate', '205', 122, '27/04/2006', '28/04/2006', 0, 1, 0, 1, 'IN_FAILED'),
(448, 'Goa', 'None', 104, '01-01-2006', '02-01-2006', 0, 0, 240, 1, 'IN_SUCCESS'),
(449, 'Income_Tax_Appellate', '205', 6, '08/03/2007', '09/03/2007', 0, 0, 0, 1, 'IN_ABORT'),
(450, 'Income_Tax_Appellate', '205', 2, '08/03/2007', '09/03/2007', 0, 0, 0, 1, 'IN_SUCCESS'),
(451, 'Income_Tax_Appellate', '205', 3, '08/03/2007', '09/03/2007', 0, 0, 0, 1, 'IN_SUCCESS'),
(452, 'Income_Tax_Appellate', '205', 3, '08/03/2007', '09/03/2007', 0, 0, 0, 1, 'IN_SUCCESS'),
(453, 'Income_Tax_Appellate', '205', 21897, '28/02/2009', '01/03/2009', 0, 1, 0, 1, 'IN_FAILED'),
(454, 'Income_Tax_Appellate', '205', 12171, '18/01/2012', '19/01/2012', 0, 1, 0, 1, 'IN_FAILED'),
(455, 'Income_Tax_Appellate', '205', 1945, '08/04/2007', '09/04/2007', 0, 1, 0, 1, 'IN_FAILED'),
(456, 'Income_Tax_Appellate', '205', 151, '14/03/2014', '15/03/2014', 0, 1, 0, 1, 'IN_FAILED'),
(457, 'Income_Tax_Appellate', '205', 152, '14/03/2014', '15/03/2014', 0, 1, 0, 1, 'IN_FAILED'),
(458, 'Income_Tax_Appellate', '205', 152, '14/03/2014', '15/03/2014', 0, 1, 0, 1, 'IN_SUCCESS'),
(459, 'Income_Tax_Appellate', '205', 47, '10/04/2015', '11/04/2015', 0, 1, 0, 1, 'IN_FAILED'),
(460, 'Income_Tax_Appellate', '205', 48, '10/04/2015', '11/04/2015', 0, 1, 0, 1, 'IN_FAILED'),
(461, 'Income_Tax_Appellate', '205', 48, '10/04/2015', '11/04/2015', 0, 1, 0, 1, 'IN_SUCCESS'),
(462, 'Income_Tax_Appellate', '205', 8608, '25/01/2017', '26/01/2017', 0, 0, 0, 1, 'IN_ABORT'),
(463, 'Income_Tax_Appellate', '205', 438, '03/03/2017', '04/03/2017', 0, 0, 0, 1, 'IN_SUCCESS'),
(464, 'Income_Tax_Appellate', '205', 439, '03/03/2017', '04/03/2017', 0, 0, 0, 1, 'IN_SUCCESS'),
(465, 'Income_Tax_Appellate', '205', 439, '03/03/2017', '04/03/2017', 0, 0, 0, 1, 'IN_SUCCESS'),
(466, 'Income_Tax_Appellate', '201', 528, '04/04/2005', '05/04/2005', 0, 0, 0, 1, 'IN_SUCCESS'),
(467, 'Income_Tax_Appellate', '201', 529, '04/04/2005', '05/04/2005', 0, 0, 0, 1, 'IN_SUCCESS'),
(468, 'Income_Tax_Appellate', '201', 529, '04/04/2005', '05/04/2005', 0, 0, 0, 1, 'IN_BUCKET_TRANSFER'),
(469, 'Income_Tax_Appellate', '201', 529, '04/04/2005', '05/04/2005', 0, 0, 0, 1, 'IN_SUCCESS'),
(470, 'Income_Tax_Appellate', '201', 2215, '24/02/2006', '25/02/2006', 0, 1, 0, 1, 'IN_FAILED'),
(471, 'Income_Tax_Appellate', '201', 2215, '24/02/2006', '25/02/2006', 0, 1, 0, 1, 'IN_FAILED'),
(472, 'Income_Tax_Appellate', '201', 2216, '24/02/2006', '25/02/2006', 0, 1, 0, 1, 'IN_BUCKET_TRANSFER'),
(473, 'Income_Tax_Appellate', '201', 2216, '24/02/2006', '25/02/2006', 0, 1, 0, 1, 'IN_SUCCESS'),
(474, 'Income_Tax_Appellate', '201', 1277, '09/07/2009', '10/07/2009', 0, 1, 0, 1, 'IN_FAILED'),
(475, 'Income_Tax_Appellate', '201', 0, '11/07/2011', '12/07/2011', 0, 0, 0, 1, 'IN_ABORT'),
(476, 'Income_Tax_Appellate', '201', 0, '11/07/2011', '12/07/2011', 0, 0, 0, 1, 'IN_SUCCESS'),
(477, 'Income_Tax_Appellate', '201', 0, '09/07/2008', '10/07/2008', 0, 0, 0, 1, 'IN_ABORT'),
(478, 'Income_Tax_Appellate', '201', 0, '09/07/2008', '10/07/2008', 0, 0, 0, 1, 'IN_SUCCESS'),
(479, 'Income_Tax_Appellate', '201', 1179, '14/08/2013', '15/08/2013', 0, 1, 0, 1, 'IN_FAILED'),
(480, 'Income_Tax_Appellate', '201', 1180, '14/08/2013', '15/08/2013', 0, 1, 0, 1, 'IN_FAILED'),
(481, 'Income_Tax_Appellate', '201', 1181, '14/08/2013', '15/08/2013', 0, 1, 0, 1, 'IN_BUCKET_TRANSFER'),
(482, 'Income_Tax_Appellate', '201', 1181, '14/08/2013', '15/08/2013', 0, 1, 0, 1, 'IN_SUCCESS'),
(483, 'Income_Tax_Appellate', '201', 70, '18/02/2014', '19/02/2014', 0, 1, 0, 1, 'IN_FAILED'),
(484, 'Supreme_Court', 'None', 180, '01-01-2009', '30-06-2009', 0, 0, 0, 1, 'IN_CANCELLED'),
(485, 'Supreme_Court', 'None', 180, '01-01-2009', '30-06-2009', 0, 0, 0, 1, 'IN_SUCCESS'),
(486, 'Income_Tax_Appellate', '201', 559, '10/05/2016', '11/05/2016', 0, 1, 0, 1, 'IN_FAILED'),
(487, 'Income_Tax_Appellate', '201', 560, '10/05/2016', '11/05/2016', 0, 1, 0, 1, 'IN_FAILED'),
(488, 'Income_Tax_Appellate', '201', 561, '10/05/2016', '11/05/2016', 0, 1, 0, 1, 'IN_BUCKET_TRANSFER'),
(489, 'Income_Tax_Appellate', '201', 561, '10/05/2016', '11/05/2016', 0, 1, 0, 1, 'IN_SUCCESS'),
(490, 'Income_Tax_Appellate', '201', 119, '28/12/2016', '29/12/2016', 0, 1, 0, 1, 'IN_FAILED'),
(491, 'Income_Tax_Appellate', '201', 120, '28/12/2016', '29/12/2016', 0, 1, 0, 1, 'IN_FAILED'),
(492, 'Income_Tax_Appellate', '201', 120, '28/12/2016', '29/12/2016', 0, 1, 0, 1, 'IN_SUCCESS'),
(493, 'Income_Tax_Appellate', '201', 16, '14/03/2017', '15/03/2017', 0, 1, 0, 1, 'IN_FAILED'),
(494, 'Income_Tax_Appellate', '201', 17, '14/03/2017', '15/03/2017', 0, 1, 0, 1, 'IN_FAILED'),
(495, 'Income_Tax_Appellate', '201', 17, '14/03/2017', '15/03/2017', 0, 1, 0, 1, 'IN_SUCCESS'),
(496, 'Income_Tax_Appellate', '201', 1600, '25/08/2017', '26/08/2017', 0, 1, 0, 1, 'IN_FAILED'),
(497, 'Income_Tax_Appellate', '201', 40, '06/10/2017', '07/10/2017', 0, 1, 0, 1, 'IN_FAILED'),
(498, 'Income_Tax_Appellate', '201', 41, '06/10/2017', '07/10/2017', 0, 1, 0, 1, 'IN_FAILED'),
(499, 'Income_Tax_Appellate', '201', 41, '06/10/2017', '07/10/2017', 0, 1, 0, 1, 'IN_SUCCESS'),
(500, 'Income_Tax_Appellate', '201', 6976, '07/09/2018', '08/09/2018', 0, 0, 0, 1, 'IN_ABORT'),
(501, 'Karnataka', 'None', 0, '2000', '2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(502, 'Karnataka', 'None', 0, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(503, 'Karnataka', 'None', 0, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(504, 'Karnataka', 'None', 0, '2000', '2014', 0, 0, 0, 1, 'IN_SUCCESS'),
(505, 'Karnataka', 'None', 0, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS'),
(506, 'Karnataka', 'None', 0, '2014', '2018', 0, 0, 0, 1, 'IN_SUCCESS');

-- --------------------------------------------------------

--
-- Table structure for table `Tracker_History_JSON`
--
-- Creation: Aug 21, 2018 at 07:40 PM
-- Last update: Oct 20, 2018 at 02:55 PM
--

CREATE TABLE `Tracker_History_JSON` (
  `id` int(11) NOT NULL,
  `Name` varchar(500) DEFAULT NULL,
  `Start_Date` varchar(40) DEFAULT NULL,
  `End_Date` varchar(40) DEFAULT NULL,
  `No_Files` int(11) DEFAULT NULL,
  `emergency_exit` tinyint(1) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Tracker_History_JSON`
--

INSERT INTO `Tracker_History_JSON` (`id`, `Name`, `Start_Date`, `End_Date`, `No_Files`, `emergency_exit`, `status`) VALUES
(1, 'Arunachal_Pradesh', '01/08/2018', '01/08/2018', 1, 1, 'IN_SUCCESS'),
(2, 'Arunachal_Pradesh', '12/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(3, 'Calcutta', 'Sunday, August 05, 2018', 'Wednesday, August 22, 2018', 6, 1, 'IN_SUCCESS'),
(4, 'Calcutta', 'Sunday, August 05, 2018', 'Tuesday, August 21, 2018', 6, 1, 'IN_SUCCESS'),
(5, 'Calcutta', 'Thursday, August 16, 2018', 'Thursday, August 09, 2018', 6, 1, 'IN_SUCCESS'),
(6, 'Madras', '01/08/1979', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(7, 'Arunachal_Pradesh', '12/08/2018', '14/08/2018', 1, 1, 'IN_SUCCESS'),
(8, 'Arunachal_Pradesh', '13/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(9, 'Arunachal_Pradesh', '13/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(10, 'Arunachal_Pradesh', '13/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(11, 'Arunachal_Pradesh', '13/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(12, 'Arunachal_Pradesh', '13/08/2018', '10/08/2018', 1, 1, 'IN_SUCCESS'),
(13, 'Arunachal_Pradesh', '14/08/2018', '23/08/2018', 1, 1, 'IN_SUCCESS'),
(14, 'Arunachal_Pradesh', '14/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(15, 'Arunachal_Pradesh', '14/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(16, 'Arunachal_Pradesh', '14/08/2018', '22/08/2018', 1, 1, 'IN_SUCCESS'),
(17, 'Madras', '01/01/1950', '27/08/2018', 66, 1, 'IN_SUCCESS'),
(18, 'Uttaranchal', '01/08/2018', '27/08/2018', 1, 1, 'IN_SUCCESS'),
(19, 'Sikkim', '01-08-2018', '27-08-2018', 1, 1, 'IN_SUCCESS'),
(20, 'Nagaland', '01.08.2018', '27.08.2018', 1, 1, 'IN_SUCCESS'),
(21, 'Mizoram', '01.01.2018', '27.08.2018', 1, 1, 'IN_SUCCESS'),
(22, 'Kerala', '01/01/2018', '28/08/2018', 7, 1, 'IN_SUCCESS'),
(23, 'Supreme_Court', '01-08-2018', '01-08-2018', 2, 1, 'IN_SUCCESS'),
(24, 'Calcutta', 'Wednesday, August 01, 2018', 'Wednesday, August 01, 2018', 6, 1, 'IN_SUCCESS'),
(25, 'Calcutta', 'Wednesday, August 01, 2018', 'Wednesday, August 01, 2018', 6, 1, 'IN_SUCCESS'),
(26, 'Chattisgarh', '01/08/2018', '01/08/2018', 1, 1, 'IN_SUCCESS'),
(27, 'Madras', '01/08/2018', '01/08/2018', 80, 1, 'IN_SUCCESS'),
(28, 'Madras', '01/08/2018', '01/08/2018', 92, 1, 'IN_SUCCESS'),
(29, 'Madras', '01/08/2018', '01/08/2018', 117, 1, 'IN_SUCCESS'),
(30, 'Arunachal_Pradesh', '01/08/2018', '01/08/2018', 1, 1, 'IN_SUCCESS'),
(31, 'Arunachal_Pradesh', '01/08/2018', '01/08/2018', 1, 1, 'IN_SUCCESS'),
(32, 'Arunachal_Pradesh', '01/08/2018', '01/08/2018', 1, 1, 'IN_SUCCESS'),
(33, 'Himachal_Pradesh', '01-08-2018', '01-08-2018', 1, 1, 'IN_SUCCESS'),
(34, 'Chattisgarh', '01/08/2018', '30/08/2018', 1, 1, 'IN_SUCCESS'),
(35, 'Karnataka', '01-Aug-2018', '01-Aug-2018', 1, 1, 'IN_SUCCESS'),
(36, 'Jammu_Srinagar', '01/08/2018', '01/08/2018', 3, 1, 'IN_SUCCESS'),
(37, 'Hyderabad', '01/08/2018', '01/08/2018', 1, 1, 'IN_SUCCESS'),
(38, 'Kerala', '01/08/2018', '01/08/2018', 7, 1, 'IN_SUCCESS'),
(39, 'Madras', '01/08/2018', '01/08/2018', 66, 1, 'IN_SUCCESS'),
(40, 'Madras', '01/08/2018', '01/08/2018', 100, 1, 'IN_SUCCESS'),
(41, 'Madras', '01/08/2018', '01/08/2018', 77, 1, 'IN_SUCCESS'),
(42, 'Meghalaya', '19/08/2018', '31/08/2018', 1, 1, 'IN_SUCCESS'),
(43, 'Meghalaya', '19/08/2018', '31/08/2018', 1, 1, 'IN_SUCCESS'),
(44, 'Supreme_Court', '01-09-2018', '02-09-2018', 10, 1, 'IN_SUCCESS'),
(45, 'Jammu_Srinagar', '01/09/2018', '01/09/2018', 3, 1, 'IN_SUCCESS'),
(46, 'Arunachal_Pradesh', '01/09/2018', '01/09/2018', 1, 1, 'IN_SUCCESS'),
(47, 'Uttaranchal', '03/09/2018', '03/09/2018', 15, 1, 'IN_SUCCESS'),
(48, 'Supreme_Court', '03-09-2018', '03-09-2018', 1, 1, 'IN_SUCCESS'),
(49, 'Sikkim', '03-09-2018', '03-09-2018', 1, 1, 'IN_SUCCESS'),
(50, 'Orissa', '03/09/2018', '03/09/2018', 1, 1, 'IN_SUCCESS'),
(51, 'Nagaland', '03.09.2018', '03.09.2018', 1, 1, 'IN_SUCCESS'),
(52, 'Mizoram', '03.09.2018', '03.09.2018', 1, 1, 'IN_SUCCESS'),
(53, 'Meghalaya', '03/09/2018', '03/09/2018', 2, 1, 'IN_SUCCESS'),
(54, 'Manipur', '03-09-2018', '03-09-2018', 1, 1, 'IN_SUCCESS'),
(55, 'Madras', '03/09/2018', '03/09/2018', 79, 1, 'IN_SUCCESS'),
(56, 'Kerala', '03/09/2018', '03/09/2018', 7, 1, 'IN_SUCCESS'),
(57, 'Karnataka', '03-Sep-2018', '03-Sep-2018', 1, 1, 'IN_SUCCESS'),
(58, 'Jammu_Srinagar', '03/09/2018', '03/09/2018', 1, 1, 'IN_SUCCESS'),
(59, 'Hyderabad', '03/09/2018', '03/09/2018', 1, 1, 'IN_SUCCESS'),
(60, 'Himachal_Pradesh', '03-09-2018', '03-09-2018', 6, 1, 'IN_SUCCESS'),
(61, 'Chattisgarh', '03/09/2018', '03/09/2018', 1, 1, 'IN_SUCCESS'),
(62, 'Chattisgarh', '03/09/2018', '03/09/2018', 1, 1, 'IN_SUCCESS'),
(63, 'Calcutta', 'Monday, September 03, 2018', 'Monday, September 03, 2018', 6, 1, 'IN_SUCCESS'),
(64, 'Arunachal_Pradesh', '03/09/2018', '03/09/2018', 1, 1, 'IN_SUCCESS'),
(65, 'Madras', '02/09/2018', '02/09/2018', 1, 1, 'IN_SUCCESS'),
(66, 'Bombay', '01/09/2018', '01/09/2018', 1, 1, 'IN_SUCCESS'),
(67, 'Jammu_Srinagar', '01/09/2018', '01/09/2018', 3, 1, 'IN_SUCCESS'),
(68, 'Uttaranchal', '01/09/2018', '05/09/2018', 9, 1, 'IN_SUCCESS'),
(69, 'Nagaland', '01.09.2018', '05.09.2018', 1, 1, 'IN_SUCCESS'),
(70, 'Madras', '01/09/2018', '05/09/2018', 155, 1, 'IN_SUCCESS'),
(71, 'Madras', '01/09/2018', '05/09/2018', 158, 1, 'IN_SUCCESS'),
(72, 'Madras', '06/09/2018', '06/09/2018', 28, 1, 'IN_SUCCESS'),
(73, 'Madras', '06/09/2018', '06/09/2018', 2, 1, 'IN_SUCCESS'),
(74, 'Madras', '06/09/2018', '06/09/2018', 14, 1, 'IN_SUCCESS'),
(75, 'Delhi', '01/09/2018', '07/09/2018', 1, 1, 'IN_SUCCESS'),
(76, 'Himachal_Pradesh', '01-09-2018', '07-09-2018', 5, 1, 'IN_SUCCESS'),
(77, 'Madhya_Pradesh', '02-09-2018', '02-09-2018', 1, 1, 'IN_SUCCESS'),
(78, 'Delhi', '05/09/2018', '05/09/2018', 5, 1, 'IN_SUCCESS'),
(79, 'Delhi', '08/09/2018', '08/09/2018', 2, 1, 'IN_SUCCESS'),
(80, 'Delhi', '09/09/2018', '09/09/2018', 6, 1, 'IN_SUCCESS'),
(81, 'Delhi', '09/09/2018', '09/09/2018', 3, 1, 'IN_SUCCESS'),
(82, 'Delhi', '09/09/2018', '09/09/2018', 3, 1, 'IN_SUCCESS'),
(83, 'Delhi', '09/09/2018', '09/09/2018', 1, 1, 'IN_SUCCESS'),
(84, 'Delhi', '09/09/2018', '10/09/2018', 5, 1, 'IN_SUCCESS'),
(85, 'Delhi', '10/09/2018', '10/09/2018', 3, 1, 'IN_SUCCESS'),
(86, 'Delhi', '10/09/2018', '10/09/2018', 1, 1, 'IN_SUCCESS'),
(87, 'Delhi', '11/09/2018', '11/09/2018', 8, 1, 'IN_SUCCESS'),
(88, 'Delhi', '11/09/2018', '11/09/2018', 4, 1, 'IN_SUCCESS'),
(89, 'Bombay', '12/09/2018', '12/09/2018', 1, 1, 'IN_SUCCESS'),
(90, 'Bombay', '12/09/2018', '12/09/2018', 1, 1, 'IN_SUCCESS'),
(91, 'Delhi', '12/09/2018', '12/09/2018', 9, 1, 'IN_SUCCESS'),
(92, 'Goa', '09-09-2018', '09-09-2018', 2, 1, 'IN_SUCCESS'),
(93, 'Delhi', '11/09/2018', '11/09/2018', 3, 1, 'IN_SUCCESS'),
(94, 'Delhi', '13/09/2018', '13/09/2018', 1, 1, 'IN_SUCCESS'),
(95, 'Gauhati', '13/09/2018', '13/09/2018', 1, 1, 'IN_SUCCESS'),
(96, 'Gauhati', '13/09/2018', '13/09/2018', 1, 1, 'IN_SUCCESS'),
(97, 'Gauhati', '14/09/2018', '14/09/2018', 1, 1, 'IN_SUCCESS'),
(98, 'Delhi', '11/09/2018', '11/09/2018', 3, 1, 'IN_SUCCESS'),
(99, 'Delhi', '15/09/2018', '15/09/2018', 4, 1, 'IN_SUCCESS'),
(100, 'Delhi', '13/09/2018', '15/09/2018', 1, 1, 'IN_SUCCESS'),
(101, 'Delhi', '16/09/2018', '16/09/2018', 7, 1, 'IN_SUCCESS'),
(102, 'Delhi', '13/09/2018', '13/09/2018', 2, 1, 'IN_SUCCESS'),
(103, 'Delhi', '17/09/2018', '17/09/2018', 5, 1, 'IN_SUCCESS'),
(104, 'Delhi', '17/09/2018', '17/09/2018', 2, 1, 'IN_SUCCESS'),
(105, 'Delhi', '17/09/2018', '17/09/2018', 2, 1, 'IN_SUCCESS'),
(106, 'Karnataka', '01-Sep-2014', '01-Sep-2018', 1, 1, 'IN_SUCCESS'),
(107, 'Uttaranchal', '01/01/2000', '31/01/2001', 1, 1, 'IN_SUCCESS'),
(108, 'Delhi', '18/09/2018', '18/09/2018', 3, 1, 'IN_SUCCESS'),
(109, 'Goa', '18-09-2018', '18-09-2018', 1, 1, 'IN_SUCCESS'),
(110, 'Karnataka', '18-Sep-2018', '18-Sep-2018', 1, 1, 'IN_SUCCESS'),
(111, 'Delhi', '16/09/2018', '18/09/2018', 1, 1, 'IN_SUCCESS'),
(112, 'Delhi', '19/09/2018', '19/09/2018', 1, 1, 'IN_SUCCESS'),
(113, 'Income_Tax_Appellate', '01/09/2018', '04/09/2018', 2, 1, 'IN_SUCCESS'),
(114, 'Income_Tax_Appellate', '20/09/2018', '20/09/2018', 7, 1, 'IN_SUCCESS'),
(115, 'Delhi', '21/09/2018', '21/09/2018', 3, 1, 'IN_SUCCESS'),
(116, 'Gauhati', '21/09/2018', '21/09/2018', 7, 1, 'IN_SUCCESS'),
(117, 'Punjab_Haryana', '20-Sep-2018', '20-Sep-2018', 2, 1, 'IN_SUCCESS'),
(118, 'Bombay', '07/09/2018', '07/09/2018', 1, 1, 'IN_SUCCESS'),
(119, 'Income_Tax_Appellate', '19/09/2018', '20/09/2018', 13, 1, 'IN_SUCCESS'),
(120, 'Goa', '23-09-2018', '23-09-2018', 1, 1, 'IN_SUCCESS'),
(121, 'Meghalaya', '06/09/2018', '24/09/2018', 1, 1, 'IN_SUCCESS'),
(122, 'Income_Tax_Appellate', '27/09/2018', '27/09/2018', 13, 1, 'IN_SUCCESS'),
(123, 'Income_Tax_Appellate', '28/09/2018', '28/09/2018', 3, 1, 'IN_SUCCESS'),
(124, 'Calcutta', 'Friday, September 28, 2018', 'Friday, September 28, 2018', 40, 1, 'IN_SUCCESS'),
(125, 'Income_Tax_Appellate', '30/09/2018', '30/09/2018', 13, 1, 'IN_SUCCESS'),
(126, 'Madhya_Pradesh', '01-10-2018', '01-10-2018', 23, 1, 'IN_SUCCESS'),
(127, 'Gauhati', '01/10/2018', '01/10/2018', 1, 1, 'IN_SUCCESS'),
(128, 'Appellate_Tribunal', '01-10-2018', '01-10-2018', 1, 1, 'IN_SUCCESS'),
(129, 'Income_Tax_Appellate', '01/10/2018', '01/10/2018', 7, 1, 'IN_SUCCESS'),
(130, 'Appellate_Tribunal', '01-10-2018', '01-10-2018', 1, 1, 'IN_SUCCESS'),
(131, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', '01/10/2018', '01/10/2018', 1, 1, 'IN_SUCCESS'),
(132, 'Income_Tax_Appellate', '01/10/2018', '01/10/2018', 3, 1, 'IN_SUCCESS'),
(133, 'Uttaranchal', '01/01/2001', '01/05/2001', 1, 1, 'IN_SUCCESS'),
(134, 'Uttaranchal', '01/01/2017', '31/05/2018', 1, 1, 'IN_SUCCESS'),
(135, 'Sikkim', '01-01-2012', '31-05-2018', 1, 1, 'IN_SUCCESS'),
(136, 'Orissa', '01/01/2012', '31/05/2018', 1, 1, 'IN_SUCCESS'),
(137, 'Income_Tax_Appellate', '03/10/2018', '03/10/2018', 4, 1, 'IN_SUCCESS'),
(138, 'Income_Tax_Appellate', '03/10/2018', '03/10/2018', 5, 1, 'IN_SUCCESS'),
(139, 'Income_Tax_Appellate', '03/10/2018', '03/10/2018', 2, 1, 'IN_SUCCESS'),
(140, 'Income_Tax_Appellate', '04/10/2018', '04/10/2018', 5, 1, 'IN_SUCCESS'),
(141, 'Income_Tax_Appellate', '04/10/2018', '04/10/2018', 4, 1, 'IN_SUCCESS'),
(142, 'Income_Tax_Appellate', '05/10/2018', '05/10/2018', 12, 1, 'IN_SUCCESS'),
(143, 'Income_Tax_Appellate', '06/10/2018', '06/10/2018', 7, 1, 'IN_SUCCESS'),
(144, 'Income_Tax_Appellate', '06/10/2018', '06/10/2018', 5, 1, 'IN_SUCCESS'),
(145, 'Income_Tax_Appellate', '06/10/2018', '06/10/2018', 1, 1, 'IN_SUCCESS'),
(146, 'Income_Tax_Appellate', '07/10/2018', '07/10/2018', 5, 1, 'IN_SUCCESS'),
(147, 'Income_Tax_Appellate', '07/10/2018', '07/10/2018', 3, 1, 'IN_SUCCESS'),
(148, 'Income_Tax_Appellate', '07/10/2018', '07/10/2018', 1, 1, 'IN_SUCCESS'),
(149, 'Income_Tax_Appellate', '08/10/2018', '08/10/2018', 5, 1, 'IN_SUCCESS'),
(150, 'Income_Tax_Appellate', '09/10/2018', '09/10/2018', 4, 1, 'IN_SUCCESS'),
(151, 'Income_Tax_Appellate', '09/10/2018', '09/10/2018', 2, 1, 'IN_SUCCESS'),
(152, 'Income_Tax_Appellate', '10/10/2018', '10/10/2018', 4, 1, 'IN_SUCCESS'),
(153, 'Income_Tax_Appellate', '10/10/2018', '10/10/2018', 2, 1, 'IN_SUCCESS'),
(154, 'Income_Tax_Appellate', '11/10/2018', '11/10/2018', 3, 1, 'IN_SUCCESS'),
(155, 'Income_Tax_Appellate', '11/10/2018', '11/10/2018', 3, 1, 'IN_SUCCESS'),
(156, 'Income_Tax_Appellate', '12/10/2018', '12/10/2018', 3, 1, 'IN_SUCCESS'),
(157, 'Income_Tax_Appellate', '12/10/2018', '12/10/2018', 2, 1, 'IN_SUCCESS'),
(158, 'Income_Tax_Appellate', '15/10/2018', '15/10/2018', 17, 1, 'IN_SUCCESS'),
(159, 'Income_Tax_Appellate', '15/10/2018', '15/10/2018', 4, 1, 'IN_SUCCESS'),
(160, 'Income_Tax_Appellate', '16/10/2018', '16/10/2018', 3, 1, 'IN_SUCCESS'),
(161, 'Income_Tax_Appellate', '16/10/2018', '16/10/2018', 1, 1, 'IN_SUCCESS'),
(162, 'Supreme_Court', '01-01-2009', '31-12-2009', 1, 1, 'IN_SUCCESS'),
(163, 'Income_Tax_Appellate', '16/10/2018', '16/10/2018', 3, 1, 'IN_SUCCESS'),
(164, 'Income_Tax_Appellate', '17/10/2018', '17/10/2018', 6, 1, 'IN_SUCCESS'),
(165, 'Income_Tax_Appellate', '17/10/2018', '17/10/2018', 2, 1, 'IN_SUCCESS'),
(166, 'Income_Tax_Appellate', '18/10/2018', '18/10/2018', 2, 1, 'IN_SUCCESS'),
(167, 'Income_Tax_Appellate', '18/10/2018', '18/10/2018', 5, 1, 'IN_SUCCESS'),
(168, 'Income_Tax_Appellate', '18/10/2018', '18/10/2018', 2, 1, 'IN_SUCCESS'),
(169, 'Income_Tax_Appellate', '19/10/2018', '19/10/2018', 1, 1, 'IN_SUCCESS'),
(170, 'Income_Tax_Appellate', '19/10/2018', '19/10/2018', 3, 1, 'IN_SUCCESS'),
(171, 'Income_Tax_Appellate', '20/10/2018', '20/10/2018', 4, 1, 'IN_SUCCESS');

-- --------------------------------------------------------

--
-- Table structure for table `Tracker_JSON`
--
-- Creation: Aug 31, 2018 at 08:16 AM
-- Last update: Oct 21, 2018 at 01:37 PM
--

CREATE TABLE `Tracker_JSON` (
  `id` int(11) NOT NULL,
  `Name` varchar(500) DEFAULT NULL,
  `Start_Date` varchar(40) DEFAULT NULL,
  `End_Date` varchar(40) DEFAULT NULL,
  `No_Files` int(11) DEFAULT NULL,
  `json_count` bigint(20) DEFAULT '0',
  `emergency_exit` tinyint(1) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Tracker_JSON`
--

INSERT INTO `Tracker_JSON` (`id`, `Name`, `Start_Date`, `End_Date`, `No_Files`, `json_count`, `emergency_exit`, `status`) VALUES
(20, 'Bombay', '07/09/2018', '07/09/2018', 1, 4, 1, 'IN_SUCCESS'),
(23, 'Delhi', '21/09/2018', '21/09/2018', 3, 89, 1, 'IN_SUCCESS'),
(29, 'Madhya_Pradesh', '01-10-2018', '01-10-2018', 23, 24, 1, 'IN_SUCCESS'),
(31, 'Manipur', '03-09-2018', '03-09-2018', 1, 1, 1, 'IN_SUCCESS'),
(32, 'Meghalaya', '06/09/2018', '24/09/2018', 1, 5, 1, 'IN_SUCCESS'),
(35, 'Orissa', '01/01/2012', '31/05/2018', 1, 2, 1, 'IN_SUCCESS'),
(36, 'Punjab_Haryana', '20-Sep-2018', '20-Sep-2018', 2, 2, 1, 'IN_SUCCESS'),
(57, 'Uttaranchal', '01/01/2017', '31/05/2018', 1, 1, 1, 'IN_SUCCESS'),
(58, 'Sikkim', '01-01-2012', '31-05-2018', 1, 1, 1, 'IN_SUCCESS'),
(59, 'Nagaland', '01.09.2018', '05.09.2018', 1, 2, 1, 'IN_SUCCESS'),
(60, 'Mizoram', '03.09.2018', '03.09.2018', 1, 1, 1, 'IN_SUCCESS'),
(62, 'Supreme_Court', '01-01-2009', '31-12-2009', 1, 12, 1, 'IN_SUCCESS'),
(64, 'Calcutta', 'Friday, September 28, 2018', 'Friday, September 28, 2018', 40, 46, 1, 'IN_SUCCESS'),
(71, 'Arunachal_Pradesh', '03/09/2018', '03/09/2018', 1, 2, 1, 'IN_SUCCESS'),
(72, 'Himachal_Pradesh', '01-09-2018', '07-09-2018', 5, 11, 1, 'IN_SUCCESS'),
(73, 'Chattisgarh', '03/09/2018', '03/09/2018', 1, 2, 1, 'IN_SUCCESS'),
(74, 'Karnataka', '18-Sep-2018', '18-Sep-2018', 1, 3, 1, 'IN_SUCCESS'),
(75, 'Jammu_Srinagar', '01/09/2018', '01/09/2018', 3, 7, 1, 'IN_SUCCESS'),
(76, 'Hyderabad', '03/09/2018', '03/09/2018', 1, 1, 1, 'IN_SUCCESS'),
(77, 'Kerala', '03/09/2018', '03/09/2018', 7, 7, 1, 'IN_SUCCESS'),
(80, 'Madras', '06/09/2018', '06/09/2018', 14, 282, 1, 'IN_SUCCESS'),
(81, 'Goa', '23-09-2018', '23-09-2018', 1, 4, 1, 'IN_SUCCESS'),
(82, 'Gauhati', '01/10/2018', '01/10/2018', 1, 11, 1, 'IN_SUCCESS'),
(83, 'Income_Tax_Appellate', '20/10/2018', '20/10/2018', 4, 196, 1, 'IN_SUCCESS'),
(84, 'Customs_Excise_And_Service_Tax_Appellate_Tribunal', '01/10/2018', '01/10/2018', 1, 1, 1, 'IN_SUCCESS'),
(85, 'National_Company_Law_Tribunal', '0', '0', 0, 0, 0, '0'),
(86, 'Appellate_Tribunal', '01-10-2018', '01-10-2018', 1, 2, 1, 'IN_SUCCESS');

-- --------------------------------------------------------

--
-- Table structure for table `Tracker_pdf`
--
-- Creation: Oct 21, 2018 at 05:38 PM
-- Last update: Oct 21, 2018 at 05:38 PM
--

CREATE TABLE `Tracker_pdf` (
  `id` int(11) NOT NULL,
  `Name` varchar(200) DEFAULT NULL,
  `No_Files` int(11) DEFAULT '0',
  `emergency_exit` tinyint(1) DEFAULT '0',
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Tracker_pdf`
--

INSERT INTO `Tracker_pdf` (`id`, `Name`, `No_Files`, `emergency_exit`, `status`) VALUES
(1, 'Arunachal_Pradesh', 0, 1, 'IN_CANCELLED');

-- --------------------------------------------------------

--
-- Table structure for table `Uttaranchal`
--
-- Creation: Oct 21, 2018 at 05:51 PM
--

CREATE TABLE `Uttaranchal` (
  `id` int(11) NOT NULL,
  `case_no` varchar(1000) CHARACTER SET latin1 NOT NULL,
  `petitioner` text CHARACTER SET latin1,
  `respondent` text CHARACTER SET latin1,
  `judgment_date` text CHARACTER SET latin1,
  `corrigendum` text CHARACTER SET latin1,
  `pdf_data` longtext CHARACTER SET latin1,
  `pdf_file` text CHARACTER SET latin1,
  `pdf_filename` varchar(1000) DEFAULT NULL,
  `bench_code` int(11) DEFAULT NULL,
  `is_json` tinyint(1) DEFAULT '0',
  `is_pdf` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Appellate_Tribunal`
--
ALTER TABLE `Appellate_Tribunal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Arunachal_Pradesh`
--
ALTER TABLE `Arunachal_Pradesh`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Bombay`
--
ALTER TABLE `Bombay`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Calcutta`
--
ALTER TABLE `Calcutta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Chattisgarh`
--
ALTER TABLE `Chattisgarh`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Customs_Excise_And_Service_Tax_Appellate_Tribunal`
--
ALTER TABLE `Customs_Excise_And_Service_Tax_Appellate_Tribunal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Delhi`
--
ALTER TABLE `Delhi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Gauhati`
--
ALTER TABLE `Gauhati`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Goa`
--
ALTER TABLE `Goa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Himachal_Pradesh`
--
ALTER TABLE `Himachal_Pradesh`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Hyderabad`
--
ALTER TABLE `Hyderabad`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Income_Tax_Appellate`
--
ALTER TABLE `Income_Tax_Appellate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appeal_no` (`appeal_no`);

--
-- Indexes for table `Jammu_Srinagar`
--
ALTER TABLE `Jammu_Srinagar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Karnataka`
--
ALTER TABLE `Karnataka`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Kerala`
--
ALTER TABLE `Kerala`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Madhya_Pradesh`
--
ALTER TABLE `Madhya_Pradesh`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Madras`
--
ALTER TABLE `Madras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Manipur`
--
ALTER TABLE `Manipur`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Meghalaya`
--
ALTER TABLE `Meghalaya`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Mizoram`
--
ALTER TABLE `Mizoram`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Nagaland`
--
ALTER TABLE `Nagaland`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `National_Company_Law_Tribunal`
--
ALTER TABLE `National_Company_Law_Tribunal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Orissa`
--
ALTER TABLE `Orissa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Punjab_Haryana`
--
ALTER TABLE `Punjab_Haryana`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Sikkim`
--
ALTER TABLE `Sikkim`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Supreme_Court`
--
ALTER TABLE `Supreme_Court`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- Indexes for table `Tracker`
--
ALTER TABLE `Tracker`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Tracker_History`
--
ALTER TABLE `Tracker_History`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Tracker_History_JSON`
--
ALTER TABLE `Tracker_History_JSON`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Tracker_JSON`
--
ALTER TABLE `Tracker_JSON`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Tracker_pdf`
--
ALTER TABLE `Tracker_pdf`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Uttaranchal`
--
ALTER TABLE `Uttaranchal`
  ADD PRIMARY KEY (`id`),
  ADD KEY `case_no` (`case_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Appellate_Tribunal`
--
ALTER TABLE `Appellate_Tribunal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;
--
-- AUTO_INCREMENT for table `Arunachal_Pradesh`
--
ALTER TABLE `Arunachal_Pradesh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=598;
--
-- AUTO_INCREMENT for table `Bombay`
--
ALTER TABLE `Bombay`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Calcutta`
--
ALTER TABLE `Calcutta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45084;
--
-- AUTO_INCREMENT for table `Chattisgarh`
--
ALTER TABLE `Chattisgarh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1193;
--
-- AUTO_INCREMENT for table `Customs_Excise_And_Service_Tax_Appellate_Tribunal`
--
ALTER TABLE `Customs_Excise_And_Service_Tax_Appellate_Tribunal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=915;
--
-- AUTO_INCREMENT for table `Delhi`
--
ALTER TABLE `Delhi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76910;
--
-- AUTO_INCREMENT for table `Gauhati`
--
ALTER TABLE `Gauhati`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6611;
--
-- AUTO_INCREMENT for table `Goa`
--
ALTER TABLE `Goa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=846;
--
-- AUTO_INCREMENT for table `Himachal_Pradesh`
--
ALTER TABLE `Himachal_Pradesh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10585;
--
-- AUTO_INCREMENT for table `Hyderabad`
--
ALTER TABLE `Hyderabad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
--
-- AUTO_INCREMENT for table `Income_Tax_Appellate`
--
ALTER TABLE `Income_Tax_Appellate`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=180624;
--
-- AUTO_INCREMENT for table `Jammu_Srinagar`
--
ALTER TABLE `Jammu_Srinagar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2960;
--
-- AUTO_INCREMENT for table `Karnataka`
--
ALTER TABLE `Karnataka`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2173;
--
-- AUTO_INCREMENT for table `Kerala`
--
ALTER TABLE `Kerala`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6818;
--
-- AUTO_INCREMENT for table `Madhya_Pradesh`
--
ALTER TABLE `Madhya_Pradesh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22860;
--
-- AUTO_INCREMENT for table `Madras`
--
ALTER TABLE `Madras`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=133655;
--
-- AUTO_INCREMENT for table `Manipur`
--
ALTER TABLE `Manipur`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Meghalaya`
--
ALTER TABLE `Meghalaya`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=692;
--
-- AUTO_INCREMENT for table `Mizoram`
--
ALTER TABLE `Mizoram`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=94;
--
-- AUTO_INCREMENT for table `Nagaland`
--
ALTER TABLE `Nagaland`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=924;
--
-- AUTO_INCREMENT for table `National_Company_Law_Tribunal`
--
ALTER TABLE `National_Company_Law_Tribunal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=230;
--
-- AUTO_INCREMENT for table `Orissa`
--
ALTER TABLE `Orissa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=518;
--
-- AUTO_INCREMENT for table `Punjab_Haryana`
--
ALTER TABLE `Punjab_Haryana`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1782;
--
-- AUTO_INCREMENT for table `Sikkim`
--
ALTER TABLE `Sikkim`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Supreme_Court`
--
ALTER TABLE `Supreme_Court`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9404;
--
-- AUTO_INCREMENT for table `Tracker`
--
ALTER TABLE `Tracker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT for table `Tracker_History`
--
ALTER TABLE `Tracker_History`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=507;
--
-- AUTO_INCREMENT for table `Tracker_History_JSON`
--
ALTER TABLE `Tracker_History_JSON`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=172;
--
-- AUTO_INCREMENT for table `Tracker_JSON`
--
ALTER TABLE `Tracker_JSON`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;
--
-- AUTO_INCREMENT for table `Tracker_pdf`
--
ALTER TABLE `Tracker_pdf`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `Uttaranchal`
--
ALTER TABLE `Uttaranchal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
