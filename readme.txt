#########################################	白名单	python-iptables	

/ecms
/tph
/tyd
/zjj
/test
/fj


https://github.com/pyhunterpig/python-iptables     使用python3.7安装    pip3.7 install --upgrade python-iptables -i https://pypi.tuna.tsinghua.edu.cn/simple

iptables -I FORWARD 3 -p tcp --dport 8080 -j DROP;
iptables -I FORWARD 3 -p tcp -s 180.165.0.0/16 -j ACCEPT;
iptables -I FORWARD 3 -p tcp -s 222.69.0.0/16 -j ACCEPT;
iptables -I FORWARD 3 -p tcp -s  42.236.10.0/16 -j ACCEPT;
iptables -I FORWARD 3 -p tcp -s  116.224.0.0/16 -j ACCEPT;
iptables -I FORWARD 3 -p tcp -s  116.228.0.0/16 -j ACCEPT;
iptables -I FORWARD 3 -p tcp -s  192.168.0.0/16 -j ACCEPT;


预先准备：
	cat /etc/redhat-release # 查看下版本

	python环境：
		CentOS 安装Python3.6多版本共存		https://blog.csdn.net/joson1234567890/article/details/81462175
		1、安装依赖包
		yum install libffi-devel openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc

		2、下载python3.7.0
		cd /usr/local/src
		wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
		tar -xvf Python-3.7.0.tar.xz
		cd Python-3.7.0

		3、配置安装目录
		./configure --prefix=/usr/local/python3.7.0/

		4、编译&安装
		make && make install

		5、创建软链接
		创建python3.7软链接
		ln -s /usr/local/python3.7.0/bin/python3.7 /usr/bin/python3.7
		创建pip软链接
		ln -s /usr/local/python3.7.0/bin/pip3.7 /usr/bin/pip3.7
		pip3.7 install --upgrade pip

	防火墙环境：
		service iptables status
		service firewalld.service status
		firewall-cmd --state
		systemctl start firewalld.service
		systemctl unmask firewalld.service		# 解锁
		systemctl start firewalld.service

#########################################	webserver   django

# 安装django
pip3.7 install django -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3.7 install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple

# sqlite版本过低无法启动需要升级
python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001		
python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001		
		
	升级 SQlite		https://blog.csdn.net/qq_39969226/article/details/92218635	https://blog.csdn.net/weixin_43336281/article/details/100055435
	
	sqlite3 --version	
	
	cd /usr/local/src;
	wget http://www.sqlite.org/2019/sqlite-autoconf-3280000.tar.gz;
	tar zxvf sqlite-autoconf-3280000.tar.gz;
	cd sqlite-autoconf-3280000/;
	./configure --prefix=/usr/local/sqlite;
	make && make install;
	mv /usr/bin/sqlite3 /usr/bin/sqlite3_old;
	cd /usr/local/sqlite/bin/;
	ln -s /usr/local/sqlite/bin/sqlite3 /usr/bin/sqlite3;
	vim /etc/profile
	export LD_LIBRARY_PATH="/usr/local/sqlite/lib"
	source /etc/profile

sqlite3原生操作语句：
	sqlite3 db.sqlite3		# 进入数据库
	.tables					# 查表
	select * from add_ip_ip;
	insert into add_ip_ip(ip) values('192.168.0.0/16');
	insert into add_ip_ip(ip) values('116.228.0.0/16');
	insert into add_ip_ip(ip) values('116.224.0.0/16');
	insert into add_ip_ip(ip) values('42.236.0.0/16');
	insert into add_ip_ip(ip) values('222.69.0.0/16');
	insert into add_ip_ip(ip) values('180.165.0.0/16');
	.quit;

# 防火墙放行8001端口	重启生效
firewall-cmd --zone=public --add-port=8001/tcp --permanent
firewall-cmd --zone=public --add-port=8069/tcp --permanent
firewall-cmd --reload


防火墙规则持久化：https://blog.csdn.net/qq_36512792/article/details/79239390


#########################################	文件监控 pyinotify
https://github.com/seb-m/pyinotify

安装：
	pip3.7 install pyinotify -i https://pypi.tuna.tsinghua.edu.cn/simple

python3.7 -m pyinotify -v /home/xjj/pyinotify
python3.7 /home/xjj/pyinotify/test.py

#########################################	测试


测试成功：  240
	python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001
	python3.7 /home/xjj/pyinotify/test.py

	echo "114.80.177.174 - - [11/Jun/2019:23:04:59 +0800] \"POST /fj/loadWarningInfo.htm HTTP/1.1\" 200 300" >> localhost_access_log.2019-12-20.txt
	echo "123" >> localhost_access_log.2019-06-11.txt
	sed -n '1,10'p test2 >>localhost_access_log.2019-06-11.txt
	cat test2 >> localhost_v6.txt
	ip -L
	iptables -I FORWARD 3 -p tcp --dport 8080 -j DROP;

	iptables --table filter --list FORWARD --line-numbers -n -v
	iptables-save -t filter -c
	iptables-save > /etc/sysconfig/iptables
	iptables-restore < /etc/sysconfig/iptables

# 数据库判断ip,已存在的无需加入防火墙
	django-sqlite
	models.py
	默认使用sqlite3数据库，无需做任何配置,同步一下数据库
	python3.7 manage.py makemigrations
	python37 manage.py migrate

1.多行写入
3.防火墙持久化
2.防火墙去重
4.文件动态变化
	程序启动。获取当前应该监测的文件的指针的位置
		文件存在，定位
			文件变
				是否符合标准文件名格式
					是：置0，写入的文件发请求
					nothing
			内容变


		文件不存在
			等待create事件
#########################################
print(time.localtime(time.time()).)
print(time.strftime("%Y-%m-%d", time.localtime()))
print(type(time.strftime("%Y-%m-%d", time.localtime())))

scp -r /home/xjj/white_ip_log/ root@192.168.1.240:/home/xjj/white_ip_log/

192.168.1.240	192.168.1.230
root
JYcxys@3030



###############################  白名单文档

简介：只允许真正的用户访问proxy，使用防火墙。
	tomcat:访问tomcat的用户，过滤出ip，调用proxy上的django提供的接口，加入到白名单，即可访问	（pyinotify）
	proxy：开启防火墙，不再白名单内的ip，drop掉。 （django	python-iptables	）


230环境(proxy)：
安装python3.7
	cat /etc/redhat-release # 查看下版本
	python环境：
		1、安装依赖包
		yum install libffi-devel openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc

		2、下载python3.7.0
		cd /usr/local/src
		wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
		tar -xvf Python-3.7.0.tar.xz
		cd Python-3.7.0

		3、配置安装目录
		./configure --prefix=/usr/local/python3.7.0/

		4、编译&安装
		make && make install

		5、创建软链接
		创建python3.7软链接
		ln -s /usr/local/python3.7.0/bin/python3.7 /usr/bin/python3.7
		创建pip软链接
		ln -s /usr/local/python3.7.0/bin/pip3.7 /usr/bin/pip3.7
		pip3.7 install --upgrade pip
防火墙环境：
		service iptables status
		service firewalld.service status
		firewall-cmd --state
		systemctl start firewalld.service
		systemctl unmask firewalld.service		# 解锁
		systemctl start firewalld.service
防火墙放行8001端口	重启生效
firewall-cmd --zone=public --add-port=8001/tcp --permanent
firewall-cmd --zone=public --add-port=8069/tcp --permanent
firewall-cmd --zone=public --add-port=8068/tcp --permanent
firewall-cmd --zone=public --add-port=8888/tcp --permanent
firewall-cmd --zone=public --add-service=http --permanent
firewall-cmd --reload
安装python-iptables：
        pip3.7 install --upgrade python-iptables -i https://pypi.tuna.tsinghua.edu.cn/simple
webserver   django:
	pip3.7 install django -i https://pypi.tuna.tsinghua.edu.cn/simple
	pip3.7 install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple
sqlite版本过低无法启动需要升级:
	sqlite3 --version

	cd /usr/local/src
	wget http://www.sqlite.org/2019/sqlite-autoconf-3280000.tar.gz
	tar zxvf sqlite-autoconf-3280000.tar.gz
	cd sqlite-autoconf-3280000/
	./configure --prefix=/usr/local/sqlite
	make && make install
	mv /usr/bin/sqlite3 /usr/bin/sqlite3_old
	cd /usr/local/sqlite/bin/
	ln -s sqlite3 /usr/bin/sqlite3
	vim /etc/profile
	export LD_LIBRARY_PATH="/usr/local/sqlite/lib"
	source /etc/profile

	同步sqlite：
		python3.7 manage.py makemigrations
		python3.7 manage.py migrate

启动：

	python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001
	nohup python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001 >/dev/null 2>&1 &
	jobs -l # 查看pid
	kill -9 pid	# 关闭程序



240环境(tomcat)：
安装python3.7
	cat /etc/redhat-release # 查看下版本

	python环境：
		CentOS7 安装Python3.7多版本共存
		1、安装依赖包
		yum install libffi-devel openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc

		2、下载python3.7.0
		cd /usr/local/src
		wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
		tar -xvf Python-3.7.0.tar.xz
		cd Python-3.7.0

		3、配置安装目录
		./configure --prefix=/usr/local/python3.7.0/

		4、编译&安装
		make && make install

		5、创建软链接
		创建python3.7软链接
		ln -s /usr/local/python3.7.0/bin/python3.7 /usr/bin/python3.7
		创建pip软链接
		ln -s /usr/local/python3.7.0/bin/pip3.7 /usr/bin/pip3.7
		pip3.7 install --upgrade pip
文件监控 pyinotify 安装：
		pip3.7 install pyinotify -i https://pypi.tuna.tsinghua.edu.cn/simple
启动：
		python3.7 /home/xjj/pyinotify/test.py
		nohup python3.7 /home/xjj/pyinotify/pyinotify.py >/dev/null 2>&1 &
		jobs -l # 查看pid
		kill -9 pid	# 关闭程序
###############################

项目做成docker镜像：pyinotify_tomcat
	linux 国内安装docker：（多种安装方式，选择适合自己的）
		curl -sSL https://get.daocloud.io/docker | sh
	启动：
		systemctl start docker
	linux	配置 Docker 镜像站：
		curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s http://f1361db2.m.daocloud.io
	编写Dockerfile文件即可。daocloud会根据这个文件构建docker镜像
		docker pull daocloud.io/xjinjin/pyinotify_tomcat:master-8f30c85
		docker run --name pyinotify_tomcat -v /home/program/apache-tomcat-8.5.32/logs:/code/logs -t -d daocloud.io/xjinjin/pyinotify_tomcat:master-8f30c85

white_ip: 虚拟环境
	mkvirtualenv --no-site-packages --python=/usr/bin/python3.7 env-white_ip

	安装python-iptables：
        pip3.7 install --upgrade python-iptables -i https://pypi.tuna.tsinghua.edu.cn/simple

	webserver   django:
		pip3.7 install django -i https://pypi.tuna.tsinghua.edu.cn/simple
		pip3.7 install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple

	同步sqlite：模型改动需要同步
		python3.7 manage.py makemigrations
		python3.7 manage.py migrate

	启动：
		python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001
		nohup python3.7 /home/xjj/django/white_ip/manage.py runserver 0.0.0.0:8001 >/dev/null 2>&1 &
		nohup python3 /home/xjj/white_ip/manage.py runserver 0.0.0.0:8001 >/dev/null 2>&1 &
		jobs -l # 查看pid
		kill -9 pid	# 关闭程序


###############################