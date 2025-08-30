plugins {
    id("org.jetbrains.kotlin.native.cocoapods")
}

kotlin {
    ios()
    cocoapods {
        summary = "Akulearn iOS App"
        homepage = "https://akulearn.com"
        ios.deploymentTarget = "14.1"
        podfile = project.file("../iosApp/Podfile")
        framework {
            baseName = "shared"
        }
    }
}
