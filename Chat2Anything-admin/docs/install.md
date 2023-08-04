### 环境要求 :id=install
- Python >= 3.6
- Mysql >= 5.7.0

###  安装配置

#### 克隆远程仓库

您可以使用 git 来克隆远程仓库：

```shell
# 进入项目主目录
cd Pear Admin Flask

# 使用 git 克隆远程仓库
git clone https://gitee.com/pear-admin/pear-admin-flask.git

# 切换分支
git checkout master  # master, main or mini
```

或者直接前往 Pear Admin Flask 项目的[Gitee 主页](https://gitee.com/pear-admin/pear-admin-flask)下载项目仓库。

#### 搭建开发环境

我们推荐使用 Python 的虚拟环境来开发该项目，这样便于项目的迁移与二次开发。当然，您也可以选择使用原 Python 环境。

如果你想创建 Python 虚拟环境，你可以使用下面的命令行：

```shell
# 在当前目录的venv文件夹创建虚拟环境
python -m venv venv

# Windows 激活虚拟环境
.\test_env\Scripts\Activate.ps1

# Linux 和 Mac 激活虚拟环境
source ./test_env/bin/activate
```

**如果在创建虚拟环境时报错 “ModuleNotFoundError” ，这说明您的 Python 版本小于 3.3 。**

#### 安装项目依赖

```shell
# 使用 pip 安装必要模块（对于 master 分支）
pip install -r requirement\requirement.txt

# 使用 pip 安装必要模块（对于 mini 分支）
pip install -r requirement.txt
```

或者您可以尝试：

```shell
# 使用 pip 安装必要模块
python -m pip install -r requirement.txt
```

#### 配置数据库

在 `applications/config.py` 中配置好数据库。

> 由于结构与目录调整，我们简化了项目结构，废弃了文件 ```.flaskenv``` ，请使用 config.py 配置程序。

并使用以下命令生成数据库文件：

```shell
# 初始化数据库
flask db init
flask db migrate
flask db upgrade
flask admin init
```

#### 运行项目

```shell
# linux
run.bat

# windows
./run.sh
```

#### 使用docker-compose运行项目

```shell
# 安装docker-compose 
curl -L https://github.com/docker/compose/releases/download/1.26.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose 

docker-compose --version
docker-compose up -d # -d后台运行
docker-compose stop # 停止启动
docker-compose down # 清除容器

dockerdata/config.py # 配置文件
dockerdata/mysql/initdb/ # MySQL初始化数据在 
rm -rf dockerdata/mysql/{log,data}/* # down掉容器后启动需要清除删除log,dat
```

### 二次开发

恭喜！现在您已经成功搭建并运行了 Pear Admin Flask ，是时候参与开发了：

请阅读：

+ Pear Admin Flask [目录结构](list.md) 章节
+ Pear Admin Flask [开发函数](function.md) 章节
+ Pear Admin Flask [插件开发](plugin.md) 章节

其它章节等待更新。
