import androidx.compose.desktop.Window
import androidx.compose.runtime.*
import androidx.compose.material.*

// Centralized repository browser UI
fun main() = Window(title = "Akulearn Repository Browser") {
    MaterialTheme {
        Column {
            Text("Akulearn Repository Browser")
            Text("Browse e-books, journals, AR assets, datasets, and code.")
            Button(onClick = { /* List textbooks */ }) { Text("Textbooks") }
            Button(onClick = { /* List journals */ }) { Text("Journals") }
            Button(onClick = { /* List AR Assets */ }) { Text("AR Assets") }
            Button(onClick = { /* List Datasets */ }) { Text("Datasets") }
            Button(onClick = { /* List Code Snippets */ }) { Text("Code Snippets") }
        }
    }
}
