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







