/**
 * API client for Phase 5 authentication endpoints.
 */

import type {
  User,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  TokenResponse,
  MessageResponse,
  UserUpdate,
  EmailVerificationRequest,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  APIError
} from '../types/auth';

// API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ============================================================================
// Helper Functions
// ============================================================================

class AuthAPIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public detail?: string
  ) {
    super(message);
    this.name = 'AuthAPIError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error: APIError = await response.json().catch(() => ({
      message: 'An error occurred',
    }));
    
    throw new AuthAPIError(
      error.message,
      response.status,
      error.detail
    );
  }
  
  return response.json();
}

function getAuthHeaders(token?: string): HeadersInit {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  return headers;
}

// ============================================================================
// Authentication API
// ============================================================================

export const authAPI = {
  /**
   * Register a new user account.
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    
    return handleResponse<AuthResponse>(response);
  },
  
  /**
   * Login with email and password.
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(credentials),
    });
    
    return handleResponse<AuthResponse>(response);
  },
  
  /**
   * Logout current user.
   */
  async logout(token: string): Promise<MessageResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      headers: getAuthHeaders(token),
    });
    
    return handleResponse<MessageResponse>(response);
  },
  
  /**
   * Refresh access token using refresh token.
   */
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    
    return handleResponse<TokenResponse>(response);
  },
  
  /**
   * Verify email with OTP.
   */
  async verifyEmail(data: EmailVerificationRequest): Promise<MessageResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/verify-email`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    
    return handleResponse<MessageResponse>(response);
  },
  
  /**
   * Resend verification OTP.
   */
  async resendVerification(token: string): Promise<MessageResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/resend-verification`, {
      method: 'POST',
      headers: getAuthHeaders(token),
    });
    
    return handleResponse<MessageResponse>(response);
  },
  
  /**
   * Request password reset.
   */
  async forgotPassword(data: ForgotPasswordRequest): Promise<MessageResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/forgot-password`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    
    return handleResponse<MessageResponse>(response);
  },
  
  /**
   * Reset password with token.
   */
  async resetPassword(data: ResetPasswordRequest): Promise<MessageResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/reset-password`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    
    return handleResponse<MessageResponse>(response);
  },
};

// ============================================================================
// User API
// ============================================================================

export const userAPI = {
  /**
   * Get current user profile.
   */
  async getProfile(token: string): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/api/users/me`, {
      method: 'GET',
      headers: getAuthHeaders(token),
    });
    
    return handleResponse<User>(response);
  },
  
  /**
   * Update user profile.
   */
  async updateProfile(token: string, data: UserUpdate): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/api/users/me`, {
      method: 'PUT',
      headers: getAuthHeaders(token),
      body: JSON.stringify(data),
    });
    
    return handleResponse<User>(response);
  },
  
  /**
   * Delete user account.
   */
  async deleteAccount(token: string): Promise<MessageResponse> {
    const response = await fetch(`${API_BASE_URL}/api/users/me`, {
      method: 'DELETE',
      headers: getAuthHeaders(token),
    });
    
    return handleResponse<MessageResponse>(response);
  },
};

// Export error class
export { AuthAPIError };
