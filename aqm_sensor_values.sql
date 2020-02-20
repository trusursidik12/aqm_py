-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 18 Feb 2020 pada 04.35
-- Versi server: 10.4.11-MariaDB
-- Versi PHP: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `trusur_aqm`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `aqm_sensor_values`
--

DROP TABLE IF EXISTS `aqm_sensor_values`;
CREATE TABLE `aqm_sensor_values` (
  `id` int(11) NOT NULL,
  `AIN0` double DEFAULT NULL,
  `AIN1` double DEFAULT NULL,
  `AIN2` double DEFAULT NULL,
  `AIN3` double DEFAULT NULL,
  `PM25` varchar(255) NOT NULL,
  `PM10` varchar(255) NOT NULL,
  `WS` varchar(255) DEFAULT NULL,
  `xtimestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `aqm_sensor_values`
--

INSERT INTO `aqm_sensor_values` (`id`, `AIN0`, `AIN1`, `AIN2`, `AIN3`, `PM25`, `PM10`, `WS`, `xtimestamp`) VALUES
(1, 4.302363395690918, 4.293194770812988, 1.502382755279541, 1.7023757696151733, '', 'b\'000.040,2.0,+28.3,067,1007.4,00,*01543\\r\\n\'', '2020-02-18 10:31:35.519638;255;29.702;82.0;71;80.2;0;0;302;76;0.0;0;0;0.0;2127-15-31;0.0;0.0;0.0;0.001;0.0;0.0;0;4.8515625;0;193;07:23;17:02;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;', '2020-02-18 03:31:35'),
(2, 3.9226908683776855, 4.010066032409668, 1.58293616771698, 1.7379157543182373, '', 'b\'000.040,2.0,+28.3,066,1007.3,00,*01541\\r\\n\'', '2020-02-18 10:31:12.245940;255;29.703;82.0;71;80.2;0;0;302;76;0.0;0;0;0.0;2127-15-31;0.0;0.0;0.0;0.001;0.0;0.0;0;4.8515625;0;193;07:23;17:02;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;', '2020-02-18 03:31:12');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `aqm_sensor_values`
--
ALTER TABLE `aqm_sensor_values`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `aqm_sensor_values`
--
ALTER TABLE `aqm_sensor_values`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;
--Datetime,BarTrend,Barometer,TempIn,HumIn,TempOut,WindSpeed,WindSpeed10Min,WindDir,HumOut,RainRate,UV,SolarRad,RainStorm,StormStartDate,RainDay,RainMonth,RainYear,ETDay,ETMonth,ETYear,BatteryStatus,BatteryVolts,ForecastIcon,ForecastRuleNo,SunRise,SunSet,AlarmInFallBarTrend,AlarmInRisBarTrend,AlarmInLowTemp,AlarmInHighTemp,AlarmInLowHum,AlarmInHighHum,AlarmInTime,AlarmRainHighRate,AlarmRain15min,AlarmRain24hour,AlarmRainStormTotal,AlarmRainETDaily,AlarmOutLowTemp,AlarmOutHighTemp,AlarmOutWindSpeed,AlarmOut10minAvgSpeed,AlarmOutLowDewpoint,AlarmOutHighDewPoint,AlarmOutHighHeat,AlarmOutLowWindChill,AlarmOutHighTHSW,AlarmOutHighSolarRad,AlarmOutHighUV,AlarmOutUVDose,AlarmOutUVDoseEnabled,AlarmEx01LowTemp,AlarmEx01HighTemp,AlarmEx01LowHum,AlarmEx01HighHum,AlarmEx02LowTemp,AlarmEx02HighTemp,AlarmEx02LowHum,AlarmEx02HighHum,AlarmEx03LowTemp,AlarmEx03HighTemp,AlarmEx03LowHum,AlarmEx03HighHum,AlarmEx04LowTemp,AlarmEx04HighTemp,AlarmEx04LowHum,AlarmEx04HighHum,AlarmEx05LowTemp,AlarmEx05HighTemp,AlarmEx05LowHum,AlarmEx05HighHum,AlarmEx06LowTemp,AlarmEx06HighTemp,AlarmEx06LowHum,AlarmEx06HighHum,AlarmEx07LowTemp,AlarmEx07HighTemp,AlarmEx07LowHum,AlarmEx07HighHum,Alarm01LowLeafWet,Alarm01HighLeafWet,Alarm01LowSoilMois,Alarm01HighSoilMois,Alarm01LowLeafTemp,Alarm01HighLeafTemp,Alarm01LowSoilTemp,Alarm01HighSoilTemp,Alarm02LowLeafWet,Alarm02HighLeafWet,Alarm02LowSoilMois,Alarm02HighSoilMois,Alarm02LowLeafTemp,Alarm02HighLeafTemp,Alarm02LowSoilTemp,Alarm02HighSoilTemp,Alarm03LowLeafWet,Alarm03HighLeafWet,Alarm03LowSoilMois,Alarm03HighSoilMois,Alarm03LowLeafTemp,Alarm03HighLeafTemp,Alarm03LowSoilTemp,Alarm03HighSoilTemp,Alarm04LowLeafWet,Alarm04HighLeafWet,Alarm04LowSoilMois,Alarm04HighSoilMois,Alarm04LowLeafTemp,Alarm04HighLeafTemp,Alarm04LowSoilTemp,Alarm04HighSoilTemp,ExtraTemps01,ExtraTemps02,ExtraTemps03,ExtraTemps04,ExtraTemps05,ExtraTemps06,ExtraTemps07,LeafTemps01,LeafTemps02,LeafTemps03,LeafTemps04,SoilTemps01,SoilTemps02,SoilTemps03,SoilTemps04,HumExtra01,HumExtra02,HumExtra03,HumExtra04,HumExtra05,HumExtra06,HumExtra07,LeafWetness01,LeafWetness02,LeafWetness03,LeafWetness04,SoilMoist01,SoilMoist02,SoilMoist03,SoilMoist04
