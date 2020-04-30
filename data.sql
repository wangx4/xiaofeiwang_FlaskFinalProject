SET
    SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

SET
    time_zone = "+00:00";

use flask_app;
--
-- Database: `flask_app`
--
--
-- Create model user
--
CREATE TABLE IF NOT EXISTS `user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `fname` varchar(55) NOT NULL,
    `lname` varchar(55) NOT NULL,
    `email` varchar(55) NOT NULL,
    `password` varchar(100) NOT NULL,
    `description` varchar(300) NOT NULL DEFAULT ''
) ENGINE = MyISAM DEFAULT CHARSET = latin1 AUTO_INCREMENT=10;

INSERT INTO `user` (`id`, `fname`, `lname`, `email`, `password`, `description`) VALUES
(1, 'Testguy', 'Test', 'abcde@a.com', '', 'its me'),
(2, 'Testguy', 'newname', 'a@a.com', '', 'NO its not'),
(3, 'Tom', 'Test', 'b@a.com', '123', 'yes it is'),
(4, 'Testguy', 'Test', 'a@a.com', '12345', 'short'),
(5, 'Test', 'Testtest', 'admin@root.com', '123', '');
--
-- Create model file
--
--`content_length` integer NOT NULL,
--`update_time` datetime(6) NOT NULL,
--`storage_path` varchar(200) NOT NULL,
CREATE TABLE IF NOT EXISTS `file` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `storage_name` varchar(300) NOT NULL
) ENGINE = MyISAM DEFAULT CHARSET = latin1;

--
-- Create model shared_file
--
CREATE TABLE IF NOT EXISTS `shared_file` (
    `user_id` integer NOT NULL,
    `user_file_id` integer NOT NULL,
    `id` varchar(36) NOT NULL PRIMARY KEY,
    `access_token` varchar(4) NOT NULL
) ENGINE = MyISAM DEFAULT CHARSET = latin1;

--
-- Create model user_file
--
CREATE TABLE IF NOT EXISTS `user_file` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `file_id` integer NOT NULL,
    `filename` varchar(200) NOT NULL,
    `is_shared` bool NOT NULL DEFAULT false,
    `is_deleted` bool NOT NULL DEFAULT false
) ENGINE = MyISAM DEFAULT CHARSET = latin1;