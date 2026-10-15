import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ErrorBoundary } from './components/ErrorBoundary';
import { ProtectedRoute } from './components/ProtectedRoute';
import { OnboardingLogin } from './pages/OnboardingLogin';
import { Home } from './pages/Home';
import { CategorySearch } from './pages/CategorySearch';
import { ProductDetail } from './pages/ProductDetail';
import { Cart } from './pages/Cart';
import { Checkout } from './pages/Checkout';
import { OrderTracking } from './pages/OrderTracking';
import ShoppingLists from './pages/ShoppingLists';
import ProfileNotifications from './pages/ProfileNotifications';
import AdminDashboard from './pages/AdminDashboard';
import Notifications from './pages/Notifications';
import Loyalty from './pages/Loyalty';
import Orders from './pages/Orders';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<OnboardingLogin />} />
            
            {/* Protected routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Navigate to="/shop" replace />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/shop"
              element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/shop/categories"
              element={
                <ProtectedRoute>
                  <CategorySearch />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/shop/product/:id"
              element={
                <ProtectedRoute>
                  <ProductDetail />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/shop/cart"
              element={
                <ProtectedRoute>
                  <Cart />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/shop/checkout"
              element={
                <ProtectedRoute>
                  <Checkout />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/shop/orders/:id"
              element={
                <ProtectedRoute>
                  <OrderTracking />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/planner/lists"
              element={
                <ProtectedRoute>
                  <ShoppingLists />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/account"
              element={
                <ProtectedRoute>
                  <ProfileNotifications />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/account/notifications"
              element={
                <ProtectedRoute>
                  <Notifications />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/account/loyalty"
              element={
                <ProtectedRoute>
                  <Loyalty />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/account/orders"
              element={
                <ProtectedRoute>
                  <Orders />
                </ProtectedRoute>
              }
            />
            
            {/* Operator-only routes */}
            <Route
              path="/ops"
              element={
                <ProtectedRoute requiredRole="operator">
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            
            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/shop" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ErrorBoundary>
  );
};

export default App;
