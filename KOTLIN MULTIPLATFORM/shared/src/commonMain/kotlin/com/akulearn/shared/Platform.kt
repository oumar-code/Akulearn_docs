package com.akulearn.shared

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform
