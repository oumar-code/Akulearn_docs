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

dependencies {
    implementation(project(":shared"))
    implementation("androidx.compose.ui:ui:1.5.0")
    implementation("androidx.compose.material:material:1.5.0")
    implementation("androidx.compose.ui:ui-tooling:1.5.0")
    implementation("androidx.activity:activity-compose:1.7.2")
}
