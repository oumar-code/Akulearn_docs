plugins {
    id("com.android.application")
    kotlin("android")
}

android {
    namespace = "com.akulearn.androidApp"
    compileSdk = 33
    defaultConfig {
        applicationId = "com.akulearn.androidApp"
        minSdk = 24
        targetSdk = 33
        versionCode = 1
        versionName = "1.0"
    }
}
plugins {
    id("com.android.application") version "8.5.2"
    id("org.jetbrains.kotlin.android") version "2.1.0"
    id("org.jetbrains.kotlin.plugin.compose") version "2.1.0"
}

repositories {
    google()
    mavenCentral()
}

android {
    namespace = "com.akuplatform.android"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.akuplatform.android"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"

        buildConfigField("String", "SUPABASE_URL", "\"${System.getenv("SUPABASE_URL") ?: ""}\"")
        buildConfigField("String", "SUPABASE_ANON_KEY", "\"${System.getenv("SUPABASE_ANON_KEY") ?: ""}\"")
        buildConfigField("String", "WAVE3_BASE_URL", "\"${System.getenv("WAVE3_BASE_URL") ?: ""}\"")
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(project(":shared"))

    // Compose BOM and artifacts
    implementation(platform("androidx.compose:compose-bom:2024.09.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")

    // Android essentials
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.6")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.8.6")
    implementation("androidx.activity:activity-compose:1.9.2")

    // Navigation
    implementation("androidx.navigation:navigation-compose:2.8.2")

    // Secure token storage and preferences
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
    implementation("androidx.datastore:datastore-preferences:1.1.1")

    debugImplementation("androidx.compose.ui:ui-tooling")
}
dependencies {
    implementation(project(":shared"))
    implementation("androidx.compose.ui:ui:1.5.0")
    implementation("androidx.compose.material:material:1.5.0")
    implementation("androidx.compose.ui:ui-tooling:1.5.0")
    implementation("androidx.activity:activity-compose:1.7.2")
}
