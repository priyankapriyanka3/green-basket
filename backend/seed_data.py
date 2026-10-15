"""Idempotent seed data script for GreenBasket AI development data.

Creates 2 customers (Ananya shopper, Rohan operator), 2 addresses for Ananya,
6 categories, 20+ products, 3 delivery slots, 2 promotions, sample recommendations,
1 shopping list, sample order, reviews, and notifications.

Passwords hashed with bcrypt cost >= 12.
Demo credentials documented in README.md and .env.example.
"""
import json
from datetime import UTC, datetime, timedelta

import bcrypt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models.address import Address
from app.models.category import Category
from app.models.customer import Customer
from app.models.delivery_slot import DeliverySlot
from app.models.farmer import Farmer
from app.models.inventory import Inventory
from app.models.notification import Notification
from app.models.order import Order, OrderDiscount, OrderItem
from app.models.payment import Payment
from app.models.product import Product
from app.models.promotion import Promotion
from app.models.recommendation import Recommendation
from app.models.review import Review
from app.models.shopping_list import ShoppingList, ShoppingListItem


def hash_password(password: str) -> str:
    """Hash password with bcrypt cost factor 12."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def get_iso_timestamp() -> str:
    """Get current timestamp in ISO 8601 format."""
    return datetime.now(UTC).isoformat()


def seed_database():
    """Main seeding function with idempotency checks."""
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if already seeded
        existing_customer = db.execute(
            select(Customer).where(Customer.customer_id == "cust-001")
        ).scalar_one_or_none()
        
        if existing_customer:
            print("✓ Seed data already exists. Skipping seeding.")
            return
        
        print("Starting database seeding...")
        now = get_iso_timestamp()
        default_password = "Demo@123"
        hashed_password = hash_password(default_password)
        
        # === CUSTOMERS ===
        print("Creating customers...")
        customers = [
            Customer(
                customer_id="cust-001",
                full_name="Ananya Sharma",
                phone_number="+919876543210",
                email=hashed_password,  # Password stored in email field for demo
                preferred_language="en",
                dietary_preference="vegetarian",
                allergies_json=json.dumps(["peanuts"]),
                loyalty_points=420.0,
                status="active",
                created_at=now,
                updated_at=now,
            ),
            Customer(
                customer_id="cust-002",
                full_name="Rohan Mehta",
                phone_number="+919876543220",
                email=hashed_password,  # Password stored in email field for demo
                preferred_language="en",
                dietary_preference="role:operator",  # Operator role stored in dietary_preference
                allergies_json=json.dumps([]),
                loyalty_points=0.0,
                status="active",
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(customers)
        db.flush()
        
        # === ADDRESSES ===
        print("Creating addresses...")
        addresses = [
            Address(
                address_id="addr-001",
                customer_id="cust-001",
                address_line1="123 HSR Layout",
                address_line2="Sector 2",
                city="Bengaluru",
                state="Karnataka",
                postal_code="560102",
                country="India",
                latitude=12.918200,
                longitude=77.637700,
                service_zone="Bengaluru-South",
                serviceability_status="serviceable",
                serviceability_reason=None,
                is_default="true",
                created_at=now,
                updated_at=now,
            ),
            Address(
                address_id="addr-002",
                customer_id="cust-001",
                address_line1="456 Indiranagar",
                address_line2="100 Feet Road",
                city="Bengaluru",
                state="Karnataka",
                postal_code="560038",
                country="India",
                latitude=12.978300,
                longitude=77.641400,
                service_zone="Bengaluru-East",
                serviceability_status="serviceable",
                serviceability_reason=None,
                is_default="false",
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(addresses)
        db.flush()
        
        # === CATEGORIES ===
        print("Creating categories...")
        categories = [
            Category(
                category_id="cat-001",
                name="Fruits",
                description="Fresh seasonal fruits",
                parent_category_id=None,
                display_order=1,
                icon_url="https://cdn.greenbasketai.com/icons/fruits.svg",
                is_active="true",
                created_at=now,
                updated_at=now,
            ),
            Category(
                category_id="cat-002",
                name="Vegetables",
                description="Farm-fresh vegetables",
                parent_category_id=None,
                display_order=2,
                icon_url="https://cdn.greenbasketai.com/icons/vegetables.svg",
                is_active="true",
                created_at=now,
                updated_at=now,
            ),
            Category(
                category_id="cat-003",
                name="Dairy",
                description="Milk and dairy products",
                parent_category_id=None,
                display_order=3,
                icon_url="https://cdn.greenbasketai.com/icons/dairy.svg",
                is_active="true",
                created_at=now,
                updated_at=now,
            ),
            Category(
                category_id="cat-004",
                name="Staples",
                description="Rice, grains, and pulses",
                parent_category_id=None,
                display_order=4,
                icon_url="https://cdn.greenbasketai.com/icons/staples.svg",
                is_active="true",
                created_at=now,
                updated_at=now,
            ),
            Category(
                category_id="cat-005",
                name="Snacks",
                description="Healthy snacks and nuts",
                parent_category_id=None,
                display_order=5,
                icon_url="https://cdn.greenbasketai.com/icons/snacks.svg",
                is_active="true",
                created_at=now,
                updated_at=now,
            ),
            Category(
                category_id="cat-006",
                name="Beverages",
                description="Juices and drinks",
                parent_category_id=None,
                display_order=6,
                icon_url="https://cdn.greenbasketai.com/icons/beverages.svg",
                is_active="true",
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(categories)
        db.flush()
        
        # === FARMERS ===
        print("Creating farmers...")
        farmers = [
            Farmer(
                farmer_id="fmr-001",
                name="Raju's Farm",
                location="Karnataka",
                bio="Organic farming since 1995",
                created_at=now,
                updated_at=now,
            ),
            Farmer(
                farmer_id="fmr-002",
                name="Green Valley Co-op",
                location="Tamil Nadu",
                bio="Women-led cooperative farm",
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(farmers)
        db.flush()
        
        # === PRODUCTS ===
        print("Creating products...")
        products = [
            # Fruits
            Product(
                product_id="prod-001",
                category_id="cat-001",
                farmer_id="fmr-001",
                name="Organic Bananas",
                description="Fresh organic bananas from Karnataka",
                unit_price=45.00,
                unit_type="dozen",
                is_organic="true",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 89, "protein": 1.1, "carbs": 22.8, "fiber": 2.6}),
                tags_json=json.dumps(["organic", "local", "potassium-rich"]),
                image_url="https://cdn.greenbasketai.com/products/bananas.jpg",
                average_rating=4.5,
                review_count=24,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-002",
                category_id="cat-001",
                farmer_id="fmr-001",
                name="Alphonso Mangoes",
                description="Sweet Alphonso mangoes, seasonal special",
                unit_price=180.00,
                unit_type="kg",
                is_organic="true",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 60, "protein": 0.8, "carbs": 15.0, "vitamin_c": 36.4}),
                tags_json=json.dumps(["seasonal", "organic", "premium"]),
                image_url="https://cdn.greenbasketai.com/products/mangoes.jpg",
                average_rating=4.8,
                review_count=42,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-003",
                category_id="cat-001",
                farmer_id="fmr-001",
                name="Red Apples",
                description="Crisp red apples from Himachal",
                unit_price=120.00,
                unit_type="kg",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 52, "protein": 0.3, "carbs": 13.8, "fiber": 2.4}),
                tags_json=json.dumps(["fresh", "crunchy"]),
                image_url="https://cdn.greenbasketai.com/products/apples.jpg",
                average_rating=4.3,
                review_count=18,
                created_at=now,
                updated_at=now,
            ),
            # Vegetables
            Product(
                product_id="prod-004",
                category_id="cat-002",
                farmer_id="fmr-002",
                name="Organic Tomatoes",
                description="Farm-fresh organic tomatoes",
                unit_price=35.00,
                unit_type="kg",
                is_organic="true",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 18, "protein": 0.9, "carbs": 3.9, "vitamin_c": 13.7}),
                tags_json=json.dumps(["organic", "local", "vitamin-c"]),
                image_url="https://cdn.greenbasketai.com/products/tomatoes.jpg",
                average_rating=4.6,
                review_count=31,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-005",
                category_id="cat-002",
                farmer_id="fmr-002",
                name="Spinach",
                description="Fresh green spinach leaves",
                unit_price=25.00,
                unit_type="bunch",
                is_organic="true",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 23, "protein": 2.9, "carbs": 3.6, "iron": 2.7}),
                tags_json=json.dumps(["organic", "iron-rich", "leafy"]),
                image_url="https://cdn.greenbasketai.com/products/spinach.jpg",
                average_rating=4.4,
                review_count=15,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-006",
                category_id="cat-002",
                farmer_id="fmr-002",
                name="Carrots",
                description="Crunchy orange carrots",
                unit_price=40.00,
                unit_type="kg",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 41, "protein": 0.9, "carbs": 9.6, "vitamin_a": 835}),
                tags_json=json.dumps(["fresh", "vitamin-a"]),
                image_url="https://cdn.greenbasketai.com/products/carrots.jpg",
                average_rating=4.2,
                review_count=12,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-007",
                category_id="cat-002",
                farmer_id="fmr-002",
                name="Onions",
                description="Fresh red onions",
                unit_price=30.00,
                unit_type="kg",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 40, "protein": 1.1, "carbs": 9.3, "fiber": 1.7}),
                tags_json=json.dumps(["staple", "fresh"]),
                image_url="https://cdn.greenbasketai.com/products/onions.jpg",
                average_rating=4.0,
                review_count=8,
                created_at=now,
                updated_at=now,
            ),
            # Dairy
            Product(
                product_id="prod-008",
                category_id="cat-003",
                farmer_id=None,
                name="Fresh Milk",
                description="Full cream milk, 500ml",
                unit_price=28.00,
                unit_type="bottle",
                is_organic="false",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 61, "protein": 3.2, "carbs": 4.8, "fat": 3.3, "calcium": 113}),
                tags_json=json.dumps(["dairy", "calcium", "daily-essential"]),
                image_url="https://cdn.greenbasketai.com/products/milk.jpg",
                average_rating=4.7,
                review_count=56,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-009",
                category_id="cat-003",
                farmer_id=None,
                name="Greek Yogurt",
                description="Thick Greek yogurt, 400g",
                unit_price=65.00,
                unit_type="cup",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 59, "protein": 10.0, "carbs": 3.6, "fat": 0.4, "calcium": 110}),
                tags_json=json.dumps(["dairy", "protein", "probiotic"]),
                image_url="https://cdn.greenbasketai.com/products/yogurt.jpg",
                average_rating=4.5,
                review_count=22,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-010",
                category_id="cat-003",
                farmer_id=None,
                name="Paneer",
                description="Fresh cottage cheese, 200g",
                unit_price=90.00,
                unit_type="pack",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 265, "protein": 18.3, "carbs": 1.2, "fat": 20.8, "calcium": 208}),
                tags_json=json.dumps(["dairy", "protein", "vegetarian"]),
                image_url="https://cdn.greenbasketai.com/products/paneer.jpg",
                average_rating=4.6,
                review_count=28,
                created_at=now,
                updated_at=now,
            ),
            # Staples
            Product(
                product_id="prod-011",
                category_id="cat-004",
                farmer_id=None,
                name="Basmati Rice",
                description="Premium aged basmati rice, 1kg",
                unit_price=120.00,
                unit_type="kg",
                is_organic="false",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 130, "protein": 2.7, "carbs": 28.0, "fiber": 0.4}),
                tags_json=json.dumps(["staple", "premium", "aromatic"]),
                image_url="https://cdn.greenbasketai.com/products/basmati.jpg",
                average_rating=4.8,
                review_count=67,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-012",
                category_id="cat-004",
                farmer_id=None,
                name="Toor Dal",
                description="Split pigeon peas, 1kg",
                unit_price=110.00,
                unit_type="kg",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 335, "protein": 22.3, "carbs": 62.0, "fiber": 15.0}),
                tags_json=json.dumps(["staple", "protein", "pulse"]),
                image_url="https://cdn.greenbasketai.com/products/toor-dal.jpg",
                average_rating=4.4,
                review_count=19,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-013",
                category_id="cat-004",
                farmer_id=None,
                name="Whole Wheat Flour",
                description="Stone-ground atta, 5kg",
                unit_price=220.00,
                unit_type="pack",
                is_organic="true",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 340, "protein": 13.7, "carbs": 72.0, "fiber": 12.2}),
                tags_json=json.dumps(["staple", "organic", "whole-grain"]),
                image_url="https://cdn.greenbasketai.com/products/atta.jpg",
                average_rating=4.5,
                review_count=34,
                created_at=now,
                updated_at=now,
            ),
            # Snacks
            Product(
                product_id="prod-014",
                category_id="cat-005",
                farmer_id=None,
                name="Almonds",
                description="Raw California almonds, 250g",
                unit_price=180.00,
                unit_type="pack",
                is_organic="false",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 579, "protein": 21.2, "carbs": 21.6, "fat": 49.9, "vitamin_e": 25.6}),
                tags_json=json.dumps(["nuts", "protein", "healthy-fat"]),
                image_url="https://cdn.greenbasketai.com/products/almonds.jpg",
                average_rating=4.7,
                review_count=45,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-015",
                category_id="cat-005",
                farmer_id=None,
                name="Cashews",
                description="Roasted cashew nuts, 200g",
                unit_price=220.00,
                unit_type="pack",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 553, "protein": 18.2, "carbs": 30.2, "fat": 43.9}),
                tags_json=json.dumps(["nuts", "protein", "snack"]),
                image_url="https://cdn.greenbasketai.com/products/cashews.jpg",
                average_rating=4.6,
                review_count=29,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-016",
                category_id="cat-005",
                farmer_id=None,
                name="Roasted Peanuts",
                description="Lightly salted peanuts, 400g (contains allergen)",
                unit_price=95.00,
                unit_type="pack",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 567, "protein": 25.8, "carbs": 16.1, "fat": 49.2}),
                tags_json=json.dumps(["nuts", "protein", "peanut-allergen"]),
                image_url="https://cdn.greenbasketai.com/products/peanuts.jpg",
                average_rating=4.3,
                review_count=14,
                created_at=now,
                updated_at=now,
            ),
            # Beverages
            Product(
                product_id="prod-017",
                category_id="cat-006",
                farmer_id=None,
                name="Orange Juice",
                description="Freshly squeezed orange juice, 1L",
                unit_price=85.00,
                unit_type="bottle",
                is_organic="false",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 45, "protein": 0.7, "carbs": 10.4, "vitamin_c": 50}),
                tags_json=json.dumps(["fresh", "vitamin-c", "juice"]),
                image_url="https://cdn.greenbasketai.com/products/orange-juice.jpg",
                average_rating=4.5,
                review_count=38,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-018",
                category_id="cat-006",
                farmer_id=None,
                name="Green Tea",
                description="Organic green tea bags, 25 count",
                unit_price=120.00,
                unit_type="box",
                is_organic="true",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 2, "protein": 0, "carbs": 0, "antioxidants": "high"}),
                tags_json=json.dumps(["organic", "tea", "antioxidant"]),
                image_url="https://cdn.greenbasketai.com/products/green-tea.jpg",
                average_rating=4.4,
                review_count=26,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-019",
                category_id="cat-006",
                farmer_id=None,
                name="Coconut Water",
                description="Natural coconut water, 500ml",
                unit_price=50.00,
                unit_type="bottle",
                is_organic="false",
                is_featured="false",
                nutrition_json=json.dumps({"calories": 19, "protein": 0.7, "carbs": 3.7, "potassium": 250}),
                tags_json=json.dumps(["natural", "hydrating", "electrolytes"]),
                image_url="https://cdn.greenbasketai.com/products/coconut-water.jpg",
                average_rating=4.3,
                review_count=21,
                created_at=now,
                updated_at=now,
            ),
            Product(
                product_id="prod-020",
                category_id="cat-001",
                farmer_id="fmr-001",
                name="Pomegranate",
                description="Fresh juicy pomegranates",
                unit_price=140.00,
                unit_type="kg",
                is_organic="true",
                is_featured="true",
                nutrition_json=json.dumps({"calories": 83, "protein": 1.7, "carbs": 18.7, "fiber": 4.0, "vitamin_c": 10.2}),
                tags_json=json.dumps(["organic", "antioxidant", "seasonal"]),
                image_url="https://cdn.greenbasketai.com/products/pomegranate.jpg",
                average_rating=4.7,
                review_count=33,
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(products)
        db.flush()
        
        # === INVENTORY ===
        print("Creating inventory...")
        harvest_date = (datetime.now(UTC) - timedelta(days=2)).isoformat()
        expiry_date_short = (datetime.now(UTC) + timedelta(days=4)).isoformat()
        expiry_date_long = (datetime.now(UTC) + timedelta(days=30)).isoformat()
        
        inventories = [
            Inventory(inventory_id="inv-001", product_id="prod-001", stock_quantity=50, reorder_level=10, harvest_date=harvest_date, expiry_date=expiry_date_long, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-002", product_id="prod-002", stock_quantity=25, reorder_level=5, harvest_date=harvest_date, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-003", product_id="prod-003", stock_quantity=3, reorder_level=5, harvest_date=harvest_date, expiry_date=expiry_date_long, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="low_stock"),
            Inventory(inventory_id="inv-004", product_id="prod-004", stock_quantity=40, reorder_level=10, harvest_date=harvest_date, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-005", product_id="prod-005", stock_quantity=15, reorder_level=8, harvest_date=harvest_date, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-006", product_id="prod-006", stock_quantity=35, reorder_level=10, harvest_date=harvest_date, expiry_date=expiry_date_long, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-007", product_id="prod-007", stock_quantity=45, reorder_level=12, harvest_date=harvest_date, expiry_date=expiry_date_long, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-008", product_id="prod-008", stock_quantity=80, reorder_level=20, harvest_date=None, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-009", product_id="prod-009", stock_quantity=30, reorder_level=10, harvest_date=None, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-010", product_id="prod-010", stock_quantity=20, reorder_level=8, harvest_date=None, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-011", product_id="prod-011", stock_quantity=100, reorder_level=20, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-012", product_id="prod-012", stock_quantity=60, reorder_level=15, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-013", product_id="prod-013", stock_quantity=40, reorder_level=10, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-014", product_id="prod-014", stock_quantity=50, reorder_level=12, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-015", product_id="prod-015", stock_quantity=35, reorder_level=10, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-016", product_id="prod-016", stock_quantity=0, reorder_level=10, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="unavailable"),
            Inventory(inventory_id="inv-017", product_id="prod-017", stock_quantity=45, reorder_level=15, harvest_date=None, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-018", product_id="prod-018", stock_quantity=70, reorder_level=20, harvest_date=None, expiry_date=None, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-019", product_id="prod-019", stock_quantity=40, reorder_level=12, harvest_date=None, expiry_date=expiry_date_short, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
            Inventory(inventory_id="inv-020", product_id="prod-020", stock_quantity=18, reorder_level=8, harvest_date=harvest_date, expiry_date=expiry_date_long, warehouse_zone="Bengaluru-Central", last_updated_at=now, availability_status="available"),
        ]
        db.add_all(inventories)
        db.flush()
        
        # === DELIVERY SLOTS ===
        print("Creating delivery slots...")
        slot_date = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()
        delivery_slots = [
            DeliverySlot(
                slot_id="slt-001",
                slot_date=slot_date,
                start_time="08:00",
                end_time="12:00",
                label="Morning",
                max_capacity=50,
                reserved_count=0,
                is_available="true",
                service_zone="Bengaluru-South",
                created_at=now,
                updated_at=now,
            ),
            DeliverySlot(
                slot_id="slt-002",
                slot_date=slot_date,
                start_time="13:00",
                end_time="17:00",
                label="Afternoon",
                max_capacity=50,
                reserved_count=0,
                is_available="true",
                service_zone="Bengaluru-South",
                created_at=now,
                updated_at=now,
            ),
            DeliverySlot(
                slot_id="slt-003",
                slot_date=slot_date,
                start_time="18:00",
                end_time="21:00",
                label="Evening",
                max_capacity=50,
                reserved_count=0,
                is_available="true",
                service_zone="Bengaluru-South",
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(delivery_slots)
        db.flush()
        
        # === PROMOTIONS ===
        print("Creating promotions...")
        valid_from = (datetime.now(UTC) - timedelta(days=1)).isoformat()
        valid_to = (datetime.now(UTC) + timedelta(days=30)).isoformat()
        
        promotions = [
            Promotion(
                promotion_id="prm-001",
                code="FIRST10",
                description="10% off on first order",
                discount_type="percentage",
                discount_value=10.0,
                minimum_order_threshold=200.0,
                usage_limit=1000,
                usage_count=45,
                valid_from=valid_from,
                valid_to=valid_to,
                is_active="true",
                applicability_json=json.dumps({"new_customers": True}),
                created_at=now,
                updated_at=now,
            ),
            Promotion(
                promotion_id="prm-002",
                code="LOYALTY50",
                description="₹50 off for loyalty members",
                discount_type="flat",
                discount_value=50.0,
                minimum_order_threshold=500.0,
                usage_limit=5000,
                usage_count=320,
                valid_from=valid_from,
                valid_to=valid_to,
                is_active="true",
                applicability_json=json.dumps({"loyalty_tier": "silver"}),
                created_at=now,
                updated_at=now,
            ),
        ]
        db.add_all(promotions)
        db.flush()
        
        # === RECOMMENDATIONS ===
        print("Creating recommendations...")
        recommendations = [
            Recommendation(
                recommendation_id="rec-001",
                customer_id="cust-001",
                product_id="prod-001",
                score=0.92,
                reason_tag="frequently_bought",
                reason_text="You buy bananas often",
                generated_at=now,
            ),
            Recommendation(
                recommendation_id="rec-002",
                customer_id="cust-001",
                product_id="prod-004",
                score=0.88,
                reason_tag="based_on_diet",
                reason_text="Matches your vegetarian preference",
                generated_at=now,
            ),
            Recommendation(
                recommendation_id="rec-003",
                customer_id="cust-001",
                product_id="prod-002",
                score=0.85,
                reason_tag="seasonal",
                reason_text="Fresh mangoes are in season",
                generated_at=now,
            ),
            Recommendation(
                recommendation_id="rec-004",
                customer_id="cust-001",
                product_id="prod-008",
                score=0.80,
                reason_tag="reorder_reminder",
                reason_text="It's been 5 days since your last milk order",
                generated_at=now,
            ),
        ]
        db.add_all(recommendations)
        db.flush()
        
        # === SHOPPING LIST ===
        print("Creating shopping list...")
        shopping_list = ShoppingList(
            list_id="lst-001",
            customer_id="cust-001",
            name="Weekly Essentials",
            is_ai_generated="true",
            suggestion_note="Based on your weekly purchase pattern",
            created_at=now,
            updated_at=now,
        )
        db.add(shopping_list)
        db.flush()
        
        shopping_list_items = [
            ShoppingListItem(
                item_id="lsi-001",
                list_id="lst-001",
                product_id="prod-001",
                quantity=1,
                source_reason_tag="frequently_bought",
                added_at=now,
            ),
            ShoppingListItem(
                item_id="lsi-002",
                list_id="lst-001",
                product_id="prod-004",
                quantity=2,
                source_reason_tag="frequently_bought",
                added_at=now,
            ),
            ShoppingListItem(
                item_id="lsi-003",
                list_id="lst-001",
                product_id="prod-008",
                quantity=4,
                source_reason_tag="reorder_reminder",
                added_at=now,
            ),
        ]
        db.add_all(shopping_list_items)
        db.flush()
        
        # === SAMPLE ORDER ===
        print("Creating sample order...")
        order_date = (datetime.now(UTC) - timedelta(days=3)).isoformat()
        confirmed_date = (datetime.now(UTC) - timedelta(days=3, hours=1)).isoformat()
        
        order = Order(
            order_id="ord-001",
            customer_id="cust-001",
            address_id="addr-001",
            slot_id="slt-001",
            agent_id=None,
            status="delivered",
            subtotal=253.00,
            discount_amount=25.30,
            loyalty_redeemed_amount=0.0,
            final_amount=227.70,
            tracking_url="https://track.greenbasketai.com/ord-001",
            order_date=order_date,
            confirmed_at=confirmed_date,
        )
        db.add(order)
        db.flush()
        
        order_items = [
            OrderItem(
                item_id="oit-001",
                order_id="ord-001",
                product_id="prod-001",
                quantity=1,
                unit_price=45.00,
                total_price=45.00,
            ),
            OrderItem(
                item_id="oit-002",
                order_id="ord-001",
                product_id="prod-004",
                quantity=2,
                unit_price=35.00,
                total_price=70.00,
            ),
            OrderItem(
                item_id="oit-003",
                order_id="ord-001",
                product_id="prod-008",
                quantity=5,
                unit_price=28.00,
                total_price=140.00,
            ),
        ]
        db.add_all(order_items)
        db.flush()
        
        order_discount = OrderDiscount(
            order_discount_id="odc-001",
            order_id="ord-001",
            promotion_id="prm-001",
            discount_amount=25.30,
            applied_at=order_date,
        )
        db.add(order_discount)
        db.flush()
        
        # === PAYMENT ===
        print("Creating payment...")
        payment = Payment(
            payment_id="pay-001",
            order_id="ord-001",
            payment_method="upi",
            status="paid",
            amount=227.70,
            transaction_reference="TXN-20261012-ABC123",
            payment_date=confirmed_date,
        )
        db.add(payment)
        db.flush()
        
        # === REVIEWS ===
        print("Creating reviews...")
        reviewed_at = (datetime.now(UTC) - timedelta(days=1)).isoformat()
        
        reviews = [
            Review(
                review_id="rev-001",
                order_id="ord-001",
                product_id="prod-001",
                customer_id="cust-001",
                rating=5,
                review_text="Fresh and sweet bananas, great quality!",
                sentiment="positive",
                reviewed_at=reviewed_at,
            ),
            Review(
                review_id="rev-002",
                order_id="ord-001",
                product_id="prod-004",
                customer_id="cust-001",
                rating=4,
                review_text="Good tomatoes but slightly soft",
                sentiment="positive",
                reviewed_at=reviewed_at,
            ),
            Review(
                review_id="rev-003",
                order_id="ord-001",
                product_id="prod-008",
                customer_id="cust-001",
                rating=5,
                review_text="Fresh milk delivered on time",
                sentiment="positive",
                reviewed_at=reviewed_at,
            ),
        ]
        db.add_all(reviews)
        db.flush()
        
        # === NOTIFICATIONS ===
        print("Creating notifications...")
        notifications = [
            Notification(
                notification_id="ntf-001",
                customer_id="cust-001",
                order_id="ord-001",
                type="order_update",
                title="Order Confirmed",
                message="Your order #ord-001 has been confirmed and will be delivered tomorrow morning.",
                channel="in_app",
                is_read="false",
                dispatch_status="sent",
                created_at=confirmed_date,
            ),
            Notification(
                notification_id="ntf-002",
                customer_id="cust-001",
                order_id="ord-001",
                type="delivery_update",
                title="Order Delivered",
                message="Your order #ord-001 has been delivered successfully.",
                channel="push",
                is_read="true",
                dispatch_status="sent",
                created_at=reviewed_at,
            ),
            Notification(
                notification_id="ntf-003",
                customer_id="cust-001",
                order_id=None,
                type="ai_suggestion",
                title="New Recommendations",
                message="We have fresh recommendations based on your preferences!",
                channel="in_app",
                is_read="false",
                dispatch_status="sent",
                created_at=now,
            ),
        ]
        db.add_all(notifications)
        db.flush()
        
        db.commit()
        print("✓ Database seeding completed successfully!")
        print("\nDemo Credentials:")
        print("  Ananya (Shopper):")
        print("    Phone: +919876543210")
        print(f"    Password: {default_password}")
        print("    Role: shopper")
        print("  Rohan (Operator):")
        print("    Phone: +919876543220")
        print(f"    Password: {default_password}")
        print("    Role: operator")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error during seeding: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
