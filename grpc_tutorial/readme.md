# Learning grpc basics

Following tutorial from https://www.velotio.com/engineering-blog/grpc-implementation-using-python

### Unary service
- create `.proto` file
- generate stubs with `python -m grpc_tools.protoc --proto_path=. ./unary.proto --python_out=. --grpc_python_out=.`
- you should see `unary_pb2.py` and `unary_pb2_grpc.py` created
- create server file
- create client file
- run server
- run client


### Unary service
- same as above but generate stubs with `python -m grpc_tools.protoc --proto_path=. ./bidirectional.proto --python_out=. --grpc_python_out=.`