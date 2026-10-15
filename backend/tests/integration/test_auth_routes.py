"""Integration tests for auth routes."""
import json


def test_login_success_shopper(client, test_customer):
    """Test successful shopper login."""
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919876543210",
        "otp_or_password": "password123",
        "role_hint": "shopper"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert "expires_in_seconds" in data
    assert data["expires_in_seconds"] > 0
    
    assert "user" in data
    user = data["user"]
    assert user["customer_id"] == "cust-test-001"
    assert user["full_name"] == "Test Shopper"
    assert user["phone_number"] == "+919876543210"
    assert user["role"] == "shopper"


def test_login_success_operator(client, test_operator):
    """Test successful operator login."""
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919123456789",
        "otp_or_password": "operator123",
        "role_hint": "operator"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["user"]["role"] == "operator"
    assert data["user"]["customer_id"] == "cust-op-001"


def test_login_invalid_phone_format(client):
    """Test login with invalid phone number format returns 422."""
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "9876543210",  # Missing +91
        "otp_or_password": "password123",
        "role_hint": "shopper"
    })
    
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "PHONE_FORMAT_INVALID"


def test_login_wrong_password(client, test_customer):
    """Test login with wrong password returns 401."""
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919876543210",
        "otp_or_password": "wrong_password",
        "role_hint": "shopper"
    })
    
    assert response.status_code == 401
    error = response.json()["error"]
    assert error["code"] == "INVALID_CREDENTIALS"
    assert "trace_id" in error


def test_login_nonexistent_user(client):
    """Test login with nonexistent user returns 401."""
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919999999999",
        "otp_or_password": "password123",
        "role_hint": "shopper"
    })
    
    assert response.status_code == 401
    error = response.json()["error"]
    assert error["code"] == "INVALID_CREDENTIALS"


def test_jwt_token_includes_exp_and_role(client, test_customer):
    """Verify JWT token includes exp and role claims."""
    import jwt

    from app.config import settings
    
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919876543210",
        "otp_or_password": "password123",
        "role_hint": "shopper"
    })
    
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # Decode to inspect claims
    decoded = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    
    assert "exp" in decoded, "Token must include exp claim"
    assert "role" in decoded, "Token must include role claim"
    assert decoded["role"] == "shopper"


def test_operator_role_mismatch_denied(client, test_customer):
    """Test operator role hint with shopper account is denied."""
    response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919876543210",
        "otp_or_password": "password123",
        "role_hint": "operator"
    })
    
    assert response.status_code == 401


def test_protected_route_requires_token(client):
    """Test protected route without token returns 401."""
    response = client.get("/api/v1/customers/me")
    
    assert response.status_code == 401


def test_protected_route_with_valid_token(client, test_customer):
    """Test protected route with valid token succeeds."""
    # Login first
    login_response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919876543210",
        "otp_or_password": "password123",
        "role_hint": "shopper"
    })
    
    token = login_response.json()["access_token"]
    
    # Access protected route
    response = client.get(
        "/api/v1/customers/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == "cust-test-001"


def test_profile_update_creates_audit_log(client, test_customer, test_db):
    """Test profile update creates audit log entry."""
    # Login
    login_response = client.post("/api/v1/auth/login", json={
        "phone_number": "+919876543210",
        "otp_or_password": "password123",
        "role_hint": "shopper"
    })
    
    token = login_response.json()["access_token"]
    
    # Update profile
    response = client.put(
        "/api/v1/customers/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "Updated Name",
            "allergies": ["peanuts", "shellfish"]
        }
    )
    
    assert response.status_code == 200
    
    # Verify audit log was created
    from app.models.audit_log import AuditLog
    audit_logs = test_db.query(AuditLog).filter(
        AuditLog.entity_type == "customer",
        AuditLog.entity_id == "cust-test-001",
        AuditLog.action == "profile_update"
    ).all()
    
    assert len(audit_logs) > 0, "Audit log should be created for profile update"
    
    audit_log = audit_logs[0]
    assert audit_log.actor_id == "cust-test-001"
    
    # Verify payload contains update data
    payload = json.loads(audit_log.payload_json)
    assert payload["full_name"] == "Updated Name"
    assert payload["allergies"] == ["peanuts", "shellfish"]
