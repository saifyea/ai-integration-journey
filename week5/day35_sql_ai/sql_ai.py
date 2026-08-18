import sqlite3
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ✅ Database বানাও
def create_database():
    conn = sqlite3.connect("kids_store.db")
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        stock INTEGER,
        category TEXT,
        age_min INTEGER,
        age_max INTEGER
    )""")

    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        customer_name TEXT,
        quantity INTEGER,
        total_price INTEGER,
        status TEXT,
        order_date TEXT,
        location TEXT
    )""")

    # Customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT,
        location TEXT,
        total_orders INTEGER,
        total_spent INTEGER
    )""")

    conn.commit()
    return conn

# ✅ Sample Data যোগ করো
def insert_sample_data(conn):
    cursor = conn.cursor()

    # Products
    products = [
        (1, "Bangladesh Map Puzzle", 450, 50, "puzzle", 5, 12),
        (2, "Magic Drawing Board", 350, 80, "drawing", 3, 10),
        (3, "Flash Cards", 250, 120, "cards", 3, 6),
        (4, "Counting Beads", 180, 60, "math", 3, 7),
        (5, "Story Books Set", 380, 40, "books", 4, 10)
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?,?)",
        products
    )

    # Orders
    orders = [
        (1, 1, "Rahim", 2, 900, "delivered", "2024-01-15", "Dhaka"),
        (2, 2, "Karim", 1, 350, "delivered", "2024-01-16", "Chittagong"),
        (3, 3, "Salam", 3, 750, "pending", "2024-01-17", "Sylhet"),
        (4, 1, "Hasan", 1, 450, "delivered", "2024-01-18", "Dhaka"),
        (5, 4, "Noor", 2, 360, "delivered", "2024-01-19", "Rajshahi"),
        (6, 2, "Rina", 1, 350, "cancelled", "2024-01-20", "Dhaka"),
        (7, 5, "Mina", 1, 380, "delivered", "2024-01-21", "Khulna"),
        (8, 3, "Tina", 2, 500, "pending", "2024-01-22", "Dhaka"),
        (9, 1, "Raju", 3, 1350, "delivered", "2024-01-23", "Chittagong"),
        (10, 2, "Lima", 1, 350, "delivered", "2024-01-24", "Dhaka")
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO orders VALUES (?,?,?,?,?,?,?,?)",
        orders
    )

    # Customers
    customers = [
        (1, "Rahim", "01711111111", "Dhaka", 3, 1800),
        (2, "Karim", "01722222222", "Chittagong", 2, 700),
        (3, "Salam", "01733333333", "Sylhet", 1, 750),
        (4, "Hasan", "01744444444", "Dhaka", 4, 2200),
        (5, "Noor", "01755555555", "Rajshahi", 1, 360)
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO customers VALUES (?,?,?,?,?,?)",
        customers
    )

    conn.commit()
    print("✅ Sample data inserted!")

conn = create_database()
insert_sample_data(conn)

def nl_to_sql(question, conn):
    # Schema বানাও
    schema = """
Tables:
- products(id, name, price, stock, category, age_min, age_max)
- orders(id, product_id, customer_name, quantity, total_price, status, order_date, location)
- customers(id, name, phone, location, total_orders, total_spent)
"""

    # Claude দিয়ে SQL বানাও
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=f"""তুমি SQL expert।
এই schema দিয়ে SQL query লেখো:
{schema}

Rules:
- শুধু SELECT query লেখো
- SQL ছাড়া কিছু লিখবে না
- SQLite syntax ব্যবহার করো""",
        messages=[{
            "role": "user",
            "content": f"Question: {question}\nSQL:"
        }]
    )

    sql = response.content[0].text.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    print(f"📝 SQL: {sql}")

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return results, columns, sql
    except Exception as e:
        return None, None, str(e)


def ask_database(question, conn):
    print(f"\n❓ {question}")
    results, columns, sql = nl_to_sql(question, conn)

    if results is None:
        print(f"❌ Error: {sql}")
        return

    # Results দেখাও
    if results:
        print(f"📊 Results ({len(results)} rows):")
        print(" | ".join(columns))
        print("─" * 50)
        for row in results[:5]:
            print(" | ".join(str(v) for v in row))
    else:
        print("📭 No results found")

    # AI দিয়ে analyze করো
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"""Question: {question}
Data: {results}
Columns: {columns}

বাংলায় ২-৩ লাইনে business insight দাও:"""
        }]
    )
    print(f"🤖 Insight: {response.content[0].text}")


# Test করো
questions = [
    "সবচেয়ে বেশি বিক্রি হওয়া product কোনটা?",
    "ঢাকার orders কতটা?",
    "কোন product এর stock সবচেয়ে কম?",
    "মোট revenue কত?",
    "pending orders কতটা আছে?"
]

for q in questions:
    ask_database(q, conn)

conn.close()