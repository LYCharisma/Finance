# 金融风险高性能计算平台

[GitHub Pages](http://liquidfly.github.io/Finance/)

此项目地址：git@github.com:LiQuidFly/Finance.git

## Log

* 6/30

  * 关于环境配置（新）
  
    * Windows
    
      1.安装[Python](https://www.python.org/downloads/release/python-343/)（注意为3.x版本，可下载64位版本）。
      
      2.将Python的安装目录，Python安装目录下的Script目录加入环境变量。
      （如Python安装到D:\Python,则将D:\Python;D:\Python\Scripts;加入PATH最前面）
      
      3.下载[Git](http://www.git-scm.com/)并安装。
      
      4.启动Git Bash，按照[此步骤](https://help.github.com/articles/generating-ssh-keys/）添加密钥（注意选择平台）。
      
      4.启动PyCharm，在File->Settings->Version Control->Git中设置Git的可执行文件位置（Git安装目录中的bin目录）.
      
      5.在PyCharm中，选择VCS->Checkout from Version Control->GitHub。
      
      6.输入GitHub账户密码。


* 6/29

  * 关于环境配置
  
    * Windows
    
      1.下载[GitHub for Windows](https://windows.github.com/)并安装(慢)。
      
      2.使用GitHub帐号登录，并克隆此项目。
      
      3.使用PyCharm打开此文件夹。
      
    * Linux
      
      1.安装Git与SSH。（Ubuntu上为# sudo apt-get install git openssh-client）

      2.按照[此步骤](https://help.github.com/articles/generating-ssh-keys/#platform-linux)，添加密钥。
      （第1,3,5步可省略，第4步可直接复制粘贴id_rsa.pub中的内容。）
      
      3.克隆此项目，并使用PyCharm打开此文件夹。
    
