-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 21, 2019 at 01:29 AM
-- Server version: 5.7.24-0ubuntu0.18.04.1
-- PHP Version: 7.2.10-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `new_courts_data`
--

-- --------------------------------------------------------

--
-- Table structure for table `alerts`
--

CREATE TABLE `alerts` (
  `id` int(11) NOT NULL,
  `court_name` varchar(25) DEFAULT NULL,
  `bench` varchar(25) DEFAULT NULL,
  `start_date` varchar(25) DEFAULT NULL,
  `end_date` varchar(25) DEFAULT NULL,
  `error_message` longtext,
  `case_id` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `kolkata`
--

CREATE TABLE `kolkata` (
  `id` int(11) NOT NULL,
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
  `bench` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tracker`
--

CREATE TABLE `tracker` (
  `id` int(11) NOT NULL,
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
  `status` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tracker_history`
--

CREATE TABLE `tracker_history` (
  `id` int(11) NOT NULL,
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
  `status` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alerts`
--
ALTER TABLE `alerts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kolkata`
--
ALTER TABLE `kolkata`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tracker`
--
ALTER TABLE `tracker`
  ADD PRIMARY KEY (`id`),
  ADD KEY `name` (`court_name`),
  ADD KEY `bench` (`bench`);

--
-- Indexes for table `tracker_history`
--
ALTER TABLE `tracker_history`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alerts`
--
ALTER TABLE `alerts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `kolkata`
--
ALTER TABLE `kolkata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `tracker`
--
ALTER TABLE `tracker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `tracker_history`
--
ALTER TABLE `tracker_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
