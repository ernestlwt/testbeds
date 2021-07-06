# For me to learn rabbitmq
Tutorials follows content from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html


### Requirements for simple classifier
- cuda 10.1
- cudnn 7.6
- the rest can be found on requirements.txt

### To run simple classifier
1. Navigate to `testbeds/rabbitmq` and run:
```
bash start_rabbitmq.sh
```

2. Navigate to `./simple_classifier` and run:
```
# 1st terminal
python classifier_server.py

# 2nd terminal
python client.py
```