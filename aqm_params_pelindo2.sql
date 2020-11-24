-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Nov 2020 pada 05.18
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
-- Struktur dari tabel `aqm_params`
--

CREATE TABLE `aqm_params` (
  `id` int(11) NOT NULL,
  `param_id` varchar(10) NOT NULL,
  `caption` varchar(100) NOT NULL,
  `default_unit` varchar(10) NOT NULL,
  `molecular_mass` double NOT NULL,
  `formula` varchar(255) DEFAULT NULL,
  `gain` double DEFAULT 0,
  `offset` double DEFAULT 0,
  `is_view` smallint(6) NOT NULL,
  `is_graph` smallint(6) DEFAULT 0,
  `xtimestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `aqm_params`
--

INSERT INTO `aqm_params` (`id`, `param_id`, `caption`, `default_unit`, `molecular_mass`, `formula`, `gain`, `offset`, `is_view`, `is_graph`, `xtimestamp`) VALUES
(1, 'pm10', 'PM10', 'ug/m3', 0, 'round(explode(\",\",$PM25)[1]/10000,5)', 0, 0, 1, 0, '2020-11-11 01:07:47'),
(2, 'pm10_flow', 'PM10 Flow', 'l/mnt', 0, 'substr($PM10,10,3)', 0, 0, 0, 0, '2020-11-11 02:20:36'),
(3, 'pm25', 'PM2.5', 'ug/m3', 0, 'round(explode(\",\",$PM25)[0]/10000,5)', 0, 0, 1, 0, '2020-11-11 01:07:50'),
(4, 'pm25_flow', 'PM2.5 Flow', 'l/mnt', 0, 'substr($PM25,10,3)', 0, 0, 0, 0, '2020-11-11 01:02:14'),
(5, 'so2', 'SO2', 'ppm', 64.06, 'round((($AIN0 - 1.744315)/0.002827*20)+(($AIN1 - 1.618291)/-0.01114766*0.14)+(($AIN2 - 1.620738)/-0.02193604*-0.066)+(($AIN3 - 1.632592)/0.000221*0.01825),3)', 1, 0, 1, 0, '2020-11-22 13:16:57'),
(6, 'co', 'CO', 'ppm', 28.01, 'round((($AIN0 - 1.744315)/0.002827*0.05)+(($AIN1 - 1.618291)/-0.01114766*0.1)+(($AIN2 - 1.620738)/-0.02193604*0.2)+(($AIN3 - 1.632592)/0.000221*500),3)', 1, 0, 1, 0, '2020-11-22 13:37:08'),
(7, 'o3', 'O3', 'ppm', 48, 'round((($AIN0 - 1.744315)/0.002827*0)+(($AIN1 - 1.618291)/-0.01114766*1)+(($AIN2 - 1.620738)/-0.02193604*5)+(($AIN3 - 1.632592)/0.000221*0.000125),3)', 1, 0, 1, 0, '2020-11-22 13:37:18'),
(8, 'no2', 'NO2', 'ppm', 46.01, 'round((($AIN0 - 1.744315)/0.002827*0.004)+(($AIN1 - 1.618291)/-0.01114766*20)+(($AIN2 - 1.620738)/-0.02193604*0.1)+(($AIN3 - 1.632592)/0.000221*0.002),3)', 1, 0, 1, 0, '2020-11-22 13:37:32'),
(9, 'voc', 'VOC', 'ppm', 78.9516, '0', 0, 0, 0, 0, '2020-03-16 03:00:29'),
(10, 'h2s', 'H2S', 'ppm', 34.08, 'round(3.2 * ((8 + $gain) * $AIN0) - $offset, 3)', 0, 0, 0, 0, '2020-03-16 03:00:29'),
(11, 'hc', 'HC', 'ppm', 13.0186, 'round($HC / 1000, 3)', 0, 0, 0, 0, '2020-11-21 13:19:02'),
(12, 'cs2', 'CS2', 'ppm', 76.1407, 'round(1.2 * ((24 + $gain) * $AIN2) - $offset, 3)', 0, 0, 0, 0, '2020-03-16 03:00:29'),
(13, 'Barometer', 'Tekanan', 'MBar', 0, 'round((explode(\";\",$WS)[2] * 33.8639),2)', 0, 0, 1, 0, '2020-05-28 05:33:01'),
(14, 'TempIn', 'Temperatur Dalam', 'Celcius', 0, 'explode(\";\",$WS)[3]', 0, 0, 0, 0, '2020-02-18 22:44:38'),
(15, 'HumIn', 'Kelembaban Dalam', '%', 0, 'explode(\";\",$WS)[4]', 0, 0, 0, 0, '2020-02-18 22:44:38'),
(16, 'TempOut', 'Temperatur', 'Celcius', 0, 'explode(\";\",$WS)[5]', 0, 0, 1, 0, '2020-05-28 05:35:11'),
(17, 'WindSpeed', 'Kec. Angin', 'Km/jam', 0, 'explode(\";\",$WS)[6]', 0, 0, 1, 0, '2020-05-28 00:54:59'),
(18, 'WindSpeed1', 'Kec. Angin 10Min', 'Km/jam', 0, 'explode(\";\",$WS)[7]', 0, 0, 0, 0, '2020-03-01 13:43:56'),
(19, 'WindDir', 'Arah Angin', '°', 0, 'explode(\";\",$WS)[8]', 0, 0, 1, 0, '2020-05-28 00:54:59'),
(20, 'HumOut', 'Kelembaban', '%', 0, 'explode(\";\",$WS)[9]', 0, 0, 1, 0, '2020-05-28 00:54:59'),
(21, 'RainRate', 'Tingkat Hujan', 'mm/jam', 0, 'explode(\";\",$WS)[10]', 0, 0, 0, 0, '2020-04-16 00:22:35'),
(22, 'UV', 'UV', '', 0, 'explode(\";\",$WS)[11]', 0, 0, 0, 0, '2020-04-16 00:22:35'),
(23, 'SolarRad', 'Solar Radiasi', 'watt/m2', 0, 'explode(\";\",$WS)[12]', 0, 0, 1, 0, '2020-05-28 00:54:59'),
(24, 'RainDay', 'Curah Hujan', 'mm/jam', 0, 'explode(\";\",$WS)[15]', 0, 0, 1, 0, '2020-05-28 00:54:59'),
(25, 'pm10_bar', 'Tekanan', 'MBar', 0, 'explode(\",\",$PM10)[4]', 0, 0, 0, 0, '2020-03-12 03:16:13'),
(26, 'pm10_humid', 'Kelembaban', '%', 0, 'explode(\",\",$PM10)[3]', 0, 0, 0, 0, '2020-03-12 03:16:13'),
(27, 'pm10_temp', 'Suhu', 'Celcius', 0, 'explode(\",\",$PM10)[2]', 0, 0, 0, 0, '2020-03-12 03:16:13'),
(28, 'pm25_bar', 'Tekanan', 'MBar', 0, 'explode(\",\",$PM25)[4]', 0, 0, 0, 0, '2020-03-06 02:11:29'),
(29, 'pm25_humid', 'Kelembaban', '%', 0, 'explode(\",\",$PM25)[3]', 0, 0, 0, 0, '2020-03-06 02:11:29'),
(30, 'pm25_temp', 'Suhu', 'Celcius', 0, 'explode(\",\",$PM25)[2]', 0, 0, 0, 0, '2020-03-06 02:11:29'),
(32, 'tsp', 'TSP', 'ug/m3', 0, 'round(explode(\",\",$PM25)[2]/1000,4)', 0, 0, 1, 0, '2020-11-11 01:21:02');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `aqm_params`
--
ALTER TABLE `aqm_params`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `param_id` (`param_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `aqm_params`
--
ALTER TABLE `aqm_params`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
