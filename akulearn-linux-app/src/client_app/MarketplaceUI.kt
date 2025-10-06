import androidx.compose.desktop.Window
import androidx.compose.runtime.*
import androidx.compose.material.*

// Marketplace UI for buying/selling content
fun main() = Window(title = "Akulearn Marketplace") {
    MaterialTheme {
        Column {
            Text("Akulearn Marketplace")
            Button(onClick = { /* Browse e-books */ }) { Text("E-Books") }
            Button(onClick = { /* Browse AR Assets */ }) { Text("AR Assets") }
            Button(onClick = { /* Browse Datasets */ }) { Text("Datasets") }
            Button(onClick = { /* Browse Code Snippets */ }) { Text("Code Snippets") }
            Button(onClick = { /* Sell Content */ }) { Text("Sell Content") }
        }
    }
}
