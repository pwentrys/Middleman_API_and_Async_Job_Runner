  CREATE TABLE `queue` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `datetime_create` DATETIME NOT NULL DEFAULT current_timestamp(),
  `datetime_update` DATETIME NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `job_id` INT(10) UNSIGNED NOT NULL,
  `status_id` INT(1) UNSIGNED NOT NULL,
  `datetime_begin` DATETIME DEFAULT NULL,
  `datetime_finish` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `jobstatusdur_UNIQUE` (`job_id`,`status_id`),
  UNIQUE KEY `statusjobdur_UNIQUE` (`status_id`,`job_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8