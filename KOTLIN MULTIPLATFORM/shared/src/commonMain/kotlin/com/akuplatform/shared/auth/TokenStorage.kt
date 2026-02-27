package com.akuplatform.shared.auth

/**
 * Platform-specific secure token storage.
 * Android: EncryptedSharedPreferences via Android Keystore.
 * iOS: Keychain.
 */
interface TokenStorage {
    fun saveSupabaseToken(token: String)
    fun saveSupabaseRefreshToken(token: String)
    fun saveWave3Token(token: String)
    fun getSupabaseToken(): String?
    fun getSupabaseRefreshToken(): String?
    fun getWave3Token(): String?
    fun clearAll()
}
