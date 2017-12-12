#/bin/bash
#!/bin/sh

NAME=python
echo $NAME
ID=`ps -ef | grep "$NAME" | grep -v "grep" | awk '{print $2}'`
echo $ID
echo "---------------"
for id in $ID
do
kill -9 $id
echo "killed $id"
done
echo "------kill process success---------"
python manage.py collectstatic --settings=blogproject.settings.production
nohup gunicorn --worker-class=gevent blogproject.wsgi:application >log.txt &
cat log.txt
