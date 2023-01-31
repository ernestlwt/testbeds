# WSL Tips

- Expose gpu to containers spawned from docker-compose. From [here](https://docs.docker.com/compose/gpu-support/)
```
services:
  test:
    image: nvidia/cuda:10.2-base
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```