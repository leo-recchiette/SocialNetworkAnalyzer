-- Schema for the SNA tool MySQL database.
-- Auto-loaded by the official mysql image on first container start
-- (files in /docker-entrypoint-initdb.d run once, against $MYSQL_DATABASE).
--
-- Mirrors the tables documented in README.md. Column names with spaces are
-- intentional: the Python code (wordsFrequency.py, menageDumps.py) references
-- them with those exact backticked names.

CREATE DATABASE IF NOT EXISTS sna_tool;
USE sna_tool;

-- utf8mb4 on both tables: MySQL 5.7 defaults to latin1, which would reject or
-- silently corrupt the accented/multi-byte tokens the NLP pipeline produces
-- (Italian stopwords/text) and any non-ASCII profile identifiers. utf8mb4 also
-- covers 4-byte emoji. The client connection charset is set to match in
-- server/dbConnector.py (sqlHelper, charset='utf8mb4').

CREATE TABLE IF NOT EXISTS `users` (
  `mail` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `word_frequency` (
  `word` varchar(500) NOT NULL,
  `value` varchar(10) NOT NULL,
  `user Profile Property` varchar(45) NOT NULL,
  `User Registered on SNA` varchar(45) NOT NULL,
  `Social Network` varchar(45) NOT NULL
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
