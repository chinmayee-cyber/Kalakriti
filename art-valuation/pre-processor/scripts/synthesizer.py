#!/usr/bin/env python3
"""
populate_artwork_fields.py

Connects to a MongoDB collection and updates up to 50 documents by adding:
 - sale_date (random datetime between 2024-01-01 and 2025-01-01)
 - auction_house (one of 4 names, skewed distribution)
 - sold (bool; ~80% True, ~20% False)
 - year_created (random int between 2019 and 2022)

Edit MONGO_URI, DB_NAME, COLLECTION_NAME at the top before running.
"""

from pymongo import MongoClient, UpdateOne
from datetime import datetime, timedelta
import random

# ---------- MACROS ----------
MONGO_URI = "mongodb+srv://shrijulv_db_user:databaseuser123@kalakriti.antxk6w.mongodb.net/"
DB_NAME = "datasets"                                                # <-- replace
COLLECTION_NAME = "auction-sales"                                # <-- replace
# --------------------------------

# Auction houses & skewed weights (sum to 1.0)
AUCTION_HOUSES = [
    ("Sotheby's", 0.50),
    ("Christie's", 0.25),
    ("Phillips", 0.15),
    ("Gallery Ekahi", 0.10)
]

MAX_DOCS = 50  # number of documents to update (user said "all 50 documents")

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 1, 1)  # exclusive upper bound


def random_datetime_between(start: datetime, end: datetime) -> datetime:
    """Return random datetime between start (inclusive) and end (exclusive)."""
    delta = end - start
    # convert to total seconds (may include microseconds)
    int_seconds = int(delta.total_seconds())
    rand_seconds = random.randint(0, int_seconds - 1)
    # keep microsecond resolution by adding random microseconds too
    rand_micro = random.randint(0, 999_999)
    return start + timedelta(seconds=rand_seconds, microseconds=rand_micro)


def build_skewed_assignment_list(n: int, items_with_weights):
    """Return a list of length n with each item assigned according to given weights (skewed)."""
    labels = [item for item, _ in items_with_weights]
    weights = [w for _, w in items_with_weights]

    # compute integer counts per weight (floor) then distribute remainder to largest weights
    raw_counts = [int(w * n) for w in weights]
    assigned = sum(raw_counts)
    remainder = n - assigned
    # distribute remainder to indices in order of descending fractional parts (or simply by weight)
    # we'll distribute to the largest weights first
    idxs_by_weight = sorted(range(len(weights)), key=lambda i: weights[i], reverse=True)
    i = 0
    while remainder > 0:
        raw_counts[idxs_by_weight[i % len(weights)]] += 1
        remainder -= 1
        i += 1

    # build list
    out = []
    for lbl, cnt in zip(labels, raw_counts):
        out.extend([lbl] * cnt)
    # shuffle so the pattern isn't grouped
    random.shuffle(out)
    return out


def main():
    # connect
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]

    total_docs_in_collection = coll.count_documents({})
    to_process = min(total_docs_in_collection, MAX_DOCS)
    if to_process == 0:
        print("No documents found in collection. Exiting.")
        return

    print(f"Collection {DB_NAME}.{COLLECTION_NAME} contains {total_docs_in_collection} documents.")
    print(f"Will update {to_process} document(s) (first {to_process}).")

    # fetch the _id values for the first to_process documents (preserves natural order)
    docs = list(coll.find({}, {"_id": 1}).limit(to_process))
    ids = [d["_id"] for d in docs]

    # Build assignments
    # 1) auction houses skewed
    auction_assignments = build_skewed_assignment_list(len(ids), AUCTION_HOUSES)

    # 2) sold booleans: 80% True, 20% False
    n_true = int(round(0.8 * len(ids)))
    n_false = len(ids) - n_true
    sold_list = [True] * n_true + [False] * n_false
    random.shuffle(sold_list)

    # 3) sale_date random per doc
    sale_dates = [random_datetime_between(START_DATE, END_DATE) for _ in range(len(ids))]

    # 4) year_created random between 2019 and 2022 (inclusive)
    year_createds = [random.randint(2019, 2022) for _ in range(len(ids))]

    # Prepare bulk updates
    updates = []
    for _id, ah, sold_val, sale_dt, yc in zip(ids, auction_assignments, sold_list, sale_dates, year_createds):
        updates.append(
            UpdateOne(
                {"_id": _id},
                {
                    "$set": {
                        "sale_date": sale_dt,
                        "auction_house": ah,
                        "sold": bool(sold_val),
                        "year_created": int(yc),
                    }
                }
            )
        )

    # Execute bulk write
    result = coll.bulk_write(updates, ordered=False)
    print("Bulk update done.")
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

    # Print distribution summary
    # auction house counts
    from collections import Counter
    ah_counter = Counter(auction_assignments)
    sold_counter = Counter(sold_list)
    year_counter = Counter(year_createds)

    print("\nSummary of assignments (for the updated set):")
    print("Auction houses distribution:")
    for k, v in ah_counter.most_common():
        print(f" - {k}: {v}")

    print(f"\nSold counts: True={sold_counter[True]}, False={sold_counter[False]}")
    print("\nYear created distribution:")
    for k, v in sorted(year_counter.items()):
        print(f" - {k}: {v}")

    # show 5 sample updated documents (projection)
    sample = list(coll.find({}, {"sale_date": 1, "auction_house": 1, "sold": 1, "year_created": 1}).limit(5))
    print("\nSample updated documents (first 5):")
    for doc in sample:
        print(doc)

    client.close()


if __name__ == "__main__":
    main()
