import grpc
import unary_pb2_grpc as pb2_grpc
import unary_pb2 as pb2

class UnaryClient(object):

    def __init__(self):
        self.host = "localhost"
        self.server_port = 50051

        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port)
        )

        self.stub = pb2_grpc.UnaryStub(self.channel)

    def get_url(self, message):
        message = pb2.Message(message=message)
        print(message)
        return self.stub.GetServerResponse(message)

if __name__ == "__main__":
    client = UnaryClient()
    result = client.get_url(message="Hello server are you there?")
    print(result)
