-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Nov 2020 pada 05.17
-- Versi server: 10.4.11-MariaDB
-- Versi PHP: 7.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trusur_aqm`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `aqm_configuration`
--

CREATE TABLE `aqm_configuration` (
  `id` int(11) NOT NULL,
  `data` varchar(50) DEFAULT NULL,
  `content` varchar(200) DEFAULT NULL,
  `is_view` smallint(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `aqm_configuration`
--

INSERT INTO `aqm_configuration` (`id`, `data`, `content`, `is_view`) VALUES
(1, 'device_id', 'TRUSUR', NULL),
(2, 'server', '127.0.0.1', NULL),
(3, 'sta_id', 'TRUSUR', NULL),
(4, 'sta_nama', 'TRUSUR', NULL),
(5, 'sta_alamat', '', NULL),
(6, 'sta_kota', '', NULL),
(7, 'sta_prov', '', NULL),
(8, 'sta_lat', '-6.0', NULL),
(9, 'sta_lon', '106.0', NULL),
(10, 'com_pm10', '', NULL),
(11, 'baud_pm10', '9600', NULL),
(12, 'com_pm25', '', NULL),
(13, 'baud_pm25', '9600', NULL),
(14, 'com_hc', '', NULL),
(15, 'baud_hc', '9600', NULL),
(16, 'com_ws', '', NULL),
(17, 'baud_ws', '19200', NULL),
(18, 'com_airmar', '', NULL),
(19, 'baud_airmar', '4800', NULL),
(20, 'controller', '', NULL),
(21, 'controller_baud', '9600', NULL),
(22, 'com_modem', '', NULL),
(23, 'baud_modem', '115200', NULL),
(24, 'pump_interval', '120', NULL),
(25, 'pump_state', '0', NULL),
(26, 'pump_last', '2020-11-24 11:08:34', NULL),
(27, 'pump_control', '1', NULL),
(28, 'com_pump_pwm', '', NULL),
(29, 'baud_pump_pwm', '9600', NULL),
(30, 'pump_speed', '80', NULL),
(31, 'data_interval', '30', NULL),
(32, 'graph_interval', '0', NULL),
(33, 'is_sampling', '0', NULL),
(34, 'sampler_operator_name', '', NULL),
(35, 'id_sampling', '', NULL),
(36, 'start_sampling', '0', NULL),
(37, 'e_pm10', '1', NULL),
(38, 'e_pm25', '0', NULL),
(39, 'e_so2', '1', NULL),
(40, 'e_co', '1', NULL),
(41, 'e_o3', '1', NULL),
(42, 'e_no2', '1', NULL),
(43, 'e_hc', '0', NULL),
(44, 'e_ws', '1', NULL),
(45, 'e_wd', '1', NULL),
(46, 'e_humidity', '0', NULL),
(47, 'e_temperature', '1', NULL),
(48, 'e_pressure', '1', NULL),
(49, 'e_sr', '0', NULL),
(50, 'e_voc', '1', NULL),
(51, 'e_nh3', '0', NULL),
(52, 'e_rain_intensity', '0', NULL),
(53, 'e_no', '0', NULL),
(54, 'gas_simulation', '1', NULL),
(55, 'weather_simulation', '1', NULL),
(56, 'weather_city_id', '1642911', NULL),
(57, 'com_pm_sds019', '', NULL),
(58, 'baud_pm_sds019', '9600', NULL),
(59, 'com_gasreader', 'COM3', NULL),
(60, 'baud_gasreader', '9600', NULL);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `aqm_configuration`
--
ALTER TABLE `aqm_configuration`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `aqm_configuration`
--
ALTER TABLE `aqm_configuration`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
