package com.akuplatform.shared.api

import com.akuplatform.shared.auth.model.AuthToken

class Wave3ApiClient(private val baseUrl: String = BASE_URL) {

    companion object {
        const val BASE_URL = "https://api.akulearn.com/v3"
    }

    suspend fun authenticate(email: String, password: String): Result<AuthToken> {
        // TODO: implement HTTP authentication call
        return Result.failure(NotImplementedError("HTTP client not yet configured"))
    }

    suspend fun refreshToken(refreshToken: String): Result<AuthToken> {
        // TODO: implement token refresh call
        return Result.failure(NotImplementedError("HTTP client not yet configured"))
    }
}
