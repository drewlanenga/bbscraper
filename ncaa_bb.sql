# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: localhost (MySQL 5.5.27)
# Database: ncaa_bb
# Generation Time: 2017-08-18 23:33:53 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table boxscores
# ------------------------------------------------------------

CREATE TABLE `boxscores` (
  `gameid` int(11) NOT NULL,
  `teamid` int(11) NOT NULL,
  `playerid` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `min` int(11) NOT NULL,
  `fgm` int(11) NOT NULL,
  `fga` int(11) NOT NULL,
  `threem` int(11) NOT NULL,
  `threea` int(11) NOT NULL,
  `ftm` int(11) NOT NULL,
  `fta` int(11) NOT NULL,
  `oreb` int(11) NOT NULL,
  `dreb` int(11) NOT NULL,
  `ast` int(11) NOT NULL,
  `stl` int(11) NOT NULL,
  `blk` int(11) NOT NULL,
  `to` int(11) NOT NULL,
  `pf` int(11) NOT NULL,
  `pts` int(11) NOT NULL,
  PRIMARY KEY (`gameid`,`teamid`,`playerid`,`year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table playbyplay
# ------------------------------------------------------------

CREATE TABLE `playbyplay` (
  `gameid` int(11) NOT NULL,
  `teamid` int(11) NOT NULL,
  `playerid` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `boxscore` varchar(10) NOT NULL,
  `description` varchar(255) NOT NULL,
  `margin` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  KEY `gameid` (`gameid`,`teamid`,`playerid`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table roster
# ------------------------------------------------------------

CREATE TABLE `roster` (
  `year` int(11) NOT NULL,
  `teamid` int(11) NOT NULL,
  `playerid` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `position` varchar(255) NOT NULL,
  `teamid_playerid` varchar(255) NOT NULL,
  PRIMARY KEY (`year`,`teamid`,`playerid`),
  KEY `teamid_playerid` (`teamid_playerid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table schedule
# ------------------------------------------------------------

CREATE TABLE `schedule` (
  `gameid` int(11) NOT NULL,
  `homeid` int(11) NOT NULL,
  `visitid` int(11) NOT NULL,
  `homescore` int(11) NOT NULL,
  `visitscore` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `seasontype` int(11) NOT NULL,
  `gamedate` date NOT NULL,
  `neutral` int(11) NOT NULL,
  PRIMARY KEY (`gameid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table schedule_pbp
# ------------------------------------------------------------

CREATE TABLE `schedule_pbp` (
  `gameid` int(11) NOT NULL,
  `homeid` int(11) NOT NULL,
  `visitid` int(11) NOT NULL,
  `homescore` int(11) NOT NULL,
  `visitscore` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `seasontype` int(11) NOT NULL,
  `gamedate` date NOT NULL,
  `neutral` int(11) NOT NULL,
  PRIMARY KEY (`gameid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table schedule_roster
# ------------------------------------------------------------

CREATE TABLE `schedule_roster` (
  `gameid` int(11) NOT NULL,
  `homeid` int(11) NOT NULL,
  `visitid` int(11) NOT NULL,
  `homescore` int(11) NOT NULL,
  `visitscore` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `seasontype` int(11) NOT NULL,
  `gamedate` date NOT NULL,
  `neutral` int(11) NOT NULL,
  PRIMARY KEY (`gameid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table teams
# ------------------------------------------------------------

CREATE TABLE `teams` (
  `teamid` int(11) NOT NULL,
  `kaggleid` int(11) NOT NULL,
  `teamname` varchar(255) NOT NULL,
  PRIMARY KEY (`teamid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
