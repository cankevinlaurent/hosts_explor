############################################################
- @Code:    205 Project / B
- @Purpose: 根据网段探测活跃host，不包括网关和广播地址。
- @Author:  Kévin
- @Update:  17 Oct. 2018
############################################################

##################
I. 项目文件
##################
- /hosts_explor            项目文件夹。
- hosts_explor.db          数据库，记录IP信息。
- CommonConfigProcessor.py 公共类，读取配置文件。
- CommonDBProcessor.py     公共类，数据库操作。
- hosts_enabler.py         使能程序，提供API接口查询信息。
- hosts_explor.py          探测活跃IP。
- config_hosts_explor.txt  配置文件，包括端口、认证等。
- start_hosts_explor.sh    启动脚本。
- readme_hosts_explor.txt  本说明文档。

##################
II. 项目部署条件
##################
- 推荐CentOS 6.9或更高
- 推荐python 2.7.14或更高
- #visudo，增加一句：wangwei ALL=(jtitsm)   ALL
- 不需要root账号
- 正确设置文件和文件夹权限，如db文件及其全路径文件夹必须可写
- requests库：wangwei$pip install --user requests
- flask库：wangwei$pip install --user flask
- flask-httpauth库：wangwei$pip install --user flask-httpauth
- pyOpenSSL库：wangwei$pip install --user pyOpenSSL
- ipaddr库：wangwei$pip install --user ipaddr

##################
III. 项目运行
##################
- 应用账号：jtitsm，部署账号：wangwei
- 修改配置文件：设置正确location
- 修改配置文件：设置正确subnet_url
- 启动脚本赋可执行权限：wangwei$chmod +x start_hosts_explor.sh
- wangwei$sudo -u jtitsm ./start_hosts_explor.sh

##################
IV. 数据库元信息
##################
- 数据库：SQLite3
- 数据库编码：utf-8
CREATE TABLE "hosts" (
"ip"  TEXT NOT NULL,
"stat"  TEXT DEFAULT NULL,
"timestamp"  INTEGER DEFAULT NULL,
PRIMARY KEY ("ip")
);

