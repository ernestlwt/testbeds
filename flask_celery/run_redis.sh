docker run -d --rm \
    -p 6379:6379 \
    --name celery_redis \
    redis