#!/bin/sh

if [ "$DATABASE_TYPE" = "postgresql" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Migrating djRDO..."
python manage.py flush
python manage.py migrate
echo "Done !"
echo "Loading demo data ..."
python manage.py loaddata demo.json
echo "Done !"
echo "Collecting static files ..."
python manage.py collectstatic  --noinput
echo "Done !"

exec "$@"
