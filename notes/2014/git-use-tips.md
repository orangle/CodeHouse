some basic use tips:

####add file
git add filename1 filename2
git add *

####commit file
git commit -m "some comment of this comment"
**this time the file will commit to your local head **

####push your file to remote warehouse
git push origin master

* master is your local branch name
* origin is remote warehouse

####push your local warehouse to remote server
git remote add origin <server\>

####merge remote modified to local warehouse
* auto merge:   git pull
* after handled conflicts:  git add filename2

####github 协作

1.A账号登录github上，参与B账号的项目，在B账号网页上点fork
2.把项目clone到本地
　　git clone https://github.com/A/xxx.git
3.添加上游远端GIT
　　git remote add upstream https://github.com/B/xxx.git
　　upstream可以随便取别名
4.取远端最新代码，保证自己的代码是最新，免得跟别人的有冲突
　　git fetch upstream

5.合并到本地
　　git merge upstream/master

6.更新远端自己的代码库（push Update remote refs along with associated objects）
　　git push
7.登录自己的账号A，在上面点pull request
　　https://github.com/A/xxx

####问题解决
remote error: access denied or repository not exported:

$ git remote rm origin
$ git remote add origin 'git@gitcafe.com:fnngj/pyse.git'


gitssh  安装
https://gitcafe.com/GitCafe/Help/wiki/%E5%A6%82%E4%BD%95%E5%AE%89%E8%A3%85%E5%92%8C%E8%AE%BE%E7%BD%AE-Git#wiki

####区别github 和别的托管服务 设置
$ git config --global github.user defnngj      //github 上的用户名
$ git config --global github.token e97279836f0d415a3954c1193dba522f   #




