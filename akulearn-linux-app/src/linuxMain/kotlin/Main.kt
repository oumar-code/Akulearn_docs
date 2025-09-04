import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.material.*
import androidx.compose.runtime.*

fun main() = application {
    Window(onCloseRequest = ::exitApplication, title = "Akulearn Smart Board/TV") {
        var selectedScreen by remember { mutableStateOf("dashboard") }
        Scaffold(
            topBar = {
                TopAppBar(title = { Text("Akulearn Facilitator Dashboard") })
            },
            content = {
                when (selectedScreen) {
                    "dashboard" -> FacilitatorDashboard(onNavigate = { selectedScreen = it })
                    "quiz" -> QuizScreen(onBack = { selectedScreen = "dashboard" })
                }
            }
        )
    }
}

@Composable
fun FacilitatorDashboard(onNavigate: (String) -> Unit) {
    Column {
        Text("Welcome, Teacher!", style = MaterialTheme.typography.h4)
        Button(onClick = { onNavigate("quiz") }, modifier = Modifier.padding(16.dp)) {
            Text("Start Quiz")
        }
    }
}

@Composable
fun QuizScreen(onBack: () -> Unit) {
    Column {
        Text("Quiz", style = MaterialTheme.typography.h4)
        // Example question
        Text("What is 2 + 2?", style = MaterialTheme.typography.h5)
        Row {
            Button(onClick = {}, modifier = Modifier.padding(8.dp)) { Text("3") }
            Button(onClick = {}, modifier = Modifier.padding(8.dp)) { Text("4") }
            Button(onClick = {}, modifier = Modifier.padding(8.dp)) { Text("5") }
        }
        Button(onClick = onBack, modifier = Modifier.padding(16.dp)) {
            Text("Back to Dashboard")
        }
    }
}
