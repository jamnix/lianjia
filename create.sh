



mysql="mysql -hlocalhost -uroot -p123 lianjia"

sql="create table lianjia_270_310 (
href varchar(255) NOT NULL DEFAULT '',
title varchar(255) NOT NULL DEFAULT '',
title_sub varchar(255) NOT NULL DEFAULT '',
price int(11) NOT NULL DEFAULT 0,
unit_price int(11) NOT NULL DEFAULT 0,
room_huxing varchar(255) NOT NULL DEFAULT '',
room_loucheng varchar(255) NOT NULL DEFAULT '',
room_fangxiang varchar(255) NOT NULL DEFAULT '',
room_zhuanxiu varchar(255) NOT NULL DEFAULT '',
room_size varchar(255) NOT NULL DEFAULT '',
room_has_year varchar(255) NOT NULL DEFAULT '',
xiaoqu_name varchar(255) NOT NULL DEFAULT '',
xiaoqu_href varchar(255) NOT NULL DEFAULT '',
area_qu varchar(255) NOT NULL DEFAULT '',
area_qu_sub varchar(255) NOT NULL DEFAULT '',
room_tihu varchar(255) NOT NULL DEFAULT '',
room_dianti varchar(255) NOT NULL DEFAULT '',
room_chanquan varchar(255) NOT NULL DEFAULT '',
room_now_buy varchar(255) NOT NULL DEFAULT '',
room_last_buy varchar(255) NOT NULL DEFAULT '',
room_shanping varchar(255) NOT NULL DEFAULT '',
room_red_book varchar(255) NOT NULL DEFAULT '',
primary key(href)
)charset=utf8
"

echo $sql | $mysql
