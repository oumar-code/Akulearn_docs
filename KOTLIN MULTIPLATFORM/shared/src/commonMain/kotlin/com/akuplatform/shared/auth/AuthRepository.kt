package com.akuplatform.shared.auth

import com.akuplatform.shared.auth.model.AuthToken
import kotlinx.coroutines.flow.StateFlow

class AuthRepository(private val sessionManager: SessionManager) {

    val isLoggedIn: StateFlow<Boolean> = sessionManager.isLoggedIn

    suspend fun login(email: String, password: String): Result<AuthToken> {
        // TODO: wire up Wave3ApiClient for actual authentication
        return Result.failure(NotImplementedError("Login not yet implemented"))
    }

    suspend fun logout() {
        sessionManager.clearSession()
    }

    suspend fun getCurrentToken(): AuthToken? = sessionManager.getToken()
}
