from pymongo import MongoClient
from pprint import pprint
from datetime import datetime

def get_database():
   
    CONNECTION_STRING = "mongodb://localhost:27017"

    client = MongoClient(CONNECTION_STRING)

    return client["lab4"]

db = get_database()

# ------
# Part 1
db.items.drop()

# 1
db.items.insert_many([
    {
        "_id": 1,
        "category": "Phone",
        "model": "iPhone 6",
        "producer": "Apple",
        "price": 100,
        "color": "black",
        "camera": "8MP"
    },
    {
        "_id": 2,
        "category": "Phone",
        "model": "iPhone 7",
        "producer": "Apple",
        "price": 150,
        "color": "silver",
        "camera": "12MP"
    },
    {
        "_id": 3,
        "category": "Phone",
        "model": "Galaxy S8",
        "producer": "Samsung",
        "price": 180,
        "camera": "12MP"
    },
    {
        "_id": 4,
        "category": "Laptop",
        "model": "MacBook Air",
        "producer": "Apple",
        "price": 700,
        "color": "black",
        "processor": "Intel Core i5",
        "RAM": "8GB"
    },
    {
        "_id": 5,
        "category": "Laptop",
        "model": "XPS 13",
        "producer": "Dell",
        "price": 850,
        "processor": "Intel Core i7",
        "RAM": "16GB"
    }
])

# 2
res = db.items.find({})
pprint(list(res), sort_dicts=False)

# 3
res = db.items.count_documents({"category": "Phone"})
print(res)

# 4
res = len(db.items.distinct("category"))
print(res)

# 5
res = db.items.distinct("producer")
pprint(list(res), sort_dicts=False)

# 6
res = db.items.find({
   "category": "Phone",
   "price": {"$gte": 120, "$lte": 160}
})
pprint(list(res), sort_dicts=False)

res = db.items.find({
   "$or": [{"model": "iPhone 6"}, {"model": "iPhone 7"}]
})
pprint(list(res), sort_dicts=False)

res = db.items.find({
   "producer": {"$in": ["Samsung", "Dell"]}
})
pprint(list(res), sort_dicts=False)

# 7
# update iPhone 6's price
db.items.update_one(
   {"model": "iPhone 6"},
   {"$set": {"price": 120}}
)
pprint(list(db.items.find({"model": "iPhone 6"})), sort_dicts=False)

# add operating system for iPhones
db.items.update_many(
   {"model": {"$regex": "iphone", "$options": "i"}},
   {"$set": {"operating_system": "iOS"}}
)
pprint(list(db.items.find({})), sort_dicts=False)

# 8
res = db.items.find({
   "color": {"$exists": True}
})
pprint(list(res), sort_dicts=False)

# 9
db.items.update_many(
    {"color": {"$exists": True}},
    {"$inc": {"price": 5}}
)
pprint(list(db.items.find({})), sort_dicts=False)

# ------
# Part 2
db.orders.drop()

# 1
db.orders.insert_many([
    {    
        "order_number": 1,
        "date": datetime(2025, 1, 1),
        "total_sum": 260,
        "customer": {
            "name": "Andrii",
            "surname": "Rodinov",
            "phones": [1234567],
            "address": "PTI, Peremohy 37, Kyiv, UA"
        },
        "payment": {
            "card_owner": "Andrii Rodionov",
            "card_id": 12345678
        },
        "items_id": [1, 2]
    },
    {
        "order_number": 2,
        "date": datetime(2025, 2, 15),
        "total_sum": 810,
        "customer": {
            "name": "Dmytro",
            "surname": "Kovalenko",
            "phones": [987654321, 5551212],
            "address": "Khreschatyk St, 7, Kyiv, UA"
        },
        "payment": {
            "card_owner": "D. Kovalenko",
            "card_id": 87654321
        },
        "items_id": [1, 4]
    },
    {
        "order_number": 3,
        "date": datetime(2025, 3, 1),
        "total_sum": 1660,
        "customer": {
            "name": "Dmytro",
            "surname": "Kovalenko",
            "phones": [987654321, 5551212],
            "address": "Khreschatyk St, 7, Kyiv, UA"
        },
        "payment": {
            "card_owner": "D. Kovalenko",
            "card_id": 87654321
        },
        "items_id": [5]
    }
])

# 2
res = db.orders.find({})
pprint(list(res), sort_dicts=False)

# 3
res = db.orders.find({
    "total_sum": {"$gt": 1000}
})
pprint(list(res), sort_dicts=False)

# 4
res = db.orders.find({
    "customer.name": "Dmytro",
    "customer.surname": "Kovalenko"
})
pprint(list(res), sort_dicts=False)

# 5
res = db.orders.find({
    "items_id": 1
})
pprint(list(res), sort_dicts=False)

# 6
db.orders.update_many(
    {"items_id": 1},
    {
        "$addToSet": {"items_id": 3},
        "$inc": {"total_sum": 180}
    }
)
pprint(list(db.orders.find({})), sort_dicts=False)

# 7
res = db.orders.find(
    {"order_number": 1},
    {"_id": 0, "number_of_items": {"$size": "$items_id"}}
)
pprint(list(res), sort_dicts=False)

# 8
res = db.orders.find(
    {"total_sum": {"$gt": 600}},
    {"_id": 0, "customer": 1, "card_id": "$payment.card_id"}
)
pprint(list(res), sort_dicts=False)

# 9
db.orders.update_many(
    {"date": {"$gte": datetime(2025, 1, 1), "$lt": datetime(2025, 2, 1)}},
    {"$pull": {"items_id": 2}}
)
pprint(list(db.orders.find({})), sort_dicts=False)

# 10
db.orders.update_many(
    {"customer.name": "Dmytro", "customer.surname": "Kovalenko"},
    {"$set": {"customer.name": "Borys"}}
)
pprint(list(db.orders.find({})), sort_dicts=False)

# 11
res = db.orders.aggregate([
    {
        "$match": {"customer.name": "Borys", "customer.surname": "Kovalenko"}
    },
    {
        "$lookup": 
        {
            "from": "items",
            "localField": "items_id",
            "foreignField": "_id",
            "pipeline": [{
                "$project": {"_id": 0, "name": "$model", "price": 1}
            }],
            "as": "items"
        }
    },
    {
        "$project": {"_id": 0, "customer": 1, "items": 1}
    }
])
pprint(list(res), sort_dicts=False)


# Part 3
db.reviews.drop()
db.create_collection(
    "reviews",
    capped=True,
    size=10000,
    max=5
)
db.reviews.insert_many([
    {
        "date": datetime(2025, 1, 1),
        "text": "Review 1.",
        "rating": "1",
    },
    {
        "date": datetime(2025, 1, 2),
        "text": "Review 2.",
        "rating": "2",
    },
    {
        "date": datetime(2025, 1, 3),
        "text": "Review 3.",
        "rating": "3",
    },
    {
        "date": datetime(2025, 1, 4),
        "text": "Review 4.",
        "rating": "4",
    },
    {
        "date": datetime(2025, 1, 5),
        "text": "Review 5.",
        "rating": "5",
    }
])

# 1
pprint(list(db.reviews.find({})), sort_dicts=False)
db.reviews.insert_one({
    "date": datetime(2025, 1, 5),
        "text": "Review 6.",
        "rating": "5",
})
pprint(list(db.reviews.find({})), sort_dicts=False)

