from pymilvus import connections, list_collections

HOST = "127.0.0.1"
PORT = "19530"


# establish connections
connections.add_connection(default={"host": HOST, "port": PORT})
connections.connect()

collection_list = list_collections()
if len(collection_list) == 0:
    # create collection
    from pymilvus import Collection, DataType, FieldSchema, CollectionSchema

    dim = 128
    collection_schema = CollectionSchema(
        fields=[
            FieldSchema(name="id", dtype=DataType.INT64, description="pk"),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ],
        primary_field="id",
        auto_id=True,
        description="test collection"
    )
    collection = Collection(name="my_collection", schema=collection_schema)
    collection_list = list_collections()

# list collections
print(collection_list)