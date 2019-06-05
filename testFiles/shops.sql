-- phpMyAdmin SQL Dump
-- version 4.7.8
-- https://www.phpmyadmin.net/
--
-- Host: 158.69.238.64:3306
-- Generation Time: Apr 08, 2019 at 06:23 AM
-- Server version: 5.7.20-log
-- PHP Version: 7.1.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db18025`
--

-- --------------------------------------------------------

--
-- Table structure for table `shops`
--

CREATE TABLE `shops` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `item` varchar(255) NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `shops`
--

INSERT INTO `shops` (`id`, `name`, `item`, `price`) VALUES
(1, 'TwentyFourSeven', 'bread', 30),
(2, 'TwentyFourSeven', 'water', 15),
(3, 'RobsLiquor', 'bread', 30),
(4, 'RobsLiquor', 'water', 15),
(5, 'LTDgasoline', 'bread', 30),
(6, 'LTDgasoline', 'water', 15),
(7, 'Bar', 'wine', 50),
(8, 'Bar', 'beer', 50),
(9, 'Bar', 'vodka', 50),
(19, 'Bar', 'tequila', 40),
(20, 'Bar', 'whisky', 40),
(24, 'TwentyFourSeven', 'cocacola', 25),
(25, 'RobsLiquor', 'cocacola', 25),
(26, 'LTDgasoline', 'cocacola', 25),
(27, 'TwentyFourSeven', 'icetea', 20),
(28, 'RobsLiquor', 'icetea', 20),
(29, 'LTDgasoline', 'icetea', 20),
(36, 'TwentyFourSeven', 'binoculars', 1000),
(37, 'RobsLiquor', 'binoculars', 1000),
(38, 'LTDgasoline', 'binoculars', 1000),
(39, 'LTDgasoline', 'croquettes', 1000),
(40, 'LTDgasoline', 'plongee1', 250),
(41, 'RobsLiquor', 'plongee1', 250),
(42, 'TwentyFourSeven', 'plongee1', 250),
(43, 'LTDgasoline', 'plongee2', 350),
(44, 'RobsLiquor', 'plongee2', 350),
(45, 'TwentyFourSeven', 'plongee2', 350);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `shops`
--
ALTER TABLE `shops`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `shops`
--
ALTER TABLE `shops`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
