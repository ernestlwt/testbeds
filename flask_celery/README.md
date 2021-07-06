# Running background tasks with Celery on Flask

Commands
```
# web server
pip install -r requirements.txt
bash run_redis.sh
bash run.sh
```
```
# worker
celery -A app.task worker
```
go to localhost:5000 on web browser, 'hello' will be printed on worker terminal in 5 sec
