
#1、使用 python 3.5
在初始化环境时使用 requirement.txt 文件
pip install -r requirements.txt


#2、导入自定义模块时需要注意的地方：
定义可导出的模块或函数
__all__=['a','b']



#3、初始化数据库时：
#执行后会增加 migrations目录【当目录存在时可以不执行】
python magrate.py db init

#根据差异创建迁移
python magrate.py db migrate -m "说明"

#改动差异
python magrate.py db upgrade

#取消差异改动
python magrate.py db downgrade


#4、使用虚拟环境 virtualenv
#创建环境
virtualenv -p /usr/bin/python2.7 venv

virtualenv --no-site-packages venv3.6

#启用虚拟环境
source venv3.6/bin/activate

#退出当前虚拟环境
deactivate



#5、然后下面讲到创建命令，可以有3种方式
•创建Command的子类
•使用 @command 修饰符
•使用 @option 修饰符


#6、操作数据库时 1267 Illegal mix of collations (gbk_chinese_ci,IMPLICIT) and (utf8_general_ci,COERCIBLE) fo
是MySQL数据库的字符集不一致导致，无法比较，修改统一MySQL的字符集即可解决


#7.git使使用与GitHub远程库配置
##创建版本库
```
mkdir learngit
cd learngit
git init
```

##GitHub远程库配置
```
1、注册GitHub账号
由于你的本地Git仓库和GitHub仓库之间的传输是通过SSH加密的，所以进行配置

第1步：创建SSH Key。在用户主目录下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果已经有了，可直接跳到下一步。如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：

$ ssh-keygen -t rsa;

在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。


第2步：登陆GitHub，打开“Account settings”，“SSH Keys”页面：
然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容：


第三步：在本地执行，需要在git库下执行
git remote add origin git@github.com:用户名/仓储名.git


因为没有文件导致报错
error: src refspec master does not match any.
error: failed to push some refs to 'git@github.com:sumlxt123/sware.git'


```

#清空含外键的表
```
#先
set foreign_key_checks = 0;

#清空表
truncate table tablename;

#在
set foreign_key_checks = 1;

```