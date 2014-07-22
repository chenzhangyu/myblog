-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2014 年 07 月 22 日 11:48
-- 服务器版本: 5.5.38
-- PHP 版本: 5.5.15RC1
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
drop database myblog;
create datebase myblog;
use myblog;
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `myblog`
--

-- --------------------------------------------------------

--
-- 表的结构 `comments`
--
-- 创建时间: 2014 年 07 月 22 日 02:07
--

CREATE TABLE IF NOT EXISTS `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `passage_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `pubdate` varchar(30) DEFAULT NULL,
  `display` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `passage_id` (`passage_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

-- --------------------------------------------------------

--
-- 表的结构 `passages`
--
-- 创建时间: 2014 年 07 月 22 日 02:07
--

CREATE TABLE IF NOT EXISTS `passages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `content` text,
  `pubdate` varchar(80) DEFAULT NULL,
  `display` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- 表的结构 `pata`
--
-- 创建时间: 2014 年 07 月 22 日 02:07
--

CREATE TABLE IF NOT EXISTS `pata` (
  `passage_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  KEY `passage_id` (`passage_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `tags`
--
-- 创建时间: 2014 年 07 月 22 日 02:07
--

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- 转存表中的数据 `tags`
--

INSERT INTO `tags` (`id`, `tag`) VALUES
(2, 'coding'),
(1, 'Python'),
(3, 'web'),
(4, '二次元'),
(5, '杂谈');

-- --------------------------------------------------------

--
-- 表的结构 `talks`
--
-- 创建时间: 2014 年 07 月 22 日 02:07
--

CREATE TABLE IF NOT EXISTS `talks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_id` int(11) DEFAULT NULL,
  `originer_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` varchar(200) DEFAULT NULL,
  `pubdate` varchar(30) DEFAULT NULL,
  `display` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- 表的结构 `user`
--
-- 创建时间: 2014 年 07 月 22 日 02:07
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `root` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `root`) VALUES
(1, 'lance', '202cb962ac59075b964b07152d234b70', '1');

--
-- 限制导出的表
--

--
-- 限制表 `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`passage_id`) REFERENCES `passages` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

--
-- 限制表 `pata`
--
ALTER TABLE `pata`
  ADD CONSTRAINT `pata_ibfk_1` FOREIGN KEY (`passage_id`) REFERENCES `passages` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pata_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

--
-- 限制表 `talks`
--
ALTER TABLE `talks`
  ADD CONSTRAINT `talks_ibfk_1` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `talks_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
