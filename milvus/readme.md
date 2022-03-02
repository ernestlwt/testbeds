### Useful links for milvus

[docs](https://milvus.io/docs)

[github](https://github.com/milvus-io/milvus)

### Installing Milvus Standalone

[link](https://milvus.io/docs/install_standalone-docker.md)

Download docker compose using
```
wget https://github.com/milvus-io/milvus/releases/download/v2.0.0-rc7/milvus-standalone-docker-compose.yml -O docker-compose.yml
```

Run with `docker-compose up -d`

### From Milvus tutorial

1. start milvus standalone
```
bash start_milvus.sh
```
1. start redis
```
bash start_redis.sh
```
1. install python packages
```
pip install -r requirements.txt
```
