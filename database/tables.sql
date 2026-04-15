--
-- Database: `sbom_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `hr`
--

CREATE TABLE `hr` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `company` varchar(100) default NULL,
  `location` varchar(100) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `hr`
--

INSERT INTO `hr` (`id`, `name`, `email`, `mobile`, `company`, `location`, `username`, `password`) VALUES
(1, 'Mahendira', 'rajmahendira7@gmail.com', '9345911674', 'MAHENDIRA TECH', 'Cuddalore', 'raj', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(50) default NULL,
  `filename` varchar(200) default NULL,
  `result` text,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=31 ;

--
-- Dumping data for table `logs`
--

INSERT INTO `logs` (`id`, `username`, `filename`, `result`, `created_at`) VALUES
(1, 'raj', 'train_model.py', 'Low', '2026-03-18 10:19:32'),
(2, 'raj', 'app.py', 'Low', '2026-03-18 10:28:50'),
(3, 'raj', 'Requirements.txt', 'Low', '2026-03-18 10:29:33'),
(4, 'raj', 'app.py', 'Low', '2026-03-18 12:06:57'),
(5, 'raj', 'requirements.txt', 'Low', '2026-03-18 12:09:36'),
(6, 'raj', 'medium.txt', 'Low', '2026-03-18 12:11:14'),
(7, 'raj', 'requirements.txt', 'Low', '2026-03-18 12:11:26'),
(8, 'raj', 'requirements.txt', 'Critical', '2026-03-18 12:12:07'),
(9, 'raj', 'requirements.txt', 'Critical', '2026-03-18 12:15:44'),
(10, 'raj', 'medium.txt', 'High', '2026-03-18 12:15:56'),
(11, 'raj', 'high.txt', 'High', '2026-03-18 12:16:06'),
(12, 'raj', 'app.py', 'Low', '2026-03-18 12:16:28'),
(13, 'raj', 'medium.txt', 'High', '2026-03-18 12:46:12'),
(14, 'raj', 'requirements.txt', 'Critical', '2026-03-18 13:57:34'),
(15, 'raj', 'medium.txt', 'High', '2026-03-18 14:05:46'),
(16, 'raj', 'medium.txt', 'High', '2026-03-18 14:06:16'),
(17, 'raj', 'low.txt', 'Critical', '2026-03-18 15:04:53'),
(18, 'raj', 'low.txt', 'Critical', '2026-03-18 16:17:55'),
(19, 'raj', 'low.txt', 'Critical', '2026-03-18 16:23:20'),
(20, 'raj', 'low.txt', 'Critical', '2026-03-18 16:26:03'),
(21, 'raj', 'low.txt', 'Critical', '2026-03-18 16:26:45'),
(22, 'raj', 'low.txt', 'Critical', '2026-03-18 16:30:07'),
(23, 'raj', 'low.txt', 'Critical', '2026-03-18 16:32:55'),
(24, 'raj', 'low.txt', 'Critical', '2026-03-18 16:35:37'),
(25, 'raj', 'requirements.txt', 'Critical', '2026-03-18 16:37:18'),
(26, 'raj', 'requirements.txt', 'Critical', '2026-03-18 16:40:36'),
(27, 'raj', 'requirements.txt', 'High', '2026-03-18 16:42:30'),
(28, 'raj', 'requirements.txt', 'Low', '2026-03-18 16:46:40'),
(29, NULL, 'sample (4).txt', 'Medium', '2026-03-18 21:12:16'),
(30, NULL, 'sample (3).txt', 'Critical', '2026-03-18 22:30:18');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `id` int(11) NOT NULL auto_increment,
  `pm_id` int(11) default NULL,
  `tl_id` int(11) default NULL,
  `tester_id` int(11) default NULL,
  `title` varchar(200) default NULL,
  `module` text,
  `workflow` text,
  `requirements` text,
  `status` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`id`, `pm_id`, `tl_id`, `tester_id`, `title`, `module`, `workflow`, `requirements`, `status`) VALUES
(1, 1, 1, 1, 'Employee MS', 'qejlrfrgejvaw', 'deugfuigsuyga', 'duigweydfgsduycfva', 'Completed'),
(2, 1, 1, 1, 'Face Recognition', 'Face Enroll and Face Verification', 'Enroll Face, WebCam Open and Verify Face', 'Python, Mysql, Flask, HTML, CSS', 'Completed');

-- --------------------------------------------------------

--
-- Table structure for table `project_manager`
--

CREATE TABLE `project_manager` (
  `id` int(11) NOT NULL auto_increment,
  `hr_id` int(11) default NULL,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `project_manager`
--

INSERT INTO `project_manager` (`id`, `hr_id`, `name`, `email`, `mobile`, `username`, `password`) VALUES
(1, 1, 'Raj', 'raj@gmail.com', '9876522345', 'raj', '1234'),
(2, 1, 'Vijay', 'vijay@gmail.com', '8148956601', 'vijay', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

CREATE TABLE `results` (
  `id` int(11) NOT NULL auto_increment,
  `tester_id` int(11) default NULL,
  `filename` varchar(200) default NULL,
  `risk` varchar(50) default NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `project_id` int(11) default NULL,
  `recommendation` text,
  PRIMARY KEY  (`id`),
  KEY `project_id` (`project_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `results`
--

INSERT INTO `results` (`id`, `tester_id`, `filename`, `risk`, `created_at`, `project_id`, `recommendation`) VALUES
(1, 1, 'sample (4).txt', 'Medium', '2026-03-18 21:12:16', 1, NULL),
(2, 1, 'sample (3).txt', 'Critical', '2026-03-18 22:30:18', 2, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `team_leader`
--

CREATE TABLE `team_leader` (
  `id` int(11) NOT NULL auto_increment,
  `pm_id` int(11) default NULL,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `team_leader`
--

INSERT INTO `team_leader` (`id`, `pm_id`, `name`, `email`, `mobile`, `username`, `password`) VALUES
(1, 1, 'Mahendira', 'raj@gmail.com', '1234567890', 'raj', '1234'),
(2, 1, 'Ragul', 'raguk@gmail.com', '0987654321', 'ragul', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `tester`
--

CREATE TABLE `tester` (
  `id` int(11) NOT NULL auto_increment,
  `tl_id` int(11) default NULL,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(20) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `tester`
--

INSERT INTO `tester` (`id`, `tl_id`, `name`, `email`, `mobile`, `username`, `password`) VALUES
(1, 1, 'Raj', 'raj@gmail.com', '8929090909', 'raj', '1234'),
(2, 1, 'Ragul', 'ragul@gmail.com', '8929090909', 'ragul', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `testers`
--

CREATE TABLE `testers` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) default NULL,
  `email` varchar(100) default NULL,
  `mobile` varchar(15) default NULL,
  `username` varchar(50) default NULL,
  `password` varchar(255) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `testers`
--

INSERT INTO `testers` (`id`, `name`, `email`, `mobile`, `username`, `password`) VALUES
(1, 'Raj', 'raj@gmail.com', '7904978831', 'raj', '1234');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `results`
--
ALTER TABLE `results`
  ADD CONSTRAINT `results_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`);
