package com.akuplatform.shared.auth

import com.akuplatform.shared.auth.model.AkuSession
import com.akuplatform.shared.auth.model.SupabaseSession
import com.akuplatform.shared.auth.model.Wave3TokenResponse
import io.github.jan.supabase.SupabaseClient
import io.github.jan.supabase.gotrue.auth
import io.github.jan.supabase.gotrue.providers.builtin.Email
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.http.ContentType
import io.ktor.http.contentType
import kotlinx.serialization.Serializable

@Serializable
private data class Wave3TokenRequest(val supabaseToken: String)

/**
 * Handles sign-up, sign-in, sign-out, and dual-token exchange (Supabase + Wave3).
 */
class AuthRepository(
    private val supabaseClient: SupabaseClient,
    private val wave3HttpClient: HttpClient,
    private val sessionManager: SessionManager,
    private val wave3AuthEndpoint: String
) {

    suspend fun signIn(email: String, password: String): Result<AkuSession> = runCatching {
        supabaseClient.auth.signInWith(Email) {
            this.email = email
            this.password = password
        }

        val current = supabaseClient.auth.currentSessionOrNull()
            ?: error("No Supabase session returned after sign-in")

        val supabaseSession = SupabaseSession(
            accessToken = current.accessToken,
            refreshToken = current.refreshToken,
            userId = current.user?.id ?: ""
        )

        val wave3Response: Wave3TokenResponse = wave3HttpClient.post(wave3AuthEndpoint) {
            contentType(ContentType.Application.Json)
            setBody(Wave3TokenRequest(supabaseToken = supabaseSession.accessToken))
        }.body()

        val akuSession = AkuSession(
            supabaseSession = supabaseSession,
            wave3Token = wave3Response.token
        )

        sessionManager.setSession(akuSession)
        akuSession
    }

    suspend fun signUp(email: String, password: String): Result<AkuSession> = runCatching {
        supabaseClient.auth.signUpWith(Email) {
            this.email = email
            this.password = password
        }
        signIn(email, password).getOrThrow()
    }

    suspend fun signOut() {
        runCatching { supabaseClient.auth.signOut() }
        sessionManager.clearSession()
    }
}
