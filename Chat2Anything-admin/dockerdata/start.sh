#!/bin/bash

# Wait for MySQL container to be ready
echo "Waiting for MySQL container to start..."
until mysql -h mysql -uroot -p123456 -e ";" 2>/dev/null; do
    echo "MySQL container not ready, sleeping for 5 seconds..."
    sleep 5
done
echo "MySQL container started successfully!"

# to start create the dababase
echo " start to create the databse... "
mysql -uroot -p123456 -hmysql -e 'CREATE DATABASE PearAdminFlask DEFAULT CHARSET UTF8;'


# Initialize Flask database
echo "Initializing Flask database..."
flask db init
flask db migrate
flask db upgrade
flask admin init

# Start gunicorn application
echo "Starting gunicorn application..."
exec gunicorn -c gunicorn.conf.py "applications:create_app()"