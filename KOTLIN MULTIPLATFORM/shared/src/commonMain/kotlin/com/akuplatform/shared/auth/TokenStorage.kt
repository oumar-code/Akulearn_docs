package com.akuplatform.shared.auth

import com.akuplatform.shared.auth.model.AuthToken

interface TokenStorage {
    suspend fun saveToken(token: AuthToken)
    suspend fun getToken(): AuthToken?
    suspend fun clearToken()
}
