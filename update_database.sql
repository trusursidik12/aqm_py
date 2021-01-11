DELETE FROM aqm_configuration WHERE data='com_hc';
INSERT INTO aqm_configuration (data,content) VALUES ('com_hc','');
DELETE FROM aqm_configuration WHERE data='baud_hc';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_hc','9600');
DELETE FROM aqm_configuration WHERE data='com_pump_pwm';
INSERT INTO aqm_configuration (data,content) VALUES ('com_pump_pwm','');
DELETE FROM aqm_configuration WHERE data='baud_pump_pwm';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_pump_pwm','9600');
DELETE FROM aqm_configuration WHERE data='pump_speed';
INSERT INTO aqm_configuration (data,content) VALUES ('pump_speed','80');
DELETE FROM aqm_configuration WHERE data='data_interval';
INSERT INTO aqm_configuration (data,content) VALUES ('data_interval','30');
DELETE FROM aqm_configuration WHERE data='graph_interval';
INSERT INTO aqm_configuration (data,content) VALUES ('graph_interval','0');
DELETE FROM aqm_configuration WHERE data='is_sampling';
INSERT INTO aqm_configuration (data,content) VALUES ('is_sampling','0');
DELETE FROM aqm_configuration WHERE data='sampler_operator_name';
INSERT INTO aqm_configuration (data,content) VALUES ('sampler_operator_name','');
DELETE FROM aqm_configuration WHERE data='id_sampling';
INSERT INTO aqm_configuration (data,content) VALUES ('id_sampling','');
DELETE FROM aqm_configuration WHERE data='start_sampling';
INSERT INTO aqm_configuration (data,content) VALUES ('start_sampling','0');

DROP TABLE IF EXISTS `aqm_sensor_values`;
CREATE TABLE `aqm_sensor_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `AIN0` double DEFAULT '0',
  `AIN1` double DEFAULT '0',
  `AIN2` double DEFAULT '0',
  `AIN3` double DEFAULT '0',
  `AIN4` double DEFAULT '0',
  `AIN5` double DEFAULT '0',
  `AIN6` double DEFAULT '0',
  `AIN7` double DEFAULT '0',
  `HC` double DEFAULT '0',
  `PM25` varchar(255) DEFAULT '',
  `PM10` varchar(255) DEFAULT '',
  `WS` text DEFAULT NULL,
  `xtimestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
INSERT INTO aqm_sensor_values (id) VALUES (1);

DROP TABLE IF EXISTS `aqm_data`;
CREATE TABLE `aqm_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_stasiun` varchar(50) NOT NULL,
  `waktu` datetime NOT NULL,
  `pm10` double DEFAULT '0',
  `pm25` double DEFAULT '0',
  `so2` double DEFAULT '0',
  `co` double DEFAULT '0',
  `o3` double DEFAULT '0',
  `no2` double DEFAULT '0',
  `hc` double DEFAULT '0',
  `ws` double DEFAULT '0',
  `wd` double DEFAULT '0',
  `humidity` double DEFAULT '0',
  `temperature` double DEFAULT '0',
  `pressure` double DEFAULT '0',
  `sr` double DEFAULT '0',
  `sent` int(11) DEFAULT '0',
  `voc` double DEFAULT '0',
  `nh3` double DEFAULT '0',
  `rain_intensity` double DEFAULT '0',
  `h2s` double DEFAULT '0',
  `cs2` double DEFAULT '0',
  `no` double DEFAULT '0',
  `stat_pm10` tinyint(4) DEFAULT 1,
  `stat_so2` tinyint(4) DEFAULT 1,
  `stat_co` tinyint(4) DEFAULT 1,
  `stat_o3` tinyint(4) DEFAULT 1,
  `stat_no2` tinyint(4) DEFAULT 1,
  `sent2` int(11) DEFAULT 0,
  `sampler_operator_name` varchar(50) NOT NULL DEFAULT '',
  `id_sampling` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `serial_ports`;
CREATE TABLE `serial_ports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `port` varchar(20) DEFAULT '',
  `description` varchar(100) DEFAULT '',
  `is_used` TINYINT DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DELETE FROM aqm_params WHERE param_id='tsp';
INSERT INTO aqm_params (param_id,caption,default_unit,molecular_mass,formula,is_view) VALUES ('tsp','TSP','ug/m3','0','round(explode(",",$PM25)[2]/1000,4)','1');
ALTER TABLE aqm_data_log ADD COLUMN tsp DOUBLE NULL AFTER pm25;
ALTER TABLE aqm_data ADD COLUMN tsp DOUBLE DEFAULT '0' AFTER pm25;

DELETE FROM aqm_configuration WHERE data='com_pm_sds019';
INSERT INTO aqm_configuration (data,content) VALUES ('com_pm_sds019','');
DELETE FROM aqm_configuration WHERE data='baud_pm_sds019';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_pm_sds019','9600');

DELETE FROM aqm_configuration WHERE data='com_gasreader';
INSERT INTO aqm_configuration (data,content) VALUES ('com_gasreader','');
DELETE FROM aqm_configuration WHERE data='baud_gasreader';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_gasreader','9600');

DELETE FROM aqm_configuration WHERE data='com_ion_science';
INSERT INTO aqm_configuration (data,content) VALUES ('com_ion_science','');
DELETE FROM aqm_configuration WHERE data='baud_ion_science';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_ion_science','9600');


DELETE FROM aqm_configuration WHERE data='selenoid_state';
INSERT INTO aqm_configuration (data,content) VALUES ('selenoid_state','q');

DELETE FROM aqm_configuration WHERE data='selenoid_names';
INSERT INTO aqm_configuration (data,content) VALUES ('selenoid_names','Sample;Zero;Span H2S;Span CS2');


DELETE FROM aqm_configuration WHERE data='selenoid_commands';
INSERT INTO aqm_configuration (data,content) VALUES ('selenoid_commands','q;w;e;r');

UPDATE aqm_configuration SET content='360' WHERE data='pump_interval';

DELETE FROM aqm_configuration WHERE data='labjack_force_on';
INSERT INTO aqm_configuration (data,content) VALUES ('labjack_force_on','0');

DELETE FROM aqm_configuration WHERE data='calibration_menu';
INSERT INTO aqm_configuration (data,content) VALUES ('calibration_menu','1');

DELETE FROM aqm_configuration WHERE data='purge_state';
INSERT INTO aqm_configuration (data,content) VALUES ('purge_state','o');

ALTER TABLE aqm_sensor_values ADD COLUMN LABJACK varchar(255)  DEFAULT '' AFTER WS;

DELETE FROM aqm_configuration WHERE data='com_rht';
INSERT INTO aqm_configuration (data,content) VALUES ('com_rht','');
DELETE FROM aqm_configuration WHERE data='baud_rht';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_rht','115200');

DELETE FROM aqm_configuration WHERE data='com_gstar_iv';
INSERT INTO aqm_configuration (data,content) VALUES ('com_gstar_iv','');
DELETE FROM aqm_configuration WHERE data='baud_gstar_iv';
INSERT INTO aqm_configuration (data,content) VALUES ('baud_gstar_iv','4800');
DELETE FROM aqm_configuration WHERE data='altitude';
INSERT INTO aqm_configuration (data,content) VALUES ('altitude','0');