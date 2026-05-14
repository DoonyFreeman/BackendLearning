

docker network create my-network

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=my-network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16


docker run --name booking_cache \
    -p 7379:6379 \
    --network=my-network \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network=my-network \
    boooking_image

docker run --name booking_celery_worker \
    --network=my-network \
    boooking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=my-network \
    boooking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

dicker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx

docker build -t boooking_image .