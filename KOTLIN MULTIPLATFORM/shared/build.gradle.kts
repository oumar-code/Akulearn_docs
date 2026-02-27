plugins {
    kotlin("multiplatform") version "1.9.10"
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
plugins {
    id("org.jetbrains.kotlin.multiplatform") version "2.1.0"
    id("com.android.library") version "8.5.2"
    id("org.jetbrains.kotlin.plugin.serialization") version "2.1.0"
}

repositories {
    google()
    mavenCentral()
}

kotlin {
    androidTarget {
        compilations.all {
            kotlinOptions {
                jvmTarget = "17"
            }
        }
    }

    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        val commonMain by getting {
            dependencies {
                // Ktor
                implementation("io.ktor:ktor-client-core:2.3.12")
                implementation("io.ktor:ktor-client-auth:2.3.12")
                implementation("io.ktor:ktor-client-content-negotiation:2.3.12")
                implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.12")
                implementation("io.ktor:ktor-client-logging:2.3.12")

                // Supabase (KMP)
                implementation("io.github.jan-tennert.supabase:gotrue-kt:2.5.4")
                implementation("io.github.jan-tennert.supabase:postgrest-kt:2.5.4")

                // Kotlinx
                implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.1")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.1")
                implementation("org.jetbrains.kotlinx:kotlinx-datetime:0.6.1")
            }
        }
        val androidMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-cio:2.3.12")
            }
        }
        val iosMain by getting {
            dependencies {
                implementation("io.ktor:ktor-client-darwin:2.3.12")
            }
        }
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
            }
        }
    }
}

android {
    namespace = "com.akuplatform.shared"
    compileSdk = 35

    defaultConfig {
        minSdk = 26
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
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
