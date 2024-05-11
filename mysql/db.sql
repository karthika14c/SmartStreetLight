CREATE DATABASE `ledsmart` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `fault_table` (
  `idfault` int NOT NULL AUTO_INCREMENT,
  `faultdev_id` varchar(45) DEFAULT NULL,
  `reporttime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fault_status` int DEFAULT NULL,
  `fault_resolved` int DEFAULT NULL,
  `fault_res_time` datetime DEFAULT NULL,
  PRIMARY KEY (`idfault`)
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `loc_table` (
  `idloc` int NOT NULL AUTO_INCREMENT,
  `deviceid` varchar(45) NOT NULL,
  `lat` varchar(45) NOT NULL,
  `lon` varchar(45) NOT NULL,
  `light_service` varchar(45) DEFAULT NULL,
  `location` varchar(45) NOT NULL,
  PRIMARY KEY (`idloc`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `sensor_data` (
  `idsensor_data` int NOT NULL AUTO_INCREMENT,
  `deviceid` varchar(45) NOT NULL,
  `voltage` float DEFAULT NULL,
  `current` float DEFAULT NULL,
  `watt` float DEFAULT NULL,
  `tempcel` float DEFAULT NULL,
  `tempfer` float DEFAULT NULL,
  `light_den` int DEFAULT NULL,
  `light_pin` int DEFAULT NULL,
  `ir` int DEFAULT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `light_status` int DEFAULT NULL,
  `web_cond` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`idsensor_data`)
) ENGINE=InnoDB AUTO_INCREMENT=21669 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
