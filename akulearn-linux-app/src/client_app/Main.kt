
import androidx.compose.desktop.Window
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import java.net.HttpURLConnection
import java.net.URL

// Offline cache
val offlineCache = mutableMapOf<String, List<String>>()


fun main() = Window(title = "Akulearn Classroom Client") {
    var textbooks by remember { mutableStateOf(listOf<String>()) }
    var modules by remember { mutableStateOf(listOf<String>()) }
    var quizzes by remember { mutableStateOf(listOf<String>()) }
    var videos by remember { mutableStateOf(listOf<String>()) }
    var arAssets by remember { mutableStateOf(listOf<String>()) }
    var games by remember { mutableStateOf(listOf<String>()) }
    var flashcards by remember { mutableStateOf(listOf<String>()) }
    var localized by remember { mutableStateOf(listOf<String>()) }
    var encyclopedia by remember { mutableStateOf(listOf<String>()) }
    var tools by remember { mutableStateOf(listOf<String>()) }
    var syncStatus by remember { mutableStateOf("Idle") }

    MaterialTheme {
        Column(modifier = Modifier.fillMaxSize().padding(32.dp)) {
            Text("Akulearn Classroom Client", style = MaterialTheme.typography.h4)
            Button(onClick = {
                syncStatus = "Syncing..."
                textbooks = fetchFromApiOrCache("textbooks", "http://hub.local:8000/content_service/textbooks/list")
                modules = fetchFromApiOrCache("modules", "http://hub.local:8000/content_service/modules/list")
                quizzes = fetchFromApiOrCache("quizzes", "http://hub.local:8000/content_service/quizzes/list")
                videos = fetchFromApiOrCache("videos", "http://hub.local:8000/content_service/videos/list")
                arAssets = fetchFromApiOrCache("ar_assets", "http://hub.local:8000/content_service/ar_assets/list")
                games = fetchFromApiOrCache("games", "http://hub.local:8000/content_service/games/list")
                flashcards = fetchFromApiOrCache("flashcards", "http://hub.local:8000/content_service/flashcards/list")
                localized = fetchFromApiOrCache("localized", "http://hub.local:8000/content_service/localized/list")
                encyclopedia = fetchFromApiOrCache("encyclopedia", "http://hub.local:8000/content_service/encyclopedia/list")
                tools = fetchFromApiOrCache("tools", "http://hub.local:8000/content_service/tools/list")
                syncStatus = "Synced"
            }, modifier = Modifier.height(60.dp).fillMaxWidth()) {
                Text("Sync All Content", fontSize = MaterialTheme.typography.h6.fontSize)
            }
            Text("Status: $syncStatus", modifier = Modifier.padding(vertical = 8.dp))
            Divider()
            Text("Textbooks:", style = MaterialTheme.typography.h6)
            textbooks.forEach { Text(it) }
            Divider()
            Text("Modules:", style = MaterialTheme.typography.h6)
            modules.forEach { Text(it) }
            Divider()
            Text("Quizzes:", style = MaterialTheme.typography.h6)
            quizzes.forEach { quiz ->
                Row {
                    Text(quiz)
                    Button(onClick = { launchHtmlContent("quizzes/$quiz") }) { Text("Launch Quiz") }
                }
            }
            Divider()
            Text("Videos:", style = MaterialTheme.typography.h6)
            videos.forEach { video ->
                Row {
                    Text(video)
                    Button(onClick = { launchVideoPlayer("videos/$video") }) { Text("Play Video") }
                }
            }
            Divider()
            Text("AR Assets:", style = MaterialTheme.typography.h6)
            arAssets.forEach { asset ->
                Row {
                    Text(asset)
                    Button(onClick = { launchARViewer("ar_assets/$asset") }) { Text("View AR") }
                }
            }
            Divider()
            Text("Games:", style = MaterialTheme.typography.h6)
            games.forEach { game ->
                Row {
                    Text(game)
                    Button(onClick = { launchHtmlContent("games/$game") }) { Text("Play Game") }
                }
            }
            Divider()
            Text("Flashcards:", style = MaterialTheme.typography.h6)
            flashcards.forEach { Text(it) }
            Divider()
            Text("Localized Content:", style = MaterialTheme.typography.h6)
            localized.forEach { Text(it) }
            Divider()
            Text("Encyclopedia:", style = MaterialTheme.typography.h6)
            encyclopedia.forEach { Text(it) }
            Divider()
            Text("Tools:", style = MaterialTheme.typography.h6)
            tools.forEach { tool ->
                Row {
                    Text(tool)
                    Button(onClick = { launchHtmlContent("tools/$tool") }) { Text("Open Tool") }
                }
            }
        }
    }
}

// Automation: Launchers for interactive content
fun launchHtmlContent(path: String) {
    // TODO: Open HTML content in embedded browser or external browser
}

fun launchVideoPlayer(path: String) {
    // TODO: Open video file in embedded or external player
}

fun launchARViewer(path: String) {
    // TODO: Open AR/3D model viewer for .glb/.obj/.fbx files
}

fun fetchFromApiOrCache(key: String, apiUrl: String): List<String> {
    return try {
        val result = fetchListFromApi(apiUrl)
        offlineCache[key] = result
        result
    } catch (e: Exception) {
        // Fallback to offline cache
        offlineCache[key] ?: listOf("No cached data available.")
    }
}

fun fetchListFromApi(apiUrl: String): List<String> {
    val url = URL(apiUrl)
    val conn = url.openConnection() as HttpURLConnection
    conn.requestMethod = "GET"
    conn.connectTimeout = 2000
    conn.readTimeout = 2000
    return if (conn.responseCode == 200) {
        conn.inputStream.bufferedReader().readLines()
    } else {
        listOf("API error: ${conn.responseCode}")
    }
}
