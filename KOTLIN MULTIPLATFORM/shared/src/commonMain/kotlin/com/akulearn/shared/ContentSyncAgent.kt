package com.akulearn.shared

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.coroutines.*
import kotlinx.serialization.json.Json
import java.util.zip.Deflater

class ContentSyncAgent(private val client: HttpClient) {
    suspend fun syncIfConnected(localData: ByteArray, syncUrl: String): Boolean {
        return if (isConnectedToInternet()) {
            val compressedData = compressData(localData)
            try {
                val response: HttpResponse = client.post(syncUrl) {
                    setBody(compressedData)
                }
                response.status.value in 200..299
            } catch (e: Exception) {
                false
            }
        } else {
            false
        }
    }

    private fun isConnectedToInternet(): Boolean {
        // Placeholder: Replace with actual network check per platform
        return true
    }

    private fun compressData(data: ByteArray): ByteArray {
        val deflater = Deflater()
        deflater.setInput(data)
        deflater.finish()
        val output = ByteArray(data.size)
        val compressedSize = deflater.deflate(output)
        return output.copyOf(compressedSize)
    }
}
