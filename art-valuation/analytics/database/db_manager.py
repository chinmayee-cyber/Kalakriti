from pymongo import MongoClient
import pandas as pd
from config.settings import MONGO_URI, MONGO_DB, MONGO_COLLECTION

def load_artworks_from_mongo() -> pd.DataFrame:
    client = MongoClient(MONGO_URI)
    coll = client[MONGO_DB][MONGO_COLLECTION]
    docs = list(coll.find({}))
    
    if not docs:
        raise RuntimeError("No documents found in the collection.")
    
    df = pd.DataFrame(docs)
    # Ensure expected fields exist
    for f in ("artist", "medium", "dim1", "dim2", "year_created", "sale_date", 
              "value", "img_embedding", "zero_shot_tags", "auction_house", "gallery"):
        if f not in df.columns:
            df[f] = None
    
    # Normalize data
    df["dim1"] = pd.to_numeric(df["dim1"], errors="coerce")
    df["dim2"] = pd.to_numeric(df["dim2"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["area"] = df["dim1"] * df["dim2"]
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    
    return df