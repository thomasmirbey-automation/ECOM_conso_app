-- MariaDB dump 10.19  Distrib 10.11.4-MariaDB, for debian-linux-gnu (aarch64)
--
-- Host: localhost    Database: ecomddb
-- ------------------------------------------------------
-- Server version	10.11.4-MariaDB-1~deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'ecomddb'
--
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ADD_mesure` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `ADD_mesure`(
	IN `_valeur` INT,
	IN `_ip` VARCHAR(50),
	IN `_unite` VARCHAR(50)
)
BEGIN
	FOR voie1 IN (SELECT ID FROM objets WHERE IP = _ip )
	DO
	
		SET @DATE = NOW();
		INSERT INTO mesures (ID_OBJETS, HORODATAGE , VALEUR,UNITE ) VALUES ( voie1.ID,@DATE, _valeur,_unite);
		
	END FOR;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `DEV_UPDATE_priority` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `DEV_UPDATE_priority`()
BEGIN
	DECLARE temporaryValue INTEGER;
	DECLARE SUM_conso INTEGER;
	DECLARE SUM_prod INTEGER;
	DROP TEMPORARY TABLE IF EXISTS objectsValues;


	CREATE TEMPORARY TABLE objectsValues (valeurConso INT, valeurProd INT);
	SET @PREVIOUS = DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 HOUR), '%Y-%m-%d %H:00:00');
	SET @NOW = DATE_FORMAT(NOW(),'%Y-%m-%d %H:00:00');
	
	FOR voie1 IN (SELECT ID FROM maison )
	DO
		FOR voie2 IN (SELECT ID FROM objets WHERE ID_MAISON = voie1.ID AND TYPE = "CONSO" )
		DO
			SELECT voie2.ID;
	    	SELECT SUM(VALEUR) INTO temporaryValue
			FROM mesures
			WHERE (HORODATAGE BETWEEN @PREVIOUS AND @NOW) AND ID_OBJETS = voie2.ID;
	   	INSERT INTO objectsValues (valeurConso) VALUE (temporaryValue);
	   	
		END FOR;
		FOR voie3 IN (SELECT ID FROM objets WHERE ID_MAISON = voie1.ID AND TYPE = "PROD" )
		DO
		
			SELECT voie3.ID;
	    	SELECT SUM(VALEUR) INTO temporaryValue
			FROM mesures
			WHERE (HORODATAGE BETWEEN @PREVIOUS AND @NOW) AND ID_OBJETS = voie3.ID;
	   	INSERT INTO objectsValues (valeurProd) VALUE (temporaryValue);
		
		END FOR;
		SELECT SUM(valeurConso) INTO SUM_conso
		FROM objectsValues;
		SELECT SUM(valeurProd) INTO SUM_prod
		FROM objectsValues;
		INSERT INTO conso_maison ( ID_MAISON, HORODATAGE, CONSO, PROD) VALUES (voie1.ID , @NOW, SUM_conso, SUM_prod);
		SELECT * from conso_maison;
	END FOR;
	
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GET_conso_maison` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `GET_conso_maison`(
	IN `_idMaison` VARCHAR(50)
)
BEGIN
	SET @PREVIOUS = DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 DAY), '%Y-%m-%d');
	SET @NOW = DATE_FORMAT(NOW(),'%Y-%m-%d');

	SELECT CONSO,PROD, DATE_FORMAT(HORODATAGE,'%H')  AS HEURE , (PROD-CONSO) AS DIFFERENCE FROM conso_maison WHERE (HORODATAGE BETWEEN @PREVIOUS AND @NOW) AND ID_MAISON = _idMaison;
	
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GET_maison` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `GET_maison`()
BEGIN
	SELECT * FROM maison;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GET_mesures` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `GET_mesures`(
	IN `_idMaison` INT
)
BEGIN
	DROP TEMPORARY TABLE IF EXISTS table_;
   CREATE TEMPORARY TABLE table_ ( ID_OBJETS INT, VALEUR CHAR(240), UNITE CHAR(240), HORODATAGE TIMESTAMP);
   
	
    FOR voie1 IN (SELECT ID FROM objets WHERE ID_MAISON = _idMaison) 
	 DO
        FOR voie2 IN (SELECT * FROM mesures WHERE ID_OBJETS = voie1.ID) 
	 		DO
        	INSERT INTO table_ (ID_OBJETS, VALEUR, UNITE, HORODATAGE ) VALUES ( voie1.ID, voie2.VALEUR, voie2.UNITE, voie2.HORODATAGE);
        	END FOR;
    END FOR;
	SELECT * FROM table_;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GET_objets` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `GET_objets`(
	IN `_idMaison` INT
)
BEGIN
	
	SELECT NOM, ETAT, IP FROM objets WHERE ID_MAISON = _idMaison  AND TYPE = "CONSO";
	
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `GET_objet_mesures` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `GET_objet_mesures`(
	IN `_ip` VARCHAR(50)
)
BEGIN
	SET @PREVIOUS = DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 DAY), '%Y-%m-%d');
	SET @NOW = DATE_FORMAT(NOW(),'%Y-%m-%d'); 
	
	
	FOR voie1 IN (SELECT ID FROM objets WHERE IP = _ip) 
	DO
	
		SELECT * FROM mesures WHERE ID_OBJETS = voie1.ID AND 	(HORODATAGE BETWEEN @PREVIOUS AND @NOW);
		
	END FOR;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SET_ipObjet` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `SET_ipObjet`(
	IN `_id` INT,
	IN `_ip` VARCHAR(50)
)
BEGIN
	UPDATE objets
	SET IP = _ip
	WHERE ID = _id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SET_priseState` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`yohannpca` PROCEDURE `SET_priseState`(
	IN `_state` VARCHAR(50),
	IN `_idMaison` INT,
	IN `_ip` VARCHAR(50)
)
BEGIN
	UPDATE objets
	SET ETAT = _state
	WHERE IP = _ip AND ID_MAISON = _idMaison;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-07 11:34:27
