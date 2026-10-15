"""Core bootstrap endpoint integration tests."""
from fastapi.testclient import TestClient

from app.auth.services import create_access_token
from app.main import app

client = TestClient(app)


def test_bootstrap_requires_authentication():
    """Test bootstrap endpoint requires JWT token."""
    response = client.get("/api/v1/app/bootstrap")
    assert response.status_code == 401


def test_bootstrap_shopper_cannot_access_ops_summary(sample_customer, auth_token):
    """Test shopper role gets 403 when requesting includeOps=true."""
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 403
    error = response.json()
    assert error["error"]["code"] == "FORBIDDEN_ROLE_SCOPE"


def test_bootstrap_operator_can_access_ops_summary(sample_customer):
    """Test operator role can access ops summary."""
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "ops_summary" in data
    assert data["ops_summary"] is not None
    assert "open_slot_alerts" in data["ops_summary"]
    assert "promotion_warnings" in data["ops_summary"]
    assert "negative_sentiment_products" in data["ops_summary"]


def test_bootstrap_returns_profile(sample_customer, auth_token):
    """Test bootstrap returns customer profile."""
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "profile" in data
    assert data["profile"]["customer_id"] == sample_customer.customer_id
    assert data["profile"]["name"] == sample_customer.full_name
    assert data["profile"]["loyalty_points"] == 420


def test_bootstrap_returns_empty_lists_when_no_data(sample_customer, auth_token):
    """Test bootstrap handles empty data gracefully."""
    response = client.get(
        "/api/v1/app/bootstrap",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # These should be empty arrays when no data exists
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert "shopping_lists" in data
    assert isinstance(data["shopping_lists"], list)
    assert "featured_categories" in data
    assert isinstance(data["featured_categories"], list)


def test_ops_summary_has_no_pii(sample_customer):
    """Test ops summary does not expose PII."""
    operator_token, _ = create_access_token(
        customer_id=sample_customer.customer_id,
        role="operator"
    )
    
    response = client.get(
        "/api/v1/app/bootstrap?includeOps=true",
        headers={"Authorization": f"Bearer {operator_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    ops_summary = data["ops_summary"]
    
    # Verify only aggregate counts, no PII
    assert "open_slot_alerts" in ops_summary
    assert "promotion_warnings" in ops_summary
    assert "negative_sentiment_products" in ops_summary
    
    # Verify no PII fields
    assert "customer_name" not in str(ops_summary)
    assert "phone" not in str(ops_summary).lower()
    assert sample_customer.full_name not in str(ops_summary)
