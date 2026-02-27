package com.akuplatform.shared.auth.model

import kotlinx.serialization.Serializable

data class SupabaseSession(
    val accessToken: String,
    val refreshToken: String,
    val userId: String
)

@Serializable
data class Wave3TokenResponse(
    val token: String,
    val expiresIn: Long
)

data class AkuSession(
    val supabaseSession: SupabaseSession,
    val wave3Token: String
)
