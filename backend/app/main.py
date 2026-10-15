"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.addresses.routes import router as addresses_router
from app.auth.routes import router as auth_router
from app.bootstrap.routes import router as bootstrap_router
from app.cart_checkout.routes import router as cart_checkout_router
from app.catalog.routes import router as catalog_router
from app.customers.routes import router as customers_router
from app.errors import AppException
from app.fulfillment.routes import router as fulfillment_router
from app.loyalty_orders.routes import router as loyalty_orders_router
from app.notifications.routes import router as notifications_router
from app.operations.routes import router as operations_router
from app.payments.routes import router as payments_router
from app.recommendations.routes import router as recommendations_router
from app.reviews.routes import router as reviews_router
from app.shopping_lists.routes import router as shopping_lists_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Database tables are created via Alembic migrations
    # No need to call Base.metadata.create_all() here
    yield


app = FastAPI(
    title="GreenBasket AI API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler for AppException
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Handle application exceptions with unified error envelope."""
    error_response = exc.to_response()
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error_response.model_dump()}
    )

# Register routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(customers_router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(catalog_router, prefix="/api/v1/catalog", tags=["catalog"])
app.include_router(addresses_router, prefix="/api/v1/addresses", tags=["addresses"])
app.include_router(recommendations_router)
app.include_router(shopping_lists_router)
app.include_router(cart_checkout_router)
app.include_router(fulfillment_router)
app.include_router(payments_router, prefix="/api/v1/payments", tags=["payments"])
app.include_router(reviews_router, prefix="/api/v1/orders", tags=["reviews"])
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(loyalty_orders_router)
app.include_router(operations_router)
app.include_router(bootstrap_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "GreenBasket AI API", "version": "0.1.0"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
