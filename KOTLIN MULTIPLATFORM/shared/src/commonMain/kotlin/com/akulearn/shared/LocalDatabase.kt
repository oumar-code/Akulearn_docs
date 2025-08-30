package com.akulearn.shared

interface LocalDatabase {
    suspend fun saveStudentProfile(profile: StudentProfile)
    suspend fun getStudentProfile(id: String): StudentProfile?
    suspend fun saveQuizResult(profileId: String, result: QuizResult)
    suspend fun saveChatMessage(profileId: String, message: ChatMessage)
}
