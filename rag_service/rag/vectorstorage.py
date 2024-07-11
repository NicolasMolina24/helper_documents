import pandas as pd
# from pymilvus import MilvusClient
import chromadb
from langchain_openai import OpenAIEmbeddings

def search_in_collections(collections, uri, query_embedded, limit=5):
    chroma_client = chromadb.PersistentClient(path=uri)
    data_df = []
    for coll in collections:
        # get the collection
        collection = chroma_client.get_or_create_collection(name=coll)
        # query the collection
        results = collection.query(
            query_embeddings=query_embedded,
            n_results=limit # how many results to return
        )

        # get the included data  'metadatas', 'documents', 'distances'
        data = {data: results[data][0] for data in results['included']}
        data_df.append(pd.DataFrame(data))
    data = pd.concat(data_df)
    data = data.sort_values(by="distances").reset_index(drop=True)
    data_metadatas = data["metadatas"].apply(lambda x: pd.Series(x))
    data.drop(columns=["metadatas"], inplace=True)
    data = pd.concat([data, data_metadatas], axis=1)
    data = data.head(limit)
    print("This was the most relevant data", data)
    return data

# def search_in_collections(collections, uri, query_embedded, limit=5) -> pd.DataFrame:
#     """Get the most similar documents to the query in multiple collections

#     Args:
#         collections (list): List of collection names
#         uri (str): URI of the Milvus database
#         query_embedded (np.array): Query embedded
#         limit (int): Number of results to return

#     Returns:
#         pd.DataFrame: Dataframe with the results"""
#     data = []
#     client = MilvusClient(uri)
#     for coll in collections:
#         results = client.search(
#             collection_name=coll,
#             data=query_embedded,
#             limit=limit,
#             output_fields=["pk", "page", "source", "text"],
#         )
#         # Add collection name to the results
#         data += [dict(item, name_collection=coll) for item in results[0]]
#     #
#     client.close()
#     data = pd.DataFrame(data)
#     # sort by distance column and reset index
#     data = data.sort_values(by="distance").reset_index(drop=True)
#     # delete the entity column and add the text column
#     data_entity = data["entity"].apply(lambda x: pd.Series(x))
#     data.drop(columns=["entity"], inplace=True)
#     data = pd.concat([data, data_entity], axis=1)
#     data = data.head(limit)
#     print("This was the most relevant data", data)
#     return data


def retriever_vectorstore(collections, uri, question):
    """Get the context from the most similar documents to the query

    Args:
        collections (list): List of collection names
        uri (str): URI of the Milvus database
        question (str): Query

    Returns:
        str: Context"""
    embeddings = OpenAIEmbeddings()
    query_embedded = embeddings.embed_documents([question])
    retrieved_docs = search_in_collections(
        collections, uri, query_embedded, limit=5)
    context = retrieved_docs.apply(
        lambda x: f"[<<collection={x['source']}>> : [text: {x['documents']}]]", 
        axis=1)
    context = "\n\n".join(list(context))
    return context
