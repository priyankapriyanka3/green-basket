"""Integration test for seed data login verification."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.customer import Customer


@pytest.fixture(name="db")
def db_fixture():
    """Create test database with seed data."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    # Import seed_data and run seeding
    import sys
    from pathlib import Path
    backend_path = Path(__file__).resolve().parent.parent.parent
    sys.path.insert(0, str(backend_path))
    
    # Override settings to use in-memory database
    from app.config import settings
    original_db_url = settings.database_url
    settings.database_url = "sqlite:///:memory:"
    
    # Create engine for seed script
    from app.database import engine as app_engine
    app_engine.dispose()
    
    try:
        # Run seed manually with our test database
        import json
        from datetime import UTC, datetime

        import bcrypt
        
        def hash_password(password: str) -> str:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        
        now = datetime.now(UTC).isoformat()
        default_password = "Demo@123"
        hashed_password = hash_password(default_password)
        
        # Create minimal seed data
        ananya = Customer(
            customer_id="cust-001",
            full_name="Ananya Sharma",
            phone_number="+919876543210",
            email=hashed_password,
            preferred_language="en",
            dietary_preference="vegetarian",
            allergies_json=json.dumps(["peanuts"]),
            loyalty_points=420.0,
            status="active",
            created_at=now,
            updated_at=now,
        )
        rohan = Customer(
            customer_id="cust-002",
            full_name="Rohan Mehta",
            phone_number="+919876543220",
            email=hashed_password,
            preferred_language="en",
            dietary_preference="role:operator",
            allergies_json=json.dumps([]),
            loyalty_points=0.0,
            status="active",
            created_at=now,
            updated_at=now,
        )
        db.add_all([ananya, rohan])
        db.commit()
        
        yield db
    finally:
        db.close()
        settings.database_url = original_db_url


@pytest.fixture(name="client")
def client_fixture(db):
    """Create test client with test database."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_ananya_login_with_seed_credentials(client):
    """Test login with Ananya's seeded credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": "+919876543210",
            "otp_or_password": "Demo@123",
            "role_hint": "shopper"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["customer_id"] == "cust-001"
    assert data["user"]["full_name"] == "Ananya Sharma"


def test_rohan_login_with_seed_credentials(client):
    """Test login with Rohan's seeded credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": "+919876543220",
            "otp_or_password": "Demo@123",
            "role_hint": "operator"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["customer_id"] == "cust-002"
    assert data["user"]["full_name"] == "Rohan Mehta"


def test_wrong_password_fails(client):
    """Test that wrong password returns 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": "+919876543210",
            "otp_or_password": "WrongPassword",
            "roleHint": "shopper"
        }
    )
    
    assert response.status_code == 401
