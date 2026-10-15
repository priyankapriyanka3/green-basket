"""Unit tests for operations services."""
from unittest.mock import Mock

import pytest

from app.operations.schemas import OpsSummaryResponse
from app.operations.services import OperationsService


@pytest.fixture
def mock_db():
    """Create mock database session."""
    return Mock()


@pytest.fixture
def operations_service(mock_db):
    """Create operations service with mock db."""
    return OperationsService(mock_db)


def test_calculate_slot_utilization_with_high_capacity(operations_service, mock_db):
    """Test slot utilization calculation identifies high capacity slots."""
    # Create mock slots
    mock_slots = [
        Mock(
            slot_id="slt-001",
            slot_date="2026-10-16",
            service_zone="Mumbai-South",
            reserved_count=18,
            max_capacity=20
        ),
        Mock(
            slot_id="slt-002",
            slot_date="2026-10-16",
            service_zone="Mumbai-North",
            reserved_count=5,
            max_capacity=20
        ),
        Mock(
            slot_id="slt-003",
            slot_date="2026-10-17",
            service_zone="Mumbai-South",
            reserved_count=20,
            max_capacity=20
        ),
    ]
    
    mock_db.query.return_value.all.return_value = mock_slots
    
    result = operations_service.calculate_slot_utilization()
    
    assert result["open_alerts"] == 2  # slt-001 (90%) and slt-003 (100%)
    assert len(result["slots"]) == 3
    assert result["slots"][0]["utilization_pct"] == 90.0
    assert result["slots"][0]["is_alert"] is True
    assert result["slots"][1]["utilization_pct"] == 25.0
    assert result["slots"][1]["is_alert"] is False
    assert result["slots"][2]["utilization_pct"] == 100.0
    assert result["slots"][2]["is_alert"] is True


def test_calculate_slot_utilization_with_zero_capacity(operations_service, mock_db):
    """Test slot utilization handles zero capacity gracefully."""
    mock_slots = [
        Mock(
            slot_id="slt-001",
            slot_date="2026-10-16",
            service_zone="Mumbai-South",
            reserved_count=0,
            max_capacity=0
        ),
    ]
    
    mock_db.query.return_value.all.return_value = mock_slots
    
    result = operations_service.calculate_slot_utilization()
    
    assert result["open_alerts"] == 0
    assert result["slots"][0]["utilization_pct"] == 0


def test_get_promotion_warnings_identifies_low_usage(operations_service, mock_db):
    """Test promotion warnings identifies promotions with low usage."""
    mock_promotions = [
        Mock(
            promotion_id="prm-001",
            code="FRESH10",
            is_active=1,
            usage_count=5,
            usage_limit=100
        ),
        Mock(
            promotion_id="prm-002",
            code="ORGANIC20",
            is_active=1,
            usage_count=50,
            usage_limit=100
        ),
    ]
    
    mock_db.query.return_value.filter.return_value.all.return_value = mock_promotions
    
    result = operations_service.get_promotion_warnings()
    
    assert result["count"] == 1  # Only prm-001 has usage < 10%
    assert len(result["warnings"]) == 1
    assert result["warnings"][0]["code"] == "FRESH10"
    assert result["warnings"][0]["reason"] == "low_usage"


def test_get_recommendation_reason_distribution(operations_service, mock_db):
    """Test recommendation reason distribution aggregation."""
    # Mock query chain
    mock_query = Mock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    
    # Mock results
    mock_results = [
        Mock(reason_tag="reorder_reminder", count=45),
        Mock(reason_tag="based_on_diet", count=30),
        Mock(reason_tag="trending", count=15),
        Mock(reason_tag="seasonal", count=10),
    ]
    mock_query.all.return_value = mock_results
    
    result = operations_service.get_recommendation_reason_distribution()
    
    assert result["period_days"] == 30
    assert result["distribution"]["reorder_reminder"] == 45
    assert result["distribution"]["based_on_diet"] == 30
    assert result["distribution"]["trending"] == 15
    assert result["distribution"]["seasonal"] == 10


def test_get_review_sentiment_by_category(operations_service, mock_db):
    """Test review sentiment aggregation by category."""
    # Mock query chain
    mock_query = Mock()
    mock_db.query.return_value = mock_query
    mock_query.join.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    
    # Mock results
    mock_results = [
        Mock(category_name="Fresh Fruits", sentiment="positive", count=50),
        Mock(category_name="Fresh Fruits", sentiment="negative", count=5),
        Mock(category_name="Vegetables", sentiment="positive", count=30),
        Mock(category_name="Vegetables", sentiment="neutral", count=10),
    ]
    mock_query.all.return_value = mock_results
    
    result = operations_service.get_review_sentiment_by_category()
    
    assert "Fresh Fruits" in result["by_category"]
    assert result["by_category"]["Fresh Fruits"]["positive"] == 50
    assert result["by_category"]["Fresh Fruits"]["negative"] == 5
    assert result["by_category"]["Vegetables"]["positive"] == 30
    assert result["by_category"]["Vegetables"]["neutral"] == 10


def test_get_notification_dispatch_performance(operations_service, mock_db):
    """Test notification dispatch performance aggregation."""
    # Mock query chain
    mock_query = Mock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    
    # Mock results
    mock_results = [
        Mock(channel="push", dispatch_status="sent", count=80),
        Mock(channel="push", dispatch_status="failed", count=5),
        Mock(channel="email", dispatch_status="sent", count=60),
        Mock(channel="email", dispatch_status="pending", count=10),
        Mock(channel="in_app", dispatch_status="sent", count=100),
    ]
    mock_query.all.return_value = mock_results
    
    result = operations_service.get_notification_dispatch_performance()
    
    assert result["period_days"] == 7
    assert result["by_channel"]["push"]["sent"] == 80
    assert result["by_channel"]["push"]["failed"] == 5
    assert result["by_channel"]["email"]["sent"] == 60
    assert result["by_channel"]["email"]["pending"] == 10
    assert result["by_channel"]["in_app"]["sent"] == 100


def test_count_negative_sentiment_products(operations_service, mock_db):
    """Test counting products with majority negative reviews."""
    # Mock query chain
    mock_query = Mock()
    mock_db.query.return_value = mock_query
    mock_query.group_by.return_value = mock_query
    mock_query.having.return_value = mock_query
    
    # Mock results - products with at least 3 reviews
    mock_results = [
        Mock(product_id="prod-001", total_reviews=10, negative_count=8),  # 80% negative
        Mock(product_id="prod-002", total_reviews=5, negative_count=2),    # 40% negative
        Mock(product_id="prod-003", total_reviews=8, negative_count=6),    # 75% negative
    ]
    mock_query.all.return_value = mock_results
    
    result = operations_service.count_negative_sentiment_products()
    
    assert result == 2  # prod-001 and prod-003 have >50% negative


def test_get_ops_summary(operations_service, mock_db):
    """Test ops summary aggregates all KPIs."""
    # Mock slot utilization
    mock_slots = [
        Mock(slot_id="slt-001", slot_date="2026-10-16", service_zone="Mumbai",
             reserved_count=19, max_capacity=20),
    ]
    
    # Mock promotions
    mock_promotions = [
        Mock(promotion_id="prm-001", code="FRESH10", is_active=1,
             usage_count=3, usage_limit=100),
    ]
    
    # Mock negative sentiment query
    mock_negative_query = Mock()
    mock_negative_query.group_by.return_value = mock_negative_query
    mock_negative_query.having.return_value = mock_negative_query
    mock_negative_query.all.return_value = [
        Mock(product_id="prod-001", total_reviews=5, negative_count=4),
    ]
    
    # Setup query call sequence
    call_count = [0]
    def query_side_effect(*args):
        call_count[0] += 1
        if call_count[0] == 1:  # Slots query
            q = Mock()
            q.all.return_value = mock_slots
            return q
        elif call_count[0] == 2:  # Promotions query
            q = Mock()
            q.filter.return_value.all.return_value = mock_promotions
            return q
        else:  # Negative sentiment query
            return mock_negative_query
    
    mock_db.query.side_effect = query_side_effect
    
    result = operations_service.get_ops_summary()
    
    assert isinstance(result, OpsSummaryResponse)
    assert result.open_slot_alerts == 1
    assert result.promotion_warnings == 1
    assert result.negative_sentiment_products == 1


def test_ops_summary_excludes_pii(operations_service, mock_db):
    """Test that operations summary does not expose PII."""
    # Setup minimal mocks for all queries
    mock_negative_query = Mock()
    mock_negative_query.group_by.return_value = mock_negative_query
    mock_negative_query.having.return_value = mock_negative_query
    mock_negative_query.all.return_value = []
    
    call_count = [0]
    def query_side_effect(*args):
        call_count[0] += 1
        if call_count[0] == 1:  # Slots query
            q = Mock()
            q.all.return_value = []
            return q
        elif call_count[0] == 2:  # Promotions query
            q = Mock()
            q.filter.return_value.all.return_value = []
            return q
        else:  # Negative sentiment query
            return mock_negative_query
    
    mock_db.query.side_effect = query_side_effect
    
    result = operations_service.get_ops_summary()
    
    # Verify result only contains aggregate counts, no PII
    result_dict = result.model_dump()
    assert "customer_name" not in result_dict
    assert "phone_number" not in result_dict
    assert "allergies" not in result_dict
    assert "email" not in result_dict
