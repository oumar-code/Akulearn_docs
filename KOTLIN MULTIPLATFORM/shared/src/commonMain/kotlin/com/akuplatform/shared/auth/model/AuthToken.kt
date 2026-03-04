package com.akuplatform.shared.auth.model

data class AuthToken(
    val accessToken: String,
    val refreshToken: String,
    /** Duration in seconds until the [accessToken] expires, as returned by the server. */
    val expiresIn: Long
)
