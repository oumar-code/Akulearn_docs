/**
 * Authentication Context for Phase 5.
 * Provides global authentication state and methods.
 */

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authAPI, userAPI, AuthAPIError } from '../api/auth';
import { tokenStorage } from '../utils/tokenStorage';
import type {
  User,
  LoginCredentials,
  RegisterData,
  UserUpdate,
  AuthContextType
} from '../types/auth';

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// ============================================================================
// Auth Provider Component
// ============================================================================

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  
  // ========================================================================
  // Initialize - Load user from storage
  // ========================================================================
  
  useEffect(() => {
    const initAuth = async () => {
      try {
        const storedAuth = tokenStorage.load();
        
        if (storedAuth) {
          setUser(storedAuth.user);
          
          // Check if token needs refresh
          if (tokenStorage.needsRefresh()) {
            await refreshToken();
          }
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        tokenStorage.clear();
      } finally {
        setIsLoading(false);
      }
    };
    
    initAuth();
  }, []);
  
  // ========================================================================
  // Auto-refresh token before expiry
  // ========================================================================
  
  useEffect(() => {
    if (!user) return;
    
    // Check every minute if token needs refresh
    const interval = setInterval(async () => {
      if (tokenStorage.needsRefresh()) {
        try {
          await refreshToken();
        } catch (error) {
          console.error('Auto-refresh failed:', error);
        }
      }
    }, 60 * 1000); // 1 minute
    
    return () => clearInterval(interval);
  }, [user]);
  
  // ========================================================================
  // Authentication Actions
  // ========================================================================
  
  const register = useCallback(async (data: RegisterData): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await authAPI.register(data);
      
      // Save tokens and user
      tokenStorage.save({
        access_token: response.tokens.access_token,
        refresh_token: response.tokens.refresh_token,
        user: response.user,
        expires_in: response.tokens.expires_in,
      });
      
      setUser(response.user);
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Registration failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const login = useCallback(async (credentials: LoginCredentials): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await authAPI.login(credentials);
      
      // Save tokens and user
      tokenStorage.save({
        access_token: response.tokens.access_token,
        refresh_token: response.tokens.refresh_token,
        user: response.user,
        expires_in: response.tokens.expires_in,
      });
      
      setUser(response.user);
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Login failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const logout = useCallback(async (): Promise<void> => {
    try {
      setIsLoading(true);
      const token = tokenStorage.getAccessToken();
      
      if (token) {
        try {
          await authAPI.logout(token);
        } catch (error) {
          // Ignore logout API errors
          console.error('Logout API failed:', error);
        }
      }
      
      // Clear local state
      tokenStorage.clear();
      setUser(null);
      setError(null);
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const refreshToken = useCallback(async (): Promise<void> => {
    const refreshToken = tokenStorage.getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    try {
      const response = await authAPI.refreshToken(refreshToken);
      
      // Update access token
      tokenStorage.updateAccessToken(
        response.access_token,
        response.expires_in
      );
    } catch (error) {
      // If refresh fails, logout user
      console.error('Token refresh failed:', error);
      await logout();
      throw error;
    }
  }, [logout]);
  
  // ========================================================================
  // User Profile Actions
  // ========================================================================
  
  const updateProfile = useCallback(async (data: UserUpdate): Promise<void> => {
    const token = tokenStorage.getAccessToken();
    
    if (!token) {
      throw new Error('Not authenticated');
    }
    
    try {
      setIsLoading(true);
      setError(null);
      
      const updatedUser = await userAPI.updateProfile(token, data);
      
      // Update local state and storage
      tokenStorage.updateUser(updatedUser);
      setUser(updatedUser);
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Profile update failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const deleteAccount = useCallback(async (): Promise<void> => {
    const token = tokenStorage.getAccessToken();
    
    if (!token) {
      throw new Error('Not authenticated');
    }
    
    try {
      setIsLoading(true);
      await userAPI.deleteAccount(token);
      
      // Clear local state
      tokenStorage.clear();
      setUser(null);
      setError(null);
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  // ========================================================================
  // Email Verification Actions
  // ========================================================================
  
  const verifyEmail = useCallback(async (email: string, otp: string): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      
      await authAPI.verifyEmail({ email, otp });
      
      // Update user's email_verified status
      if (user && user.email === email) {
        const updatedUser = { ...user, email_verified: true };
        tokenStorage.updateUser(updatedUser);
        setUser(updatedUser);
      }
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Email verification failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [user]);
  
  const resendVerification = useCallback(async (): Promise<void> => {
    const token = tokenStorage.getAccessToken();
    
    if (!token) {
      throw new Error('Not authenticated');
    }
    
    try {
      setIsLoading(true);
      setError(null);
      await authAPI.resendVerification(token);
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Resend verification failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  // ========================================================================
  // Password Reset Actions
  // ========================================================================
  
  const forgotPassword = useCallback(async (email: string): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      await authAPI.forgotPassword({ email });
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Password reset request failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  const resetPassword = useCallback(async (
    token: string,
    newPassword: string
  ): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      await authAPI.resetPassword({ token, new_password: newPassword });
    } catch (error) {
      const message = error instanceof AuthAPIError
        ? error.message
        : 'Password reset failed';
      setError(message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  // ========================================================================
  // Utility Actions
  // ========================================================================
  
  const clearError = useCallback(() => {
    setError(null);
  }, []);
  
  // ========================================================================
  // Context Value
  // ========================================================================
  
  const value: AuthContextType = {
    user,
    isAuthenticated: user !== null,
    isLoading,
    error,
    
    // Actions
    login,
    register,
    logout,
    refreshToken,
    updateProfile,
    deleteAccount,
    verifyEmail,
    resendVerification,
    forgotPassword,
    resetPassword,
    
    // Utilities
    clearError,
  };
  
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// ============================================================================
// Hook to use Auth Context
// ============================================================================

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};
