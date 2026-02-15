/**
 * TypeScript types for Phase 5 authentication system.
 */

// ============================================================================
// User Types
// ============================================================================

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  display_name: string | null;
  avatar_url: string | null;
  target_exam: string | null;
  target_subjects: string[] | null;
  email_verified: boolean;
  is_active: boolean;
  created_at: string;
  last_login: string | null;
}

export interface UserUpdate {
  full_name?: string;
  display_name?: string;
  avatar_url?: string;
  target_exam?: string;
  target_subjects?: string[];
}

// ============================================================================
// Authentication Types
// ============================================================================

export interface LoginCredentials {
  email: string;
  password: string;
  device_info?: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  display_name?: string;
  target_exam?: string;
  target_subjects?: string[];
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  user: User;
  tokens: TokenResponse;
  message: string;
}

export interface MessageResponse {
  message: string;
  success: boolean;
}

// ============================================================================
// Email Verification Types
// ============================================================================

export interface EmailVerificationRequest {
  email: string;
  otp: string;
}

// ============================================================================
// Password Reset Types
// ============================================================================

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  new_password: string;
}

// ============================================================================
// API Error Types
// ============================================================================

export interface APIError {
  message: string;
  detail?: string;
  error_code?: string;
}

// ============================================================================
// Auth Context Types
// ============================================================================

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
  updateProfile: (data: UserUpdate) => Promise<void>;
  deleteAccount: () => Promise<void>;
  verifyEmail: (email: string, otp: string) => Promise<void>;
  resendVerification: () => Promise<void>;
  forgotPassword: (email: string) => Promise<void>;
  resetPassword: (token: string, newPassword: string) => Promise<void>;
  
  // Utilities
  clearError: () => void;
}

// ============================================================================
// Storage Types
// ============================================================================

export interface StoredAuth {
  access_token: string;
  refresh_token: string;
  user: User;
  expires_at: number;
}
