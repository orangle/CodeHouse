uwsgi+nginx deploy django project
=========================

##version
* django version:1.6
* os version: Centos 6.2
* nginx version: 1.4.2
* uwsgi version: 2.0.8
* python version: 2.7.5

##directory
1 django project is in **/home/erya/hawk** and settings.py is at **/home/erya/hawk/settings.py**
2  **nginx conf** is at  **/usr/local/nginx/conf**

##deployment
* This is not a exhaustive reference, I assume all the softwares were installed correct.
* I record some key point when deploy the project.
* the web client <-> the web server <-> the socket <-> uwsgi <-> Django

###small test
use django dev server:   python manage.py runserver 8000   OK!
use uwsgi setup django:  uwsgi --http :8000 --module wsgi    OK!

it seems ok, the important parts coming!
###uwsgi configure
create uwsgi.ini file in django project directorythe file's content is :

    [uwsgi]

    chdir=/home/erya/hawk
    module=wsgi

    master=True
    processes=10
    pidfile=/home/erya/hawk.pid
    vacuum=True
    max-requests=5000
    enable-threads=True
    socket=127.0.0.1:9001

###nginx configure
check  **uwsgi_params ** file in nginx conf or you can donwload it from github https://github.com/nginx/nginx/blob/master/conf/uwsgi_params
and put it in nginx conf directory.

add uwsgi.conf file,the content is :

    server {
            listen 8000;
            server_name 127.0.0.1;
    #       client_max_body_size 64M;
            location / {
    #           client_max_body_size 4M;
                uwsgi_pass   127.0.0.1:9001;
                include     uwsgi_params;
                access_log  off;
            }
    }

add one line to nginx.conf ,like

    http {
        include       mime.types;
        default_type  application/octet-stream;


        sendfile        on;
        #tcp_nopush     on;

        #keepalive_timeout  0;
        keepalive_timeout  65;

        #gzip  on;
        include uwsgi.conf;    ####here
        ...
        server {
            ....

###start up(the use have the permission)
uwsgi: in project directory

    uwsgi --ini uwsgi.ini

nginx:

    /usr/local/nginx/sbin/nginx

###Test
The you can open your favorite browser, type http://127.0.0.1:8000 , you will see your project's index page.
Of course, what i do is very simple, you can config custom configure of your project.

###REF
[django_and_nginx](http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html)
