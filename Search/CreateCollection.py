from qdrant_client.http.models import Distance, VectorParams, models, Filter, FieldCondition, Range
from qdrant_client import QdrantClient

client = QdrantClient("localhost", port=6333)

# client.create_collection(
#     collection_name="unknown_collection",
#     vectors_config=VectorParams(size=1536, distance=Distance.DOT),
# )

collection_name = 'unknown_collection'
vector_id = '25294200-2d30-4108-8812-893dee50c1ba'  # Replace with the ID of the vector you want to retrieve

search_result = client.search(
    collection_name=collection_name, query_vector=[0]*1536, limit=1
)

print(search_result)


# client.delete(
#     collection_name="unknown_collection",
#     points_selector=models.PointIdsList(
#         points=['25294200-2d30-4108-8812-893dee50c1ba'],
#     ),
# )