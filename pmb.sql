-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.8-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.1.0.6116
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for pmbbot
CREATE DATABASE IF NOT EXISTS `pmbbot` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `pmbbot`;

-- Dumping structure for table pmbbot.pmb
CREATE TABLE IF NOT EXISTS `pmb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  `asal_sekolah` varchar(255) DEFAULT NULL,
  `nomor_telepon` varchar(16) NOT NULL,
  `tahun` year(4) NOT NULL DEFAULT year(current_timestamp()),
  `email` varchar(255) DEFAULT NULL,
  `jenis` varchar(10) DEFAULT 'Umum',
  `jalur` varchar(10) DEFAULT 'Undangan',
  `status` varchar(13) DEFAULT 'Belum Dikirim',
  `surat` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table pmbbot.pmb: ~1 rows (approximately)
/*!40000 ALTER TABLE `pmb` DISABLE KEYS */;
INSERT INTO `pmb` (`id`, `nama`, `asal_sekolah`, `nomor_telepon`, `tahun`, `email`, `jenis`, `jalur`, `status`, `surat`) VALUES
	(1, 'Dirga Brajamusti', 'Politeknik Pos Indonesia', '6281241668963', '2021', NULL, 'Umum', 'Undangan', 'Direspon', 1),
	(2, 'Test', 'Politeknik Pos Indonesia', '62085783014665', '2021', NULL, NULL, NULL, 'Belum Dikirim', 0),
	(3, 'Test 2', 'Politeknik Pos Indonesia', '6289694909220', '2021', NULL, NULL, NULL, 'Belum Dikirim', 0);
/*!40000 ALTER TABLE `pmb` ENABLE KEYS */;

-- Dumping structure for table pmbbot.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nomor_telepon` varchar(50) NOT NULL,
  `admin` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table pmbbot.users: ~0 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `nama`, `email`, `password`, `nomor_telepon`, `admin`) VALUES
	(1, 'Dirga Brajamusti', 'dirgaizan@yahoo.com', 'pbkdf2:sha256:150000$RUdBEzeB$3bf546e5bb532145d2db92cac05d15a4323f8380c5e82fc50ba8d44ddcbcc1a8', '6281241668963', 1),
	(2, 'poltekpos.stimlog@gmail.com', 'poltekpos.stimlog@gmail.com', 'pbkdf2:sha256:150000$RUdBEzeB$3bf546e5bb532145d2db92cac05d15a4323f8380c5e82fc50ba8d44ddcbcc1a8', '6289694909220', 1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
