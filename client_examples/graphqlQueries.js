/**
 * Wave 3 GraphQL Queries
 * Predefined queries for common operations
 */

import { gql } from '@apollo/client';

// ============================================================================
// LESSON QUERIES
// ============================================================================

export const GET_LESSON = gql`
  query GetLesson($lessonId: String!) {
    lesson(lessonId: $lessonId) {
      id
      title
      subject
      grade
      description
      difficultyLevel
      durationMinutes
      learningObjectives
      nerdcCodes
      waecTopics
      keywords
      contentSections {
        title
        content
      }
      workedExamples {
        problem
        solution
        explanation
      }
      practiceProblems {
        question
        options
        correctAnswer
        explanation
      }
      glossary {
        term
        definition
      }
      resources {
        type
        title
        url
      }
    }
  }
`;

export const SEARCH_LESSONS = gql`
  query SearchLessons($searchTerm: String!, $subject: String, $grade: String, $difficulty: String) {
    searchLessons(
      searchTerm: $searchTerm
      subject: $subject
      grade: $grade
      difficultyLevel: $difficulty
    ) {
      id
      title
      subject
      grade
      description
      difficultyLevel
      durationMinutes
      nerdcCodes
      waecTopics
    }
  }
`;

export const GET_LESSONS_BY_SUBJECT = gql`
  query GetLessonsBySubject($subject: String!, $grade: String) {
    lessonsBySubject(subject: $subject, grade: $grade) {
      id
      title
      description
      difficultyLevel
      durationMinutes
    }
  }
`;

// ============================================================================
// STUDENT PROGRESS QUERIES
// ============================================================================

export const GET_STUDENT_PROGRESS = gql`
  query GetStudentProgress($studentId: String!) {
    studentProgress(studentId: $studentId) {
      lessonsCompleted
      totalLessons
      averageMastery
      totalPoints
      currentLevel
      recentActivities {
        lessonId
        lessonTitle
        activityType
        timestamp
        duration
      }
      masteryBySubject {
        subject
        masteryLevel
        lessonsCompleted
        totalLessons
      }
    }
  }
`;

export const GET_LESSON_MASTERY = gql`
  query GetLessonMastery($studentId: String!, $lessonId: String!) {
    lessonMastery(studentId: $studentId, lessonId: $lessonId) {
      lessonId
      studentId
      masteryLevel
      masteryPercentage
      totalTimeSpent
      activitiesCompleted
      quizAverage
      problemsCorrect
      problemsAttempted
      lastAccessed
    }
  }
`;

// ============================================================================
// RECOMMENDATIONS QUERIES
// ============================================================================

export const GET_RECOMMENDATIONS = gql`
  query GetRecommendations($studentId: String!, $method: String, $limit: Int) {
    recommendations(studentId: $studentId, method: $method, limit: $limit) {
      lessonId
      title
      subject
      description
      score
      reason
      difficultyLevel
    }
  }
`;

export const GET_PREREQUISITE_RECOMMENDATIONS = gql`
  query GetPrerequisiteRecommendations($studentId: String!, $lessonId: String!) {
    prerequisiteRecommendations(studentId: $studentId, lessonId: $lessonId) {
      lessonId
      title
      subject
      reason
      priority
    }
  }
`;

// ============================================================================
// GAMIFICATION QUERIES
// ============================================================================

export const GET_STUDENT_ACHIEVEMENTS = gql`
  query GetStudentAchievements($studentId: String!) {
    studentAchievements(studentId: $studentId) {
      achievementId
      name
      description
      icon
      badgeLevel
      unlockedAt
      category
      progress
      maxProgress
    }
  }
`;

export const GET_LEADERBOARD = gql`
  query GetLeaderboard($scope: String, $timeframe: String, $limit: Int) {
    leaderboard(scope: $scope, timeframe: $timeframe, limit: $limit) {
      rank
      studentId
      studentName
      points
      level
      streak
      achievements
    }
  }
`;

export const GET_STUDENT_STATS = gql`
  query GetStudentStats($studentId: String!) {
    studentStats(studentId: $studentId) {
      points
      level
      streak
      achievementsUnlocked
      lessonsCompleted
      totalStudyTime
      rank
      percentile
    }
  }
`;

// ============================================================================
// ANALYTICS QUERIES
// ============================================================================

export const GET_LEARNING_ANALYTICS = gql`
  query GetLearningAnalytics($studentId: String!, $timeframe: String) {
    learningAnalytics(studentId: $studentId, timeframe: $timeframe) {
      averageMastery
      studyTimeHours
      lessonsCompleted
      quizScoreAverage
      improvementRate
      strongSubjects
      weakSubjects
      studyPattern {
        dayOfWeek
        hoursStudied
        performanceScore
      }
      predictedPerformance {
        subject
        predictedScore
        confidence
      }
    }
  }
`;

export const GET_AT_RISK_STATUS = gql`
  query GetAtRiskStatus($studentId: String!) {
    atRiskStatus(studentId: $studentId) {
      isAtRisk
      riskLevel
      factors
      recommendations
      interventions
    }
  }
`;

// ============================================================================
// MUTATIONS
// ============================================================================

export const RECORD_QUIZ_RESULT = gql`
  mutation RecordQuizResult(
    $studentId: String!
    $lessonId: String!
    $score: Float!
    $maxScore: Float!
    $timeSpent: Int!
    $answers: [AnswerInput!]!
  ) {
    recordQuizResult(
      studentId: $studentId
      lessonId: $lessonId
      score: $score
      maxScore: $maxScore
      timeSpent: $timeSpent
      answers: $answers
    ) {
      success
      masteryLevel
      pointsEarned
      newAchievements {
        achievementId
        name
        icon
      }
    }
  }
`;

export const RECORD_LEARNING_ACTIVITY = gql`
  mutation RecordLearningActivity(
    $studentId: String!
    $lessonId: String!
    $activityType: String!
    $duration: Int!
    $metadata: JSON
  ) {
    recordActivity(
      studentId: $studentId
      lessonId: $lessonId
      activityType: $activityType
      duration: $duration
      metadata: $metadata
    ) {
      success
      pointsEarned
    }
  }
`;

export const RECORD_INTERACTION = gql`
  mutation RecordInteraction(
    $studentId: String!
    $lessonId: String!
    $interactionType: String!
  ) {
    recordInteraction(
      studentId: $studentId
      lessonId: $lessonId
      interactionType: $interactionType
    ) {
      success
    }
  }
`;

// ============================================================================
// SUBSCRIPTIONS (if WebSocket is enabled)
// ============================================================================

export const SUBSCRIBE_TO_PROGRESS_UPDATES = gql`
  subscription OnProgressUpdate($studentId: String!) {
    progressUpdate(studentId: $studentId) {
      lessonId
      masteryLevel
      pointsEarned
      achievementUnlocked {
        achievementId
        name
        icon
      }
    }
  }
`;

export const SUBSCRIBE_TO_LEADERBOARD_UPDATES = gql`
  subscription OnLeaderboardUpdate {
    leaderboardUpdate {
      rank
      studentId
      points
      level
    }
  }
`;
