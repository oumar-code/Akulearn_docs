plugins {
    kotlin("multiplatform") version "1.9.10"
    id("org.jetbrains.compose") version "1.5.0"
}

kotlin {
    linuxX64("linux") {
        binaries {
            executable {
                entryPoint = "MainKt"
            }
        }
    }
    sourceSets {
        val linuxMain by getting {
            dependencies {
                implementation("org.jetbrains.compose.ui:ui:1.5.0")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
            }
        }
    }
}

group = "com.akulearn"
version = "1.0.0"
