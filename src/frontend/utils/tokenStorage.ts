/**
 * Secure token storage utility for Phase 5 authentication.
 * Handles encryption and secure storage of JWT tokens.
 */

import type { StoredAuth, User } from '../types/auth';

const STORAGE_KEY = 'akulearn_auth';
const ENCRYPTION_KEY = 'akulearn_encryption_key'; // TODO: Use proper encryption in production

// ============================================================================
// Simple XOR "encryption" (for demonstration only)
// In production, use Web Crypto API or a proper encryption library
// ============================================================================

function simpleEncrypt(text: string): string {
  const key = ENCRYPTION_KEY;
  let result = '';
  
  for (let i = 0; i < text.length; i++) {
    result += String.fromCharCode(
      text.charCodeAt(i) ^ key.charCodeAt(i % key.length)
    );
  }
  
  return btoa(result); // Base64 encode
}

function simpleDecrypt(encoded: string): string {
  try {
    const text = atob(encoded); // Base64 decode
    const key = ENCRYPTION_KEY;
    let result = '';
    
    for (let i = 0; i < text.length; i++) {
      result += String.fromCharCode(
        text.charCodeAt(i) ^ key.charCodeAt(i % key.length)
      );
    }
    
    return result;
  } catch (error) {
    console.error('Decryption failed:', error);
    return '';
  }
}

// ============================================================================
// Token Storage
// ============================================================================

export const tokenStorage = {
  /**
   * Save authentication data to secure storage.
   */
  save(auth: {
    access_token: string;
    refresh_token: string;
    user: User;
    expires_in: number;
  }): void {
    try {
      const expiresAt = Date.now() + (auth.expires_in * 1000);
      
      const storedAuth: StoredAuth = {
        access_token: auth.access_token,
        refresh_token: auth.refresh_token,
        user: auth.user,
        expires_at: expiresAt,
      };
      
      const encrypted = simpleEncrypt(JSON.stringify(storedAuth));
      localStorage.setItem(STORAGE_KEY, encrypted);
    } catch (error) {
      console.error('Failed to save auth data:', error);
    }
  },
  
  /**
   * Load authentication data from storage.
   */
  load(): StoredAuth | null {
    try {
      const encrypted = localStorage.getItem(STORAGE_KEY);
      if (!encrypted) {
        return null;
      }
      
      const decrypted = simpleDecrypt(encrypted);
      if (!decrypted) {
        return null;
      }
      
      const auth: StoredAuth = JSON.parse(decrypted);
      
      // Check if token is expired
      if (Date.now() > auth.expires_at) {
        this.clear();
        return null;
      }
      
      return auth;
    } catch (error) {
      console.error('Failed to load auth data:', error);
      this.clear();
      return null;
    }
  },
  
  /**
   * Update access token (after refresh).
   */
  updateAccessToken(accessToken: string, expiresIn: number): void {
    try {
      const auth = this.load();
      if (!auth) {
        return;
      }
      
      auth.access_token = accessToken;
      auth.expires_at = Date.now() + (expiresIn * 1000);
      
      const encrypted = simpleEncrypt(JSON.stringify(auth));
      localStorage.setItem(STORAGE_KEY, encrypted);
    } catch (error) {
      console.error('Failed to update access token:', error);
    }
  },
  
  /**
   * Update user data.
   */
  updateUser(user: User): void {
    try {
      const auth = this.load();
      if (!auth) {
        return;
      }
      
      auth.user = user;
      
      const encrypted = simpleEncrypt(JSON.stringify(auth));
      localStorage.setItem(STORAGE_KEY, encrypted);
    } catch (error) {
      console.error('Failed to update user:', error);
    }
  },
  
  /**
   * Clear authentication data from storage.
   */
  clear(): void {
    localStorage.removeItem(STORAGE_KEY);
  },
  
  /**
   * Get access token.
   */
  getAccessToken(): string | null {
    const auth = this.load();
    return auth?.access_token || null;
  },
  
  /**
   * Get refresh token.
   */
  getRefreshToken(): string | null {
    const auth = this.load();
    return auth?.refresh_token || null;
  },
  
  /**
   * Get user.
   */
  getUser(): User | null {
    const auth = this.load();
    return auth?.user || null;
  },
  
  /**
   * Check if user is authenticated.
   */
  isAuthenticated(): boolean {
    const auth = this.load();
    return auth !== null;
  },
  
  /**
   * Check if token needs refresh (expires in less than 5 minutes).
   */
  needsRefresh(): boolean {
    const auth = this.load();
    if (!auth) {
      return false;
    }
    
    const fiveMinutes = 5 * 60 * 1000;
    return (auth.expires_at - Date.now()) < fiveMinutes;
  },
};
