# Embeddings Visualization

## Prepare Data
Tested on cat dogs dataset from https://www.kaggle.com/c/dogs-vs-cats. Organized into the following format
```
embeddings_visualization
| - data
    | - cat
        | - cat.0.jpg
        | - cat.1.jpg
        ...
    | - dog
        | - dog.0.jpg
        | - dog.1.jpg
        ...
```

## How to Run
1. Create docker container with 
```
docker build -t embedding_visualization .
```
2. Edit variables in `run_docker.sh` accordingly and run 
```
bash run_docker.sh
```
3. Generate embeddings with 
```
cd /workspace/testbeds/embeddings_visualization
python generate_embeddings.py
```
4. Run tensorboard with 
```
tensorboard --logdir=runs --bind_all
```
5. Open your browser and go to localhost:6006

6. Change dropdown list on the homepage bar to projection and enjoy