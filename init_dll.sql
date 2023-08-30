CREATE DATABASE `sample_db`;

-- sample_db.departments definition

CREATE TABLE `departments` (
  `id` int NOT NULL,
  `department_name` varchar(256) ,
  PRIMARY KEY (`id`)
);

-- sample_db.hired_employees definition

CREATE TABLE `hired_employees` (
  `id` int NOT NULL,
  `name` varchar(256),
  `hired_at` datetime,
  `department_id` int,
  `job_id` int,
  PRIMARY KEY (`id`)
);

-- sample_db.jobs definition

CREATE TABLE `jobs` (
  `id` int NOT NULL,
  `job` varchar(256),
  PRIMARY KEY (`id`)
);
