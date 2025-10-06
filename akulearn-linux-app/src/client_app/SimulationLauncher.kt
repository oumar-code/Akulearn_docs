import androidx.compose.desktop.Window
import androidx.compose.runtime.*
import androidx.compose.material.*
import java.awt.Desktop
import java.io.File

// Simple launcher for classroom simulations
fun main() = Window(title = "Akulearn Simulation Launcher") {
    MaterialTheme {
        Column {
            Text("Simulation Launcher")
            Text("Select a simulation to launch on the smart board.")
            Button(onClick = { launchSimulation("content/simulations/virtual_ecosystem.html") }) { Text("Virtual Ecosystem") }
            Button(onClick = { launchSimulation("content/simulations/virtual_frog_dissection.html") }) { Text("Virtual Frog Dissection") }
        }
    }
}

fun launchSimulation(path: String) {
    val file = File(path)
    if (file.exists()) {
        Desktop.getDesktop().browse(file.toURI())
    }
}
