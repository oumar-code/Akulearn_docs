plugins {
    kotlin("multiplatform")
    id("com.android.library")
}

kotlin {
    android()
    ios()
    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
                implementation("com.squareup.sqldelight:runtime:2.0.0") // SQLite
                implementation("io.ktor:ktor-client-core:2.3.4") // Networking
                implementation("io.ktor:ktor-client-serialization:2.3.4")
                implementation("io.ktor:ktor-client-logging:2.3.4")
                implementation("io.ktor:ktor-client-content-negotiation:2.3.4")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
            }
        }
        val androidMain by getting {
            dependencies {
                implementation("com.squareup.sqldelight:android-driver:2.0.0")
                implementation("io.ktor:ktor-client-okhttp:2.3.4")
            }
        }
        val iosMain by getting {
            dependencies {
                implementation("com.squareup.sqldelight:native-driver:2.0.0")
                implementation("io.ktor:ktor-client-darwin:2.3.4")
            }
        }
    }
}

android {
    namespace = "com.akulearn.shared"
    compileSdk = 33
    defaultConfig {
        minSdk = 24
        targetSdk = 33
    }
}
