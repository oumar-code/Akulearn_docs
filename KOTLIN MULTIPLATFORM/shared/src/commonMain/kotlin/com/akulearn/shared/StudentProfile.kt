package com.akulearn.shared

import kotlinx.serialization.Serializable

@Serializable
data class StudentProfile(
    val id: String,
    val name: String,
    val progress: Progress,
    val quizResults: List<QuizResult>,
    val chatHistory: List<ChatMessage>
)

@Serializable
data class Progress(
    val completedTopics: List<String>,
    val lastAccessed: String
)

@Serializable
data class QuizResult(
    val topicId: String,
    val score: Int,
    val timestamp: String
)

@Serializable
data class ChatMessage(
    val sender: String,
    val message: String,
    val timestamp: String
)
