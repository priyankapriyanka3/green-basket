# Graph Report - green-basket  (2026-10-15)

## Corpus Check
- 171 files · ~88,042 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: (none) 6, .ini 2, .xml 2)

## Summary
- 1475 nodes · 3385 edges · 103 communities (52 shown, 51 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 355 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `df296230`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GreenBasket AI
- cart_checkout/services.py
- seed_data.py
- Address
- auth/routes.py
- test_bootstrap_core.py
- generate_shopping_list
- test_auth_routes.py
- AppException
- client
- Product
- test_catalog.py
- greenbasket-backend
- setup_database
- AddressCreateRequest
- test_shopping_lists_routes.py
- AddressService
- test_addresses.py
- RecommendationService
- ShoppingListService
- CartItemInput
- create_address
- Base
- addresses/routes.py
- fixture
- errors.py
- Order
- Customer
- pydantic
- package.json
- App.tsx
- fulfillment/services.py
- customers/routes.py
- test_recommendations.py
- PaymentProviderAdapter
- bootstrap/services.py
- ._build_address_response
- tests/conftest.py
- compilerOptions
- app_exception_handler
- catalog/services.py
- CatalogService
- NotificationService
- test_operations.py
- reviews/routes.py
- ReviewService
- validate_and_submit_checkout
- get_recommendations
- db_fixture
- ErrorDetail
- start.sh
- compilerOptions
- health
- GeoServiceAdapter
- env.py
- Payment
- payments/services.py
- test_checkout_routes.py
- stop.sh
- operations/routes.py
- OperationsService
- db_session
- require_shopper
- sample_category
- hash_password
- test_get_ops_summary
- OpsSummaryResponse
- operations_service
- override_get_db
- sample_product
- set_sqlite_pragma
- test_bootstrap_ops_summary_excludes_pii
- test_get_products_with_keyword_search
- test_get_products_filter_by_category
- test_get_products_filter_by_organic
- test_get_products_pagination
- test_product_includes_nutrition_data
- test_product_includes_freshness_data
- test_product_includes_review_summary
- test_combine_multiple_filters
- test_featured_categories_in_response
- test_availability_status_reflected

## God Nodes (most connected - your core abstractions)
1. `Base` - 59 edges
2. `Customer` - 58 edges
3. `Product` - 50 edges
4. `Order` - 46 edges
5. `AddressService` - 42 edges
6. `CatalogService` - 40 edges
7. `AppException` - 39 edges
8. `OrderItem` - 37 edges
9. `Category` - 36 edges
10. `RecommendationService` - 35 edges

## Surprising Connections (you probably didn't know these)
- `PaymentService` --uses--> `PaymentProviderAdapter`  [INFERRED]
  backend/app/payments/services.py → backend/app/adapters/payment_provider.py
- `list_addresses()` --uses--> `AddressService`  [INFERRED]
  backend/app/addresses/routes.py → backend/app/addresses/services.py
- `create_address()` --uses--> `AddressCreateRequest`  [INFERRED]
  backend/app/addresses/routes.py → backend/app/addresses/schemas.py
- `create_address()` --uses--> `AddressService`  [INFERRED]
  backend/app/addresses/routes.py → backend/app/addresses/services.py
- `get_address()` --uses--> `AddressService`  [INFERRED]
  backend/app/addresses/routes.py → backend/app/addresses/services.py

## Import Cycles
- None detected.

## Communities (103 total, 51 thin omitted)

### Community 0 - "GreenBasket AI"
Cohesion: 0.06
Nodes (30): Backend Container, Backend Setup, CI/CD Pipeline, Container Verification, Database Migrations, Database Schema, Demo Credentials, Docker Compose Services (+22 more)

### Community 1 - "cart_checkout/services.py"
Cohesion: 0.14
Nodes (7): price_cart_endpoint(), submit_checkout(), CartPricingRequest, CartPricingResponse, CheckoutRequest, CheckoutResponse, DiscountWarning

### Community 2 - "seed_data.py"
Cohesion: 0.07
Nodes (17): OrderDiscount, Recommendation, Review, ShoppingList, ShoppingListItem, docker-entrypoint.sh script, get_iso_timestamp(), hash_password() (+9 more)

### Community 3 - "Address"
Cohesion: 0.09
Nodes (12): Address, auth_token(), clean_db(), client(), sample_address(), sample_customer(), test_address_and_slot(), test_customer() (+4 more)

### Community 4 - "auth/routes.py"
Cohesion: 0.10
Nodes (9): login(), LoginRequest, LoginResponse, UserProfile, authenticate_customer(), PhoneFormatError, test_login_request_validates_role_hint(), test_phone_number_validation_accepts_valid_e164() (+1 more)

### Community 5 - "test_bootstrap_core.py"
Cohesion: 0.14
Nodes (6): test_bootstrap_operator_can_access_ops_summary(), test_bootstrap_requires_authentication(), test_bootstrap_returns_empty_lists_when_no_data(), test_bootstrap_returns_profile(), test_bootstrap_shopper_cannot_access_ops_summary(), test_ops_summary_has_no_pii()

### Community 6 - "generate_shopping_list"
Cohesion: 0.11
Nodes (7): generate_shopping_list(), get_shopping_list(), get_shopping_lists(), GenerateShoppingListRequest, GenerateShoppingListResponse, ShoppingListItemResponse, Config

### Community 7 - "test_auth_routes.py"
Cohesion: 0.09
Nodes (10): test_jwt_token_includes_exp_and_role(), test_login_invalid_phone_format(), test_login_nonexistent_user(), test_login_success_operator(), test_login_success_shopper(), test_login_wrong_password(), test_operator_role_mismatch_denied(), test_profile_update_creates_audit_log() (+2 more)

### Community 8 - "AppException"
Cohesion: 0.15
Nodes (6): AppException, test_price_cart_insufficient_loyalty_points(), test_validate_checkout_address_not_serviceable(), test_validate_checkout_amount_mismatch(), test_validate_checkout_empty_cart(), test_validate_checkout_slot_capacity_exceeded()

### Community 15 - "Product"
Cohesion: 0.08
Nodes (17): ExpiryAlert, InventoryStatus, LowStockAlert, InventoryService, Inventory, Product, sample_data(), test_calculate_freshness_indicator_expiring_soon() (+9 more)

### Community 16 - "test_catalog.py"
Cohesion: 0.09
Nodes (12): get_products(), test_combined_filters(), test_product_card_includes_farmer_info(), test_product_card_includes_freshness(), test_product_card_includes_nutrition(), test_product_card_includes_review_summary(), test_product_tags_parsed_from_json(), test_search_products_basic() (+4 more)

### Community 21 - "AddressCreateRequest"
Cohesion: 0.12
Nodes (7): AddressCreateRequest, test_create_address_not_serviceable(), test_create_address_serviceable(), test_postal_code_validation(), test_update_address(), test_update_address_make_default(), test_update_address_postal_code_revalidates()

### Community 22 - "test_shopping_lists_routes.py"
Cohesion: 0.07
Nodes (14): test_generate_shopping_list_diet_boost(), test_generate_shopping_list_seasonal_refresh(), test_generate_shopping_list_weekly_reorder(), test_generated_list_marked_as_ai_generated(), test_get_shopping_list_by_id(), test_get_shopping_lists(), test_get_shopping_lists_requires_auth(), test_shopping_list_generation_requires_auth() (+6 more)

### Community 23 - "AddressService"
Cohesion: 0.20
Nodes (5): delete_address(), AddressService, test_delete_address(), test_get_address(), test_get_address_not_found()

### Community 24 - "test_addresses.py"
Cohesion: 0.15
Nodes (6): session(), test_check_serviceability_bengaluru_postal_code(), test_check_serviceability_mumbai_postal_code(), test_check_serviceability_unsupported_postal_code(), test_check_serviceability_with_coordinates_invalid(), test_check_serviceability_with_coordinates_valid()

### Community 25 - "RecommendationService"
Cohesion: 0.11
Nodes (6): RecommendationService, test_diet_based_recommendations_respect_preferences(), test_no_recommendations_without_reason(), test_recommendation_scoring_logic(), test_seasonal_recommendations_generated(), test_trending_recommendations_generated()

### Community 26 - "ShoppingListService"
Cohesion: 0.13
Nodes (3): ShoppingListResponse, Config, ShoppingListService

### Community 27 - "CartItemInput"
Cohesion: 0.11
Nodes (10): CartItemInput, test_price_cart_basic_calculation(), test_price_cart_discount_minimum_threshold_not_met(), test_price_cart_discount_not_active(), test_price_cart_discount_usage_limit_exceeded(), test_price_cart_with_flat_discount(), query_side_effect(), test_price_cart_with_loyalty_redemption() (+2 more)

### Community 28 - "create_address"
Cohesion: 0.18
Nodes (4): create_address(), get_address(), list_addresses(), update_address()

### Community 29 - "Base"
Cohesion: 0.10
Nodes (11): upgrade(), Base, AuditLog, DeliveryAgent, Farmer, Notification, setup_test_db(), test_get_products_basic() (+3 more)

### Community 30 - "addresses/routes.py"
Cohesion: 0.27
Nodes (5): check_serviceability(), AddressResponse, AddressUpdateRequest, ServiceabilityCheckRequest, ServiceabilityInfo

### Community 31 - "fixture"
Cohesion: 0.18
Nodes (5): sample_category(), sample_farmer(), sample_inventory(), sample_product(), session()

### Community 32 - "errors.py"
Cohesion: 0.12
Nodes (11): verify_password(), verify_token(), AuthenticationError, TokenExpiredError, test_create_access_token_includes_exp_claim(), test_create_access_token_includes_role_claim(), test_verify_password_fails_for_incorrect_password(), test_verify_password_succeeds_for_correct_password() (+3 more)

### Community 33 - "Order"
Cohesion: 0.12
Nodes (6): create_access_token(), Category, Order, OrderItem, TestReviewRoutes, TestReviewRoutesSimple

### Community 34 - "Customer"
Cohesion: 0.07
Nodes (9): get_current_user(), get_db(), lifespan(), Customer, test_ananya_login_with_seed_credentials(), test_rohan_login_with_seed_credentials(), test_wrong_password_fails(), test_customer_model_create() (+1 more)

### Community 36 - "pydantic"
Cohesion: 0.10
Nodes (6): AuditLogEntry, NotificationListResponse, NotificationResponse, ProductRecommendationCard, RecommendationResponse, Config

### Community 37 - "package.json"
Cohesion: 0.05
Nodes (42): dependencies, axios, react, react-dom, react-router-dom, devDependencies, eslint, jsdom (+34 more)

### Community 39 - "App.tsx"
Cohesion: 0.06
Nodes (65): apiClient, tokenManager, ApiError, BootstrapResponse, CartPricingRequest, CartPricingResponse, CatalogResponse, CheckoutRequest (+57 more)

### Community 43 - "fulfillment/services.py"
Cohesion: 0.18
Nodes (6): get_order(), DeliveryAgentResponse, DeliverySlotResponse, OrderDetailResponse, OrderItemResponse, get_order_detail()

### Community 44 - "customers/routes.py"
Cohesion: 0.10
Nodes (9): log_audit_event(), get_my_profile(), update_my_profile(), CustomerProfileResponse, CustomerUpdateRequest, get_customer_profile(), update_customer_profile(), NotFoundError (+1 more)

### Community 45 - "test_recommendations.py"
Cohesion: 0.11
Nodes (11): db_session(), sample_category(), sample_customer(), sample_orders(), sample_products(), test_generate_reorder_recommendations(), test_preference_updates_influence_recommendations(), test_recommendation_includes_reason_text() (+3 more)

### Community 47 - "bootstrap/services.py"
Cohesion: 0.14
Nodes (9): get_bootstrap(), AddressServiceability, AddressSummary, BootstrapResponse, CategorySummary, ProfileSummary, RecommendationCard, ShoppingListSummary (+1 more)

### Community 49 - "tests/conftest.py"
Cohesion: 0.19
Nodes (5): mock_db_session(), sample_address(), sample_customer(), sample_product(), test_db()

### Community 50 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+10 more)

### Community 52 - "catalog/services.py"
Cohesion: 0.25
Nodes (7): CatalogResponse, CategoryInfo, FarmerInfo, FreshnessData, NutritionData, ProductCard, ReviewSummary

### Community 53 - "CatalogService"
Cohesion: 0.14
Nodes (5): CatalogService, test_freshness_calculation_expiry_days(), test_get_featured_categories(), test_get_low_stock_products(), test_search_products_by_organic_flag()

### Community 54 - "NotificationService"
Cohesion: 0.08
Nodes (4): NotificationProviderAdapter, get_notifications(), mark_notification_read(), NotificationService

### Community 56 - "test_operations.py"
Cohesion: 0.12
Nodes (7): test_calculate_slot_utilization_with_high_capacity(), test_calculate_slot_utilization_with_zero_capacity(), test_count_negative_sentiment_products(), test_get_notification_dispatch_performance(), test_get_promotion_warnings_identifies_low_usage(), test_get_recommendation_reason_distribution(), test_get_review_sentiment_by_category()

### Community 59 - "validate_and_submit_checkout"
Cohesion: 0.29
Nodes (3): price_cart(), validate_and_submit_checkout(), test_price_cart_discount_expired()

### Community 60 - "get_recommendations"
Cohesion: 0.15
Nodes (4): get_reason_distribution(), get_recommendations(), test_get_customer_recommendations(), test_reason_distribution_reporting()

### Community 63 - "start.sh"
Cohesion: 0.60
Nodes (5): check_prerequisites(), find_available_port(), native_path(), port_in_use(), start.sh script

### Community 64 - "compilerOptions"
Cohesion: 0.15
Nodes (12): compilerOptions, allowSyntheticDefaultImports, composite, lib, module, moduleResolution, resolveJsonModule, skipLibCheck (+4 more)

### Community 67 - "env.py"
Cohesion: 0.15
Nodes (3): run_migrations_offline(), run_migrations_online(), Settings

### Community 68 - "Payment"
Cohesion: 0.17
Nodes (3): Payment, PaymentService, TestPaymentService

### Community 69 - "payments/services.py"
Cohesion: 0.15
Nodes (4): get_payment_status(), PaymentInitRequest, PaymentInitResponse, PaymentStatusResponse

### Community 71 - "test_checkout_routes.py"
Cohesion: 0.06
Nodes (18): DeliverySlot, Promotion, test_bootstrap_with_include_ops_for_operator(), test_ops_summary_counts_promotion_warnings(), test_ops_summary_counts_slot_alerts(), test_cart_pricing_basic(), test_cart_pricing_expired_discount(), test_cart_pricing_invalid_discount() (+10 more)

### Community 73 - "operations/routes.py"
Cohesion: 0.21
Nodes (6): get_notification_dispatch_performance(), get_operations_summary(), get_promotion_warnings(), get_recommendation_reason_distribution(), get_review_sentiment_by_category(), get_slot_utilization()

### Community 77 - "db_session"
Cohesion: 0.14
Nodes (6): auth_token(), client(), db_session(), sample_category(), sample_orders(), sample_products()

### Community 79 - "require_shopper"
Cohesion: 0.33
Nodes (3): require_operator(), require_shopper(), ForbiddenRoleScopeError

### Community 80 - "sample_category"
Cohesion: 0.29
Nodes (3): sample_category(), sample_product(), session()

### Community 81 - "hash_password"
Cohesion: 0.33
Nodes (3): hash_password(), sample_customer(), test_hash_password_uses_bcrypt_cost_12()

### Community 82 - "test_get_ops_summary"
Cohesion: 0.33
Nodes (3): test_get_ops_summary(), query_side_effect(), test_ops_summary_excludes_pii()

## Knowledge Gaps
- **9 isolated node(s):** `greenbasket-backend`, `@types/node`, `@types/react`, `@types/react-dom`, `@vitest/coverage-v8` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 727 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **51 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Base` connect `Base` to `seed_data.py`, `Address`, `client`, `Product`, `test_catalog.py`, `setup_database`, `test_shopping_lists_routes.py`, `test_addresses.py`, `fixture`, `Order`, `Customer`, `test_recommendations.py`, `tests/conftest.py`, `db_fixture`, `env.py`, `Payment`, `test_checkout_routes.py`, `db_session`, `sample_category`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `Base` (e.g. with `test_db()` and `setup_test_db()`) actually correct?**
  _`Base` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `greenbasket-backend`, `@types/node`, `@types/react` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GreenBasket AI` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._
- **Why does `Product` connect `Product` to `cart_checkout/services.py`, `seed_data.py`, `Address`, `test_catalog.py`, `test_shopping_lists_routes.py`, `RecommendationService`, `ShoppingListService`, `Base`, `fixture`, `Order`, `Customer`, `fulfillment/services.py`, `test_recommendations.py`, `catalog/services.py`, `CatalogService`, `._build_product_card`, `validate_and_submit_checkout`, `OperationsService`, `db_session`, `sample_category`, `sample_product`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `Customer` (e.g. with `get_current_user()` and `require_operator()`) actually correct?**
  _`Customer` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Should `cart_checkout/services.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13666666666666666 - nodes in this community are weakly interconnected._