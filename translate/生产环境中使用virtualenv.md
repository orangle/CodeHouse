生产环境中使用virtualenv
====================

> virtualenv 对于python开发和部署都是好工具，可以隔离多个python版本和第三方库的版本，这里作者总结了几个常用python服务怎么样结合virtual部署 [原文链接](http://dangoldin.com/2014/02/10/using-virtualenv-in-production/)

Python 中我最喜欢的东西之一就是可以使用 virtualenv 去创建隔离的环境。非常简单的就可以在不同的项目中部署不同的python类库。

有一个比较棘手的问题就是在生产环境中使用virtualenv 部署几个不同的服务有一些配置上的不同。 于是我就从我的项目中收集了几种不同的服务的不同配置方式。 可以肯定它们是不同的，但是在我这都是可以正常工作的，希望可以方面更多的人使用。如果你遇到了任何问题，或者我哪里写的不够清楚，请告诉我，我会及时更新这篇文章。

*  **Nginx** and Gunicorn under Supervisor.
Nginx- 这个配置和正常的配置基本没啥区别，出了你要在你的virtualevn中指定一些特殊的静态路径。（因为第三方库安装的位置变了）

静态文件要指向 virtualenv的目录

```
location /static/admin {
  autoindex on;
  root   /home/ubuntu/app/venv/lib/python2.7/site-packages/django/contrib/admin/;
}
```

*  **Gunicorn** - 我用一个shell脚本来配置Gunicorn的 路径变量和选项

```
#!/bin/bash
set -e
DJANGODIR=/home/ubuntu/app
DJANGO_SETTINGS_MODULE=app.settings.prod

LOGFILE=/var/log/gunicorn/guni-app.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2
# user/group to run as
USER=ubuntu
GROUP=ubuntu
cd /home/ubuntu/app
source /home/ubuntu/app/venv/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

test -d $LOGDIR || mkdir -p $LOGDIR
exec /home/ubuntu/app/venv/bin/gunicorn_django -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE -b 0.0.0.0:8000 2>>$LOGFILE
```

* **Supevisor** - 这里就直接把Gunicorn的配置文件指向shell脚本

```
[program:gunicorn-myapp]
directory = /home/ubuntu/myapp
user = ubuntu
command = /home/ubuntu/myapp/scripts/start.sh
stdout_logfile = /var/log/gunicorn/myapp-std.log
stderr_logfile = /var/log/gunicorn/myapp-err.log
```

*  **Celery**  在 Supervisor下
这种情况下我们配置 Supervisor 去启动 virtualenv路径下的 celery。一个很酷的特性就是可以指定环境变量 -在这里是通过 Django的 settings 模块

```
[program:celery]
; Set full path to celery program if using virtualenv
command=/home/ubuntu/myapp/venv/bin/celery worker -A myapp --loglevel=INFO

directory=/home/ubuntu/myapp
user=nobody
numprocs=1
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker.log
autostart=true
autorestart=true
startsecs=10

environment =
  DJANGO_SETTINGS_MODULE=myapp.settings.prod
```

*  **Fabric.**
思路就是确保所有的远程命令在 激活的virtualenv环境下工作。

```
from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager

env.activate = 'source /home/ubuntu/myapp/venv/bin/activate'
env.directory = '/home/ubuntu/myapp'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

@hosts(env.roledefs['db'])
def rebuild_index():
    with virtualenv():
        run("python manage.py rebuild_index")
```

