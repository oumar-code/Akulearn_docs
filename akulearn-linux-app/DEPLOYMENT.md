# Akulearn Linux App Deployment Guide

## Prerequisites
- Ubuntu 22.04+ or compatible Linux distribution
- JDK 17+
- Kotlin Multiplatform and Compose dependencies

## Build Instructions
1. Install JDK:
   ```sh
   sudo apt update
   sudo apt install openjdk-25-jdk
   ```
2. Install Kotlin and Gradle (if not present):
   ```sh
   curl -s https://get.sdkman.io | bash
   sdk install kotlin
   sdk install gradle
   ```
3. Clone the repository:
   ```sh
   git clone https://github.com/oumar-code/Akulearn_docs.git
   cd Akulearn_docs/akulearn-linux-app
   ```
4. Build the app:
   ```sh
   ./gradlew build
   ```
5. Run the app:
   ```sh
   ./build/bin/linuxX64/releaseExecutable/akulearn-linux-app.kexe
   ```

## Systemd Service (Optional)
To run the app on boot:
1. Create a systemd unit file `/etc/systemd/system/akulearn-linux-app.service`:
   ```ini
   [Unit]
   Description=Akulearn Smart Board/TV App
   After=network.target

   [Service]
   ExecStart=/path/to/akulearn-linux-app.kexe
   Restart=always
   User=akulearn

   [Install]
   WantedBy=multi-user.target
   ```
2. Enable and start:
   ```sh
   sudo systemctl enable akulearn-linux-app
   sudo systemctl start akulearn-linux-app
   ```

## Touchscreen Support
- Most modern Linux distributions support touchscreens out of the box.
- For advanced gestures, install and configure `libinput`.

---
Your Akulearn Linux app is now ready for deployment on smart boards and TVs!
