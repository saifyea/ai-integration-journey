import chromadb
from chromadb.utils import embedding_functions
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client_ai = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ✅ Chroma Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# ✅ Embedding Function
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# ✅ Collections বানাও
products_col = chroma_client.get_or_create_collection(
    name="products",
    embedding_function=embedding_fn
)

policy_col = chroma_client.get_or_create_collection(
    name="store_policy",
    embedding_function=embedding_fn
)

# ✅ Products Data যোগ করো
products_data = [
    {
        "id": "p1",
        "text": "Bangladesh Map Puzzle দাম ৪৫০ টাকা। বয়স ৫-১২ বছর। ৬৪টি জেলা। পরিবেশবান্ধব কাঠ।",
        "metadata": {"category": "puzzle", "price": 450, "age_min": 5}
    },
    {
        "id": "p2",
        "text": "Magic Drawing Board দাম ৩৫০ টাকা। বয়স ৩-১০ বছর। LCD board। বারবার মুছে আঁকা যায়।",
        "metadata": {"category": "drawing", "price": 350, "age_min": 3}
    },
    {
        "id": "p3",
        "text": "Flash Cards দাম ২৫০ টাকা। বয়স ৩-৬ বছর। ৩০টি কার্ড। বর্ণমালা ও সংখ্যা শেখায়।",
        "metadata": {"category": "cards", "price": 250, "age_min": 3}
    }
]

# Add to collection
products_col.upsert(
    ids=[p["id"] for p in products_data],
    documents=[p["text"] for p in products_data],
    metadatas=[p["metadata"] for p in products_data]
)
print(f"✅ Products added: {products_col.count()}")

# Policy Data
policy_data = [
    {
        "id": "pol1",
        "text": "Return policy: ৭ দিনের মধ্যে return করা যাবে। অব্যবহৃত থাকতে হবে।",
        "metadata": {"type": "return"}
    },
    {
        "id": "pol2",
        "text": "Delivery: ঢাকায় ১-২ দিন। ঢাকার বাইরে ৩-৫ দিন। সারা বাংলাদেশে।",
        "metadata": {"type": "delivery"}
    },
    {
        "id": "pol3",
        "text": "Payment: bKash, Nagad, রকেট এবং Cash on Delivery।",
        "metadata": {"type": "payment"}
    }
]

policy_col.upsert(
    ids=[p["id"] for p in policy_data],
    documents=[p["text"] for p in policy_data],
    metadatas=[p["metadata"] for p in policy_data]
)
print(f"✅ Policies added: {policy_col.count()}")


def search_with_filter(query, price_max=None, age=None):
    print(f"\n🔍 Query: {query}")
    # Build filter
    where = {}
    if price_max:
        where["price"] = {"$lte": price_max}
    if age:
        where["age_min"] = {"$lte": age}

    # Search
    if where:
        results = products_col.query(
            query_texts=[query],
            n_results=3,
            where=where
        )
    else:
        results = products_col.query(
            query_texts=[query],
            n_results=3
        )
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(docs, metas):
        print(f"✅ {doc[:60]}...")
        print(f"   Price: ৳{meta.get('price', 'N/A')}")

    return docs

# Test searches
search_with_filter("শিশুদের জন্য educational toy")
search_with_filter("সস্তা product", price_max=300)
search_with_filter("৩ বছরের বাচ্চার জন্য", age=3)

def chroma_rag(question):
    print(f"\n❓ {question}")

    # Search both collections
    product_results = products_col.query(
        query_texts=[question], n_results=2
    )
    policy_results = policy_col.query(
        query_texts=[question], n_results=2
    )

    # Context বানাও
    context = "Products:\n"
    context += "\n".join(product_results["documents"][0])
    context += "\n\nPolicies:\n"
    context += "\n".join(policy_results["documents"][0])

    # AI call
    response = client_ai.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"""তথ্য:
{context}

প্রশ্ন: {question}
বাংলায় সংক্ষেপে উত্তর দাও:"""
        }]
    )

    print(f"✅ {response.content[0].text}")

# Test
chroma_rag("৩০০ টাকার মধ্যে কোন product পাবো?")
chroma_rag("bKash এ payment করা যাবে?")
chroma_rag("৫ বছরের বাচ্চার জন্য কোনটা ভালো?")