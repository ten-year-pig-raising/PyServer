在初次搭建平台时, 数据库没有数据时，执行如下操作:

1. 建立一个新的数据库，名称为: data_analysis_spider

2. 在命令行依次执行如下三个命令: 
	
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py init

3. 再执行sql 命令， 执行本目录下的update.sql