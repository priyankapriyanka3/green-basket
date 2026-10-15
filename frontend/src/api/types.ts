// API Types matching LLD Section 3 contracts

export interface ApiError {
  error: {
    code: string;
    message: string;
    traceId: string;
    details?: Array<{
      field: string;
      reason: string;
    }>;
  };
}

export interface LoginRequest {
  phoneNumber: string;
  otpOrPassword: string;
  roleHint: 'shopper' | 'operator';
}

export interface LoginResponse {
  accessToken: string;
  tokenType: string;
  expiresInSeconds: number;
  user: {
    userId: string;
    role: 'shopper' | 'operator';
    displayName: string;
    preferredLanguage: string;
  };
}

export interface BootstrapResponse {
  profile: {
    customerId: string;
    name: string;
    preferredLanguage: string;
    dietaryPreference: string;
    allergies: string[];
    loyaltyPoints: number;
  };
  defaultAddress?: {
    addressId: string;
    label: string;
    postalCode: string;
    serviceability: {
      isServiceable: boolean;
      serviceZone: string;
      reason: string;
    };
  };
  featuredCategories: Array<{
    categoryId: string;
    name: string;
    iconUrl: string;
  }>;
  recommendations: Array<{
    recommendationId: string;
    productId: string;
    score: number;
    reasonTag: string;
    reasonText: string;
  }>;
  shoppingLists: Array<{
    listId: string;
    name: string;
    isAiGenerated: boolean;
    suggestionNote: string | null;
    itemCount: number;
  }>;
  opsSummary?: {
    openSlotAlerts: number;
    promotionWarnings: number;
    negativeSentimentProducts: number;
  };
}

export interface ProductCard {
  productId: string;
  name: string;
  unit: string;
  priceInr: string;
  isOrganic: boolean;
  isFeatured: boolean;
  tags: string[];
  nutrition: {
    calories?: number;
    protein?: number;
    carbs?: number;
    vitamins?: string[];
  };
  freshness?: {
    expiryDays?: number;
    harvestDate?: string;
  };
  reviewSummary?: {
    averageRating: number;
    sentiment: string;
    reviewCount: number;
  };
  farmer?: {
    farmerId: string;
    name: string;
  };
}

export interface CatalogResponse {
  categories: Array<{
    categoryId: string;
    name: string;
    isFeatured: boolean;
    parentCategoryId: string | null;
    iconUrl: string;
  }>;
  products: ProductCard[];
  page: number;
  pageSize: number;
  total: number;
}

export interface CartPricingRequest {
  items: Array<{
    productId: string;
    quantity: number;
  }>;
  discountCode?: string;
  loyaltyPointsToRedeem?: number;
}

export interface CartPricingResponse {
  cartId: string;
  pricing: {
    currency: string;
    subtotal: string;
    discountAmount: string;
    loyaltyRedemptionAmount: string;
    finalAmount: string;
  };
  appliedDiscount?: {
    code: string;
    type: string;
    value: string;
    minimumOrderThreshold: string;
  };
  lineItems: Array<{
    productId: string;
    quantity: number;
    unitPrice: string;
    lineTotal: string;
  }>;
  warnings: string[];
}

export interface CheckoutRequest {
  cartId: string;
  addressId: string;
  slotId: string;
  paymentMethod: string;
  clientAmount: string;
}

export interface CheckoutResponse {
  order: {
    orderId: string;
    status: string;
    orderDate: string;
    subtotal: string;
    discountAmount: string;
    finalAmount: string;
    deliveryAddressId: string;
    slotId: string;
  };
  payment: {
    paymentId: string;
    status: string;
    transactionReference: string;
    redirectOrIntentPayload: {
      provider: string;
      token: string;
    };
  };
  serviceability: {
    isServiceable: boolean;
    postalCode: string;
  };
}

export interface OrderDetailResponse {
  orderId: string;
  status: string;
  paymentStatus: string;
  trackingUrl: string;
  slot: {
    slotId: string;
    label: string;
  };
  deliveryAgent?: {
    agentId: string;
    name: string;
    phoneNumber: string;
    vehicleDetails: string;
    availabilityStatus: string;
  };
  loyalty: {
    pointsEarned: number;
    pointsBalance: number;
  };
  reviewEligibility: {
    canSubmit: boolean;
    reason: string;
  };
}
