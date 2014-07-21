-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2014 年 07 月 21 日 10:08
-- 服务器版本: 5.5.38
-- PHP 版本: 5.5.15RC1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


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
-- 创建时间: 2014 年 07 月 20 日 08:42
--

CREATE TABLE IF NOT EXISTS `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `passage_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` varchar(500) DEFAULT NULL,
  `pubdate` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `passage_id` (`passage_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `comments`
--

INSERT INTO `comments` (`id`, `passage_id`, `user_id`, `content`, `pubdate`) VALUES
(1, 4, 2, '是啊。大师兄', '2014-07-21 10:02:31'),
(2, 2, 2, '吃啊', '2014-07-21 10:04:32');

-- --------------------------------------------------------

--
-- 表的结构 `passages`
--
-- 创建时间: 2014 年 07 月 20 日 08:42
--

CREATE TABLE IF NOT EXISTS `passages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `content` text,
  `pubdate` varchar(80) DEFAULT NULL,
  `display` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- 转存表中的数据 `passages`
--

INSERT INTO `passages` (`id`, `title`, `content`, `pubdate`, `display`) VALUES
(1, '这是标题', 'test forsomething', '2014-07-20 17:11:39', 1),
(2, 'Python能吃吗', '大家来商量一下呗', '2014-07-20 17:37:40', 1),
(3, 'Python教程', '这是小白的Python新手教程。\r\n\r\nPython是一种计算机程序设计语言。你可能已经听说过很多种流行的编程语言，比如非常难学的C语言，非常流行的Java语言，适合初学者的Basic语言，适合网页编程的JavaScript语言，等等。\r\n\r\n那Python是一种什么语言？\r\n\r\n首选，我们普及一下编程语言的基础知识。用任何编程语言来开发程序，都是为了让计算机干活，比如下载一个MP3，编写一个文档等等，而计算机干活的CPU只认识机器指令，所以，尽管不同的编程语言差异极大，最后都得“翻译”成CPU可以执行的机器指令。而不同的编程语言，干同一个活，编写的代码量，差距也很大。\r\n\r\n比如，完成同一个任务，C语言要写1000行代码，Java只需要写100行，而Python可能只要20行。\r\n\r\n所以Python是一种相当高级的语言。\r\n\r\n你也许会问，代码少还不好？代码少的代价是运行速度慢，C程序运行1秒钟，Java程序可能需要2秒，而Python程序可能就需要10秒。\r\n\r\n那是不是越低级的程序越难学，越高级的程序越简单？表面上来说，是的，但是，在非常高的抽象计算中，高级的Python程序设计也是非常难学的，所以，高级程序语言不等于简单。\r\n\r\n但是，对于初学者和完成普通任务，Python语言是非常简单易用的。连Google都在大规模使用Python，你就不用担心学了会没用。\r\n\r\n用Python可以做什么？可以做日常任务，比如自动备份你的MP3；可以做网站，很多著名的网站包括YouTube就是Python写的；可以做网络游戏的后台，很多在线游戏的后台都是Python开发的。总之就是能干很多很多事啦。\r\n\r\nPython当然也有不能干的事情，比如写操作系统，这个只能用C语言写；写手机应用，只能用Objective-C（针对iPhone）和Java（针对Android）；写3D游戏，最好用C或C++。\r\n\r\n如果你是小白用户，满足以下条件：\r\n\r\n会使用电脑，但从来没写过程序；\r\n还记得初中数学学的方程式和一点点代数知识；\r\n想从编程小白变成专业的软件架构师；\r\n每天能抽出半个小时学习。\r\n不要再犹豫了，这个教程就是为你准备的！\r\n\r\n准备好了吗？', '2014-07-20 17:38:06', 0),
(4, '确认(confirm)', '确认框用于让用户选择某一个问题是否符合实际情况。\r\n\r\n“说！是还是不是？快回答！”\r\n\r\n如果你想表达这样的意思，那么confirm再合适不过了。来看下面的代码：我们用confirm("你是菜鸟吗？")向访客提问，变量r则保存了访客的回应，它只可能有两种取值：true或false。没错，它是一个布尔值。confirm后面的语句则是我们对访客回答做出的不同回应。\r\n\r\n<script type="text/JavaScript">\r\n     var r=confirm("你是菜鸟吗");\r\n     if (r==true)\r\n     {\r\n     document.write("彼此彼此");\r\n     }\r\n     else\r\n     {\r\n     document.write("佩服佩服");\r\n     }\r\n</script>\r\n看一个使用confirm的实例', '2014-07-20 17:38:46', 1),
(5, '提问(prompt)', 'prompt和confirm类似，不过它允许访客随意输入回答。我们来修改一下之前switch的例子，我们根据分数来做出不同的评价，不过那段程序并不完整，它根本就没问我们分数，而是假设我得了65分。这太不公平了。现在我么就可以用prompt来向访客提问，用score存储用户输入的回答，其余的事情就都由后面的switch来完成了。\r\n\r\n<script type="text/JavaScript">\r\n function judge() {\r\n var score;//分数\r\n var degree;//分数等级\r\n score = prompt("你的分数是多少？")\r\n if (score > 100){\r\n degree = ''耍我？100分满！'';\r\n }\r\n else{\r\n switch (parseInt(score / 10)) {\r\n case 0:\r\n case 1:\r\n case 2:\r\n case 3:\r\n case 4:\r\n case 5:\r\n degree = "恭喜你，又挂了！";\r\n break;\r\n case 6:\r\n degree = "勉强及格";\r\n break;\r\n case 7:\r\n degree = "凑合，凑合"\r\n break;\r\n case 8:\r\n degree = "8错，8错";\r\n break;\r\n case 9:\r\n case 10:\r\n degree = "高手高手，佩服佩服";\r\n }//end of switch\r\n }//end of else\r\n alert(degree);\r\n }\r\n </script>', '2014-07-20 17:39:26', 0);

-- --------------------------------------------------------

--
-- 表的结构 `pata`
--
-- 创建时间: 2014 年 07 月 20 日 08:42
--

CREATE TABLE IF NOT EXISTS `pata` (
  `passage_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  KEY `passage_id` (`passage_id`),
  KEY `tag_id` (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `pata`
--

INSERT INTO `pata` (`passage_id`, `tag_id`) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 1),
(3, 3),
(3, 1),
(3, 2),
(4, 3),
(4, 1),
(4, 2),
(5, 1),
(5, 2);

-- --------------------------------------------------------

--
-- 表的结构 `tags`
--
-- 创建时间: 2014 年 07 月 20 日 08:42
--

CREATE TABLE IF NOT EXISTS `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- 转存表中的数据 `tags`
--

INSERT INTO `tags` (`id`, `tag`) VALUES
(3, '23333'),
(1, 'Python'),
(2, 'web');

-- --------------------------------------------------------

--
-- 表的结构 `talks`
--
-- 创建时间: 2014 年 07 月 20 日 08:42
--

CREATE TABLE IF NOT EXISTS `talks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_id` int(11) DEFAULT NULL,
  `originer_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `content` varchar(200) DEFAULT NULL,
  `pubdate` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comment_id` (`comment_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- 转存表中的数据 `talks`
--

INSERT INTO `talks` (`id`, `comment_id`, `originer_id`, `user_id`, `content`, `pubdate`) VALUES
(1, 2, 0, 2, '打错了。。', '2014-07-21 10:04:46');

-- --------------------------------------------------------

--
-- 表的结构 `user`
--
-- 创建时间: 2014 年 07 月 20 日 08:42
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) DEFAULT NULL,
  `password` varchar(120) DEFAULT NULL,
  `root` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `root`) VALUES
(1, 'lance', '202cb962ac59075b964b07152d234b70', '1'),
(2, '123', '202cb962ac59075b964b07152d234b70', '0');

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
