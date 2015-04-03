#! /bin/sh

PATH=/sbin:/bin:/usr/bin:/usr/sbin:/usr/local/bin
CONFIGURE=uwsgi.ini
PID_FILE=/var/portal/uwsgi.pid

case   "$@"   in
    start)
        uwsgi --ini $CONFIGURE
        echo "start uwsgi ok.."
        ;;
    stop)
        uwsgi --stop $PID_FILE
        echo "stop uwsgi ok.."
        ;;
    reload)
        uwsgi --reload $PID_FILE
        echo "reload uwsgi ok.."
        ;;
    restart)
        uwsgi --stop $PID_FILE
        sleep 1
        uwsgi --ini $CONFIGURE
        ;;
    *)
        echo 'unknown arguments (start|stop|reload|restart)'
        exit 1
        ;;
esac
