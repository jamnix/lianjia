


mysql="mysql -hlocalhost -uroot -p123 lianjia"
echo 'select * from lianjia_270_310 where room_dianti="有" and room_fangxiang like "%南%" and (title like "%安静%" or title_sub like "%安静%") order by area_qu, room_now_buy desc ' | $mysql
