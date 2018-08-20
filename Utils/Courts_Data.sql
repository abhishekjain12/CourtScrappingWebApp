-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 13, 2018 at 05:03 PM
-- Server version: 5.7.23-0ubuntu0.16.04.1
-- PHP Version: 7.0.30-0ubuntu0.16.04.1

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
-- Table structure for table `Arunachal_HC`
--

CREATE TABLE `Arunachal_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `subject` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `BombayCivil_HC`
--

CREATE TABLE `BombayCivil_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `coram` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `CalcuttaOS_HC`
--

CREATE TABLE `CalcuttaOS_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `judgment_date` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Chattisgarh_HC`
--

CREATE TABLE `Chattisgarh_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `text_data` longtext,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `delhi_HC`
--

CREATE TABLE `delhi_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `corrigendum` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `haryana_HC`
--

CREATE TABLE `haryana_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `hp_HC`
--

CREATE TABLE `hp_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `judgment_date` text,
  `coram` text,
  `type` text,
  `status` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Hyderabad_HC`
--

CREATE TABLE `Hyderabad_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `text_data` longtext,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Jammu_HC`
--

CREATE TABLE `Jammu_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `text_data` longtext,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `karnataka_HC`
--

CREATE TABLE `karnataka_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `bench` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Kerala_HC`
--

CREATE TABLE `Kerala_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `text_data` longtext,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Madras_HC`
--

CREATE TABLE `Madras_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `text_data` longtext,
  `text_file` text,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Manipur_HC`
--

CREATE TABLE `Manipur_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `meghalaya_HC`
--

CREATE TABLE `meghalaya_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `corrigendum` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `mizoram_HC`
--

CREATE TABLE `mizoram_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `mp_HC`
--

CREATE TABLE `mp_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `petitioner_advocate` text,
  `respondent` text,
  `respondent_advocate` text,
  `judgment_date` text,
  `disposal_date` text,
  `judge_name` text,
  `bench` varchar(5) DEFAULT NULL,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `nagaland_HC`
--

CREATE TABLE `nagaland_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `judgment_date` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ORISSA_HC`
--

CREATE TABLE `ORISSA_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `corrigendum` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sikkim_HC`
--

CREATE TABLE `sikkim_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Srinagar_HC`
--

CREATE TABLE `Srinagar_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `judge_name` text,
  `text_data` longtext,
  `text_file` text CHARACTER SET utf8,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SupremeCourt`
--

CREATE TABLE `SupremeCourt` (
  `id` int(11) NOT NULL,
  `diary_number` varchar(100) DEFAULT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `petitioner_advocate` varchar(500) DEFAULT NULL,
  `respondent_advocate` varchar(500) DEFAULT NULL,
  `judgment_date` text,
  `bench` mediumtext,
  `judge_name` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Tracker`
--

CREATE TABLE `Tracker` (
  `id` int(11) NOT NULL,
  `Name` varchar(500) DEFAULT NULL,
  `No_Cases` bigint(20) DEFAULT NULL,
  `Start_Date` varchar(40) DEFAULT NULL,
  `End_Date` varchar(40) DEFAULT NULL,
  `No_Error` int(11) DEFAULT NULL,
  `No_Year_Error` int(11) DEFAULT NULL,
  `No_Year_NoData` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `UTTARANCHAL_HC`
--

CREATE TABLE `UTTARANCHAL_HC` (
  `id` int(11) NOT NULL,
  `case_no` text,
  `petitioner` text,
  `respondent` text,
  `judgment_date` text,
  `corrigendum` text,
  `pdf_data` longtext,
  `pdf_file` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Arunachal_HC`
--
ALTER TABLE `Arunachal_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `BombayCivil_HC`
--
ALTER TABLE `BombayCivil_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `CalcuttaOS_HC`
--
ALTER TABLE `CalcuttaOS_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Chattisgarh_HC`
--
ALTER TABLE `Chattisgarh_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `delhi_HC`
--
ALTER TABLE `delhi_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `haryana_HC`
--
ALTER TABLE `haryana_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hp_HC`
--
ALTER TABLE `hp_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Hyderabad_HC`
--
ALTER TABLE `Hyderabad_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `karnataka_HC`
--
ALTER TABLE `karnataka_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Kerala_HC`
--
ALTER TABLE `Kerala_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Madras_HC`
--
ALTER TABLE `Madras_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Manipur_HC`
--
ALTER TABLE `Manipur_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `meghalaya_HC`
--
ALTER TABLE `meghalaya_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mizoram_HC`
--
ALTER TABLE `mizoram_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mp_HC`
--
ALTER TABLE `mp_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `nagaland_HC`
--
ALTER TABLE `nagaland_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ORISSA_HC`
--
ALTER TABLE `ORISSA_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sikkim_HC`
--
ALTER TABLE `sikkim_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Srinagar_HC`
--
ALTER TABLE `Srinagar_HC`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `SupremeCourt`
--
ALTER TABLE `SupremeCourt`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Tracker`
--
ALTER TABLE `Tracker`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `UTTARANCHAL_HC`
--
ALTER TABLE `UTTARANCHAL_HC`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Arunachal_HC`
--
ALTER TABLE `Arunachal_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `BombayCivil_HC`
--
ALTER TABLE `BombayCivil_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `CalcuttaOS_HC`
--
ALTER TABLE `CalcuttaOS_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Chattisgarh_HC`
--
ALTER TABLE `Chattisgarh_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `delhi_HC`
--
ALTER TABLE `delhi_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `haryana_HC`
--
ALTER TABLE `haryana_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `hp_HC`
--
ALTER TABLE `hp_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `Hyderabad_HC`
--
ALTER TABLE `Hyderabad_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `karnataka_HC`
--
ALTER TABLE `karnataka_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `Kerala_HC`
--
ALTER TABLE `Kerala_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Madras_HC`
--
ALTER TABLE `Madras_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Manipur_HC`
--
ALTER TABLE `Manipur_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=106;
--
-- AUTO_INCREMENT for table `meghalaya_HC`
--
ALTER TABLE `meghalaya_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mizoram_HC`
--
ALTER TABLE `mizoram_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mp_HC`
--
ALTER TABLE `mp_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=218;
--
-- AUTO_INCREMENT for table `nagaland_HC`
--
ALTER TABLE `nagaland_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `ORISSA_HC`
--
ALTER TABLE `ORISSA_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `sikkim_HC`
--
ALTER TABLE `sikkim_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `Srinagar_HC`
--
ALTER TABLE `Srinagar_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `SupremeCourt`
--
ALTER TABLE `SupremeCourt`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `Tracker`
--
ALTER TABLE `Tracker`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `UTTARANCHAL_HC`
--
ALTER TABLE `UTTARANCHAL_HC`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
