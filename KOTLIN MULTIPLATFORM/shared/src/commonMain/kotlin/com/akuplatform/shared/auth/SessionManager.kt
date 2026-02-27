package com.akuplatform.shared.auth

import com.akuplatform.shared.auth.model.AkuSession
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Manages both the Supabase session and Wave3 JWT in memory.
 * Persists tokens via TokenStorage (platform-specific).
 */
class SessionManager(private val tokenStorage: TokenStorage) {

    private val _session = MutableStateFlow<AkuSession?>(null)
    val session: StateFlow<AkuSession?> = _session.asStateFlow()

    val isLoggedIn: Boolean get() = _session.value != null

    fun setSession(session: AkuSession) {
        _session.value = session
        tokenStorage.saveSupabaseToken(session.supabaseSession.accessToken)
        tokenStorage.saveSupabaseRefreshToken(session.supabaseSession.refreshToken)
        tokenStorage.saveWave3Token(session.wave3Token)
    }

    fun clearSession() {
        _session.value = null
        tokenStorage.clearAll()
    }

    fun getWave3Token(): String? = _session.value?.wave3Token
    fun getSupabaseAccessToken(): String? = _session.value?.supabaseSession?.accessToken
}
