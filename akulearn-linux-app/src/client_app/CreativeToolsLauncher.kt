import androidx.compose.desktop.Window
import androidx.compose.runtime.*
import androidx.compose.material.*
import java.awt.Desktop
import java.io.File

// Simple launcher for creative tools
fun main() = Window(title = "Akulearn Creative Tools Launcher") {
    MaterialTheme {
        Column {
            Text("Creative Tools Launcher")
            Text("Select a creative tool to launch.")
            Button(onClick = { launchTool("content/tools/digital_art_app.zip") }) { Text("Digital Art App") }
            Button(onClick = { launchTool("content/tools/music_creation_app.zip") }) { Text("Music Creation App") }
            Button(onClick = { launchTool("content/tools/coding_app.zip") }) { Text("Coding App") }
        }
    }
}

fun launchTool(path: String) {
    val file = File(path)
    if (file.exists()) {
        Desktop.getDesktop().open(file)
    }
}
