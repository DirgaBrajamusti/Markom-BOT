-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 26, 2021 at 02:25 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pmbbot`
--

-- --------------------------------------------------------

--
-- Table structure for table `pmb`
--

CREATE TABLE `pmb` (
  `id` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `asal_sekolah` varchar(255) DEFAULT NULL,
  `nomor_telepon` varchar(16) NOT NULL,
  `tahun` year(4) NOT NULL DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `jenis` varchar(10) DEFAULT 'Umum',
  `jalur` varchar(10) DEFAULT 'Undangan',
  `status` varchar(13) DEFAULT 'Belum Dikirim',
  `surat` tinyint(4) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pmb`
--

INSERT INTO `pmb` (`id`, `nama`, `asal_sekolah`, `nomor_telepon`, `tahun`, `email`, `jenis`, `jalur`, `status`, `surat`) VALUES
(1, 'Dirga Brajamusti', 'Politeknik Pos Indonesia', '6281241668963', 2021, NULL, 'Umum', 'Undangan', 'Direspon', 1),
(2, 'Test', 'Politeknik Pos Indonesia', '62085783014665', 2021, NULL, NULL, NULL, 'Belum Dikirim', 0),
(3, 'Test 2', 'Politeknik Pos Indonesia', '6289694909220', 2021, NULL, NULL, NULL, 'Belum Dikirim', 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nomor_telepon` varchar(50) NOT NULL,
  `admin` tinyint(4) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama`, `email`, `password`, `nomor_telepon`, `admin`) VALUES
(1, 'Dirga Brajamusti', 'dirgaizan@yahoo.com', 'pbkdf2:sha256:150000$RUdBEzeB$3bf546e5bb532145d2db92cac05d15a4323f8380c5e82fc50ba8d44ddcbcc1a8', '6281241668963', 1),
(2, 'poltekpos.stimlog@gmail.com', 'poltekpos.stimlog@gmail.com', 'pbkdf2:sha256:150000$RUdBEzeB$3bf546e5bb532145d2db92cac05d15a4323f8380c5e82fc50ba8d44ddcbcc1a8', '6289694909220', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pmb`
--
ALTER TABLE `pmb`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pmb`
--
ALTER TABLE `pmb`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
