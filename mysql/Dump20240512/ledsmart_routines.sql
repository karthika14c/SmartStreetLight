-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: ledsmart
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping events for database 'ledsmart'
--

--
-- Dumping routines for database 'ledsmart'
--
/*!50003 DROP PROCEDURE IF EXISTS `InsertSensorDataWithFault` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertSensorDataWithFault`(
    IN p_deviceid VARCHAR(45),
    IN p_voltage FLOAT,
    IN p_current FLOAT,
    IN p_watt FLOAT,
    IN p_tempcel FLOAT,
    IN p_tempfer FLOAT,
    IN p_light_den INT,
    IN p_light_pin INT,
    IN p_ir INT,
    IN p_web_cond VARCHAR(8)
)
BEGIN
	DECLARE last_3_light_den INT;
    DECLARE light_status INT;
    DECLARE prev_light_status INT;

    -- Fetch the last 3 values of light_den
    SELECT light_den INTO last_3_light_den 
    FROM (
        SELECT light_den 
        FROM sensor_data 
        WHERE deviceid = p_deviceid AND light_den IS NOT NULL
        ORDER BY timestamp DESC 
        LIMIT 1
    ) AS recent_light_dens;
    
    -- Get the previous light status within the specified time frame
    SELECT light_status INTO prev_light_status
    FROM sensor_data
    WHERE deviceid = p_deviceid
    AND timestamp >= DATE_SUB(NOW(), INTERVAL 6 SECOND) -- Adjust time frame as needed
    ORDER BY timestamp DESC
    LIMIT 1;

    -- If no previous light status is found, default to 0
    IF prev_light_status IS NULL THEN
        SET prev_light_status = 0;
    END IF;

    -- Compare with p_light_den and set light_status
    IF ((p_light_den BETWEEN last_3_light_den - 1 AND last_3_light_den + 1) AND p_watt > 0 AND p_light_pin = 1 ) OR ( prev_light_status = 1 AND  p_watt > 0 AND p_light_pin = 1 ) THEN
        SET light_status = 1; -- Variation detected and conditions met
    ELSE
        SET light_status = 0; -- No variation detected or conditions not met
    END IF;

    -- Insert data into sensor_data table
    INSERT INTO sensor_data (deviceid, voltage, current, watt, tempcel, tempfer, light_den, light_pin, ir, web_cond, light_status)
    VALUES (p_deviceid, p_voltage, p_current, p_watt, p_tempcel, p_tempfer, p_light_den, p_light_pin, p_ir, p_web_cond, light_status);

    -- Check if light_status is 0 and light pin is 1
    IF light_status = 0  AND p_light_pin = 1 THEN
        -- Check if there is an existing row with same deviceid, faultstatus, and fault_res_status as 0
        IF NOT EXISTS (SELECT 1 FROM fault_table WHERE faultdev_id = p_deviceid AND fault_status = 0 AND fault_resolved = 0) THEN
            -- Insert into fault_table
            INSERT INTO fault_table (faultdev_id, fault_status, fault_resolved)
            VALUES (p_deviceid, 0, 0);
        END IF;
    -- If watts more than zero and light status is 1
    ELSEIF p_watt > 0 AND light_status = 1 AND p_light_pin = 1 THEN
        -- Update fault_table for the deviceid with faultstatus and resstatus
        UPDATE fault_table 
        SET fault_status = 1, fault_resolved = 1, fault_res_time = CURRENT_TIMESTAMP 
        WHERE faultdev_id = p_deviceid AND fault_status = 0;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-12  2:31:20
