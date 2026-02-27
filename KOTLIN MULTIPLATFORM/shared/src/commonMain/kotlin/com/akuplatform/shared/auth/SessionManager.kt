package com.akuplatform.shared.auth

import com.akuplatform.shared.auth.model.AuthToken
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class SessionManager(private val tokenStorage: TokenStorage) {

    private val _isLoggedIn = MutableStateFlow(false)
    val isLoggedIn: StateFlow<Boolean> = _isLoggedIn.asStateFlow()

    suspend fun initialize() {
        _isLoggedIn.value = tokenStorage.getToken() != null
    }

    suspend fun saveSession(token: AuthToken) {
        tokenStorage.saveToken(token)
        _isLoggedIn.value = true
    }

    suspend fun clearSession() {
        try {
            tokenStorage.clearToken()
        } finally {
            _isLoggedIn.value = false
        }
    }

    suspend fun getToken(): AuthToken? = tokenStorage.getToken()
}
