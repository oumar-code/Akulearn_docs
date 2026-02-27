package com.akuplatform.shared.api

import com.akuplatform.shared.auth.SessionManager
import io.ktor.client.HttpClient
import io.ktor.client.plugins.auth.Auth
import io.ktor.client.plugins.auth.providers.BearerTokens
import io.ktor.client.plugins.auth.providers.bearer
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.logging.LogLevel
import io.ktor.client.plugins.logging.Logging
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

fun buildWave3Client(sessionManager: SessionManager): HttpClient = HttpClient {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
            isLenient = true
        })
    }

    install(Auth) {
        bearer {
            loadTokens {
                val token = sessionManager.getWave3Token() ?: return@loadTokens null
                BearerTokens(accessToken = token, refreshToken = "")
            }
        }
    }

    install(Logging) {
        level = LogLevel.HEADERS
    }
}
