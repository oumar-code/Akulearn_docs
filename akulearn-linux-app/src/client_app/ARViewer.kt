import androidx.compose.desktop.Window
import androidx.compose.runtime.*
import androidx.compose.material.*

// Placeholder for AR viewer integration
fun main() = Window(title = "Akulearn AR Viewer") {
    MaterialTheme {
        Column {
            Text("AR Viewer")
            Text("Select a 3D model to view in AR.")
            // In production, integrate with WebAR or native AR libraries
            Button(onClick = { /* Load human_heart.glb */ }) { Text("View Human Heart") }
            Button(onClick = { /* Load solar_system.glb */ }) { Text("View Solar System") }
            Button(onClick = { /* Load historical_building.glb */ }) { Text("View Historical Building") }
        }
    }
}
