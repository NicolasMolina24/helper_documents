import pandas as pd

def clean_collections(collections, client):
    """ Delete collections if they exist
    
    Args:
        collections (list): List of collection names
        client (MilvusClient): Milvus client
    """
    for coll in collections:
        if client.has_collection(collection_name=coll):
            client.drop_collection(collection_name=coll)


def create_collection(collection_name, client, dim):
    """Create a collection if it does not exist
    
    Args:
        collection_name (str): Name of the collection
        client (MilvusClient): Milvus client
        dim (int): Dimension of the vectors embdings"""
    # create collection if not exists
    if not client.has_collection(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            dimension=dim,
        )
    else:
        print(f"Collection {collection_name} already exists.")
    return

def create_collections(collections, client, dim):
    """Create multiple collections
    
    Args:
        collections (list): List of collection names
        client (MilvusClient): Milvus client
        dim (int): Dimension of the vectors embdings"""
    for coll in collections:
        create_collection(coll, client, dim)
    return

def search_in_collections(collections, client, query_embedded, limit=5) -> pd.DataFrame:
    """ Get the most similar documents to the query in multiple collections
    
    Args:
        collections (list): List of collection names
        client (MilvusClient): Milvus client
        query_embedded (np.array): Query embedded
        limit (int): Number of results to return
    
    Returns:
        pd.DataFrame: Dataframe with the results"""
    data = []
    for coll in collections:
        results = client.search(
            collection_name=coll,
            data=query_embedded,
            limit=limit,
            output_fields=["id", "text"],
        )
        # Add collection name to the results
        data+=[dict(item, name_collection=coll) for item in results[0]]
    
    data = pd.DataFrame(data)
    # sort by distance column and reset index
    data = data.sort_values(by="distance").reset_index(drop=True)
    return data.head(limit)