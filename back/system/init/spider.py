spider = """INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (1, '2022-10-29 17:38:43.000000', '2022-10-31 13:32:48.984354', NULL, 0, '文旅部-公告', '*', 'https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081.html', '.*?index_3081.*?', '.*/scgl/.*.html', '//div[@class=\"fanye_list\"]', '//ul[@class=\"mesgopen2\"]//a', '//h2[@class=\"xxgk_title\"]//text()', '//dt[contains(text(), \'发布日期：\')]/../dd/text()', '//div[@class=\"gsj_htmlcon\"]', '//div[@class=\"gsj_htmlcon_bot\"]', '//dt[contains(text(), \'发布机构\')]/../dd/text()', 1, 'https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081{}.html', 'var countPage = (\\d+)', 0, '\'_\'+str(num) if num > 0 else \'\'', NULL, NULL);
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (3, '2022-10-31 09:16:26.000000', '2022-10-31 13:32:53.516832', NULL, 0, '河北文旅厅-媒体关注', '*', 'http://www.hebeitour.gov.cn/xwzx/mtgz/index.html', '.*/index_.*', '.*/c/.*', '//span[contains(text(), \"下一页\")]/parent::a', '//div[@class=\"list\"]/ul/li/a', '//div[@class=\"content\"]/h1/text()', '//div[@class=\"post_source\"]/text()', '//div[@id=\"content\"]', '//div[@id=\"content\"]', '//div[@class=\"post_source\"]/text()', 1, NULL, NULL, NULL, NULL, '.*?来源：(.*)', '(.*?)来源.*?');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (4, '2022-10-31 09:16:26.000000', '2022-10-31 13:32:51.368632', NULL, 0, '河北文旅厅-展演信息', '*', 'https://www.hebeitour.gov.cn/xwzx/zyxx/index.html', '.*', '.*/c/.*', '//span[contains(text(), \"下一页\")]/parent::a', '//div[@class=\"list\"]/ul/li/a', '//div[@class=\"content\"]/h1/text()', '//div[@class=\"post_source\"]/text()', '//div[@id=\"content\"]', '//div[@id=\"content\"]', '//div[@class=\"post_source\"]/text()', 1, NULL, NULL, NULL, NULL, '.*?来源：(.*)', '(.*?)来源.*?');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (5, '2022-10-29 17:38:43.000000', '2022-10-31 13:24:37.648373', NULL, 0, '文旅部-通知', '*', 'https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081.html', '', '.*/scgl/.*.html', '', '//ul[@class=\"mesgopen2\"]//a', '//h2[@class=\"xxgk_title\"]//text()', '//dt[contains(text(), \'发布日期：\')]/../dd/text()', '//div[@class=\"gsj_htmlcon\"]', '//div[@class=\"gsj_htmlcon_bot\"]', '//dt[contains(text(), \'发布机构\')]/../dd/text()', 1, 'https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081{}.html', 'var countPage = (\\d+)', 0, '\'_\'+str(num) if num > 0 else \'\'', NULL, NULL);
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (6, '2022-10-31 09:47:41.000000', '2022-12-08 16:09:07.716547', NULL, 0, '文旅部-焦点新闻', '*', 'https://www.mct.gov.cn/whzx/whyw/', 'var countPage = (\\d+);', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/whzx/whyw/index{}.htm', NULL, NULL, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (7, '2022-10-31 09:47:41.000000', '2022-11-03 08:54:03.151573', NULL, 0, '文旅部-中央精神', '*', 'https://www.mct.gov.cn/preview/special/xy20d/9671/', '', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/preview/special/xy20d/9671/index{}.htm', 'var countPage = (\\d+);', 0, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (9, '2022-10-31 09:47:41.000000', '2022-10-31 13:33:04.089922', NULL, 0, '文旅部-文化和旅游部系统', '*', 'https://www.mct.gov.cn/preview/special/xy20d/9674/index.htm', '', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/preview/special/xy20d/9674/index{}.htm', 'var countPage = (\\d+);', 0, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (10, '2022-10-31 09:47:41.000000', '2022-10-31 13:33:02.088080', NULL, 0, '文旅部-代表风采', '*', 'https://www.mct.gov.cn/preview/special/xy20d/9677/', '', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/preview/special/xy20d/9677/index{}.htm', 'var countPage = (\\d+);', 0, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (11, '2022-10-31 09:47:41.000000', '2022-10-31 13:32:59.689590', NULL, 0, '文旅部-媒体报道', '*', 'https://www.mct.gov.cn/preview/special/xy20d/9676/', '', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/preview/special/xy20d/9676/index{}.htm', 'var countPage = (\\d+);', 0, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (12, '2022-10-31 09:47:41.000000', '2022-10-31 13:32:57.591243', NULL, 0, '文旅部-数说文旅', '*', 'https://www.mct.gov.cn/preview/special/xy20d/9678/', '', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/preview/special/xy20d/9678/index{}.htm', 'var countPage = (\\d+);', 0, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');
INSERT INTO `spider` (`id`, `createAt`, `updateAt`, `dept_belong_id`, `is_delete`, `name`, `allowed_domains`, `start_urls`, `re_page`, `re_item`, `xpath_page_restrict`, `xpath_item_restrict`, `xpath_name`, `xpath_time`, `xpath_cover`, `xpath_content`, `xpath_source`, `enable`, `page_format`, `re_page_num`, `start_page_num`, `page_format_shift`, `re_source`, `re_time`) VALUES (13, '2022-10-31 09:47:41.000000', '2022-10-31 13:32:55.563151', NULL, 0, '文旅部-数说文旅', '*', 'https://www.mct.gov.cn/preview/special/xy20d/9672/', '', './*/t.*', '', '//table[@class=\"lm_tabe\"]/tr/td/a', '//div[@class=\"sp_title\"]//text()', '//div[@class=\"sp_time\"]/font[1]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"TRS_Editor\"]', '//div[@class=\"sp_time\"]/font[2]', 1, 'https://www.mct.gov.cn/preview/special/xy20d/9672/index{}.htm', 'var countPage = (\\d+);', 0, '\'_\'+str(num) if num > 0 else \'\'', '.*?来源：(.*?)<.*', '.*发布时间：(.*?)<.*');

"""