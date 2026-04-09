/**
 * Apollo GraphQL Usage Examples
 * Demonstrates how to use Apollo Client with Wave 3 GraphQL API
 */

import React from 'react';
import { useQuery, useMutation, useSubscription } from '@apollo/client';
import {
  GET_LESSON,
  GET_STUDENT_PROGRESS,
  GET_RECOMMENDATIONS,
  GET_LEADERBOARD,
  RECORD_QUIZ_RESULT,
  SUBSCRIBE_TO_PROGRESS_UPDATES,
} from './graphqlQueries';

// ============================================================================
// Example 1: Fetch Lesson Details
// ============================================================================

export function LessonDetailExample({ lessonId }) {
  const { loading, error, data, refetch } = useQuery(GET_LESSON, {
    variables: { lessonId },
    // Optional: skip if no lessonId
    skip: !lessonId,
  });

  if (loading) return <div>Loading lesson...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const lesson = data?.lesson;

  return (
    <div>
      <h1>{lesson.title}</h1>
      <p><strong>Subject:</strong> {lesson.subject}</p>
      <p><strong>Difficulty:</strong> {lesson.difficultyLevel}</p>
      <p><strong>Duration:</strong> {lesson.durationMinutes} minutes</p>
      
      <h2>Learning Objectives</h2>
      <ul>
        {lesson.learningObjectives.map((obj, i) => (
          <li key={i}>{obj}</li>
        ))}
      </ul>

      <h2>Content Sections</h2>
      {lesson.contentSections.map((section, i) => (
        <div key={i}>
          <h3>{section.title}</h3>
          <p>{section.content}</p>
        </div>
      ))}

      <button onClick={() => refetch()}>Refresh</button>
    </div>
  );
}

// ============================================================================
// Example 2: Student Progress Dashboard
// ============================================================================

export function ProgressDashboardExample({ studentId }) {
  const { loading, error, data } = useQuery(GET_STUDENT_PROGRESS, {
    variables: { studentId },
    // Poll every 30 seconds for updates
    pollInterval: 30000,
  });

  if (loading) return <div>Loading progress...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const progress = data?.studentProgress;

  return (
    <div className="progress-dashboard">
      <h2>Your Progress</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>{progress.lessonsCompleted}</h3>
          <p>Lessons Completed</p>
        </div>
        <div className="stat-card">
          <h3>{Math.round(progress.averageMastery)}%</h3>
          <p>Average Mastery</p>
        </div>
        <div className="stat-card">
          <h3>{progress.totalPoints}</h3>
          <p>Total Points</p>
        </div>
        <div className="stat-card">
          <h3>Level {progress.currentLevel}</h3>
          <p>Current Level</p>
        </div>
      </div>

      <h3>Recent Activities</h3>
      <ul>
        {progress.recentActivities.map((activity, i) => (
          <li key={i}>
            {activity.lessonTitle} - {activity.activityType} ({activity.duration}s ago)
          </li>
        ))}
      </ul>

      <h3>Mastery by Subject</h3>
      {progress.masteryBySubject.map((subject, i) => (
        <div key={i} className="subject-mastery">
          <h4>{subject.subject}</h4>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${(subject.lessonsCompleted / subject.totalLessons) * 100}%` }}
            />
          </div>
          <p>{subject.lessonsCompleted} / {subject.totalLessons} lessons</p>
        </div>
      ))}
    </div>
  );
}

// ============================================================================
// Example 3: Recommendations with Apollo
// ============================================================================

export function RecommendationsExample({ studentId }) {
  const [method, setMethod] = React.useState('hybrid');
  
  const { loading, error, data } = useQuery(GET_RECOMMENDATIONS, {
    variables: { 
      studentId, 
      method,
      limit: 5 
    },
  });

  if (loading) return <div>Loading recommendations...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const recommendations = data?.recommendations || [];

  return (
    <div>
      <h2>Recommended for You</h2>
      
      <div className="method-selector">
        <button 
          className={method === 'content' ? 'active' : ''}
          onClick={() => setMethod('content')}
        >
          Content-Based
        </button>
        <button 
          className={method === 'collaborative' ? 'active' : ''}
          onClick={() => setMethod('collaborative')}
        >
          Collaborative
        </button>
        <button 
          className={method === 'hybrid' ? 'active' : ''}
          onClick={() => setMethod('hybrid')}
        >
          Hybrid
        </button>
      </div>

      <div className="recommendations-list">
        {recommendations.map((rec, i) => (
          <div key={i} className="recommendation-card">
            <h3>#{i + 1} {rec.title}</h3>
            <p>{rec.subject} - {rec.difficultyLevel}</p>
            <p>{rec.description}</p>
            <div className="score">
              Match: {Math.round(rec.score * 100)}%
            </div>
            {rec.reason && <p className="reason">💡 {rec.reason}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}

// ============================================================================
// Example 4: Leaderboard with Real-time Updates
// ============================================================================

export function LeaderboardExample() {
  const { loading, error, data } = useQuery(GET_LEADERBOARD, {
    variables: { 
      scope: 'global',
      timeframe: 'weekly',
      limit: 10 
    },
    pollInterval: 10000, // Update every 10 seconds
  });

  if (loading) return <div>Loading leaderboard...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const leaderboard = data?.leaderboard || [];

  return (
    <div className="leaderboard">
      <h2>🏆 Top Students This Week</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Student</th>
            <th>Points</th>
            <th>Level</th>
            <th>Streak</th>
            <th>Achievements</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry) => (
            <tr key={entry.studentId}>
              <td className="rank">#{entry.rank}</td>
              <td>{entry.studentName}</td>
              <td>{entry.points}</td>
              <td>Level {entry.level}</td>
              <td>{entry.streak}🔥</td>
              <td>{entry.achievements}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ============================================================================
// Example 5: Submit Quiz with Mutation
// ============================================================================

export function QuizSubmissionExample({ studentId, lessonId }) {
  const [recordQuizResult, { data, loading, error }] = useMutation(
    RECORD_QUIZ_RESULT,
    {
      // Refetch queries after mutation
      refetchQueries: [
        { query: GET_STUDENT_PROGRESS, variables: { studentId } },
      ],
      // Optimistic UI update
      optimisticResponse: {
        recordQuizResult: {
          success: true,
          masteryLevel: 'Developing',
          pointsEarned: 0,
          newAchievements: [],
          __typename: 'QuizResult',
        },
      },
    }
  );

  const handleSubmit = async (answers) => {
    try {
      const result = await recordQuizResult({
        variables: {
          studentId,
          lessonId,
          score: answers.filter(a => a.correct).length,
          maxScore: answers.length,
          timeSpent: 300, // 5 minutes
          answers: answers.map(a => ({
            questionId: a.questionId,
            answer: a.answer,
            correct: a.correct,
          })),
        },
      });

      if (result.data.recordQuizResult.success) {
        alert('Quiz submitted successfully!');
        
        if (result.data.recordQuizResult.newAchievements.length > 0) {
          const achievements = result.data.recordQuizResult.newAchievements;
          alert(`🎉 New Achievements: ${achievements.map(a => a.name).join(', ')}`);
        }
      }
    } catch (err) {
      console.error('Quiz submission error:', err);
    }
  };

  return (
    <div>
      <button 
        onClick={() => handleSubmit(/* quiz answers */)} 
        disabled={loading}
      >
        {loading ? 'Submitting...' : 'Submit Quiz'}
      </button>
      
      {error && <div className="error">Error: {error.message}</div>}
      
      {data?.recordQuizResult && (
        <div className="results">
          <h3>Results</h3>
          <p>Mastery Level: {data.recordQuizResult.masteryLevel}</p>
          <p>Points Earned: +{data.recordQuizResult.pointsEarned}</p>
        </div>
      )}
    </div>
  );
}

// ============================================================================
// Example 6: Real-time Subscription
// ============================================================================

export function ProgressSubscriptionExample({ studentId }) {
  const { data, loading } = useSubscription(SUBSCRIBE_TO_PROGRESS_UPDATES, {
    variables: { studentId },
  });

  React.useEffect(() => {
    if (data?.progressUpdate) {
      const update = data.progressUpdate;
      
      // Show notification for achievement
      if (update.achievementUnlocked) {
        showNotification(
          '🎉 Achievement Unlocked!',
          update.achievementUnlocked.name
        );
      }
      
      // Show mastery update
      if (update.masteryLevel) {
        showNotification(
          'Mastery Updated',
          `New level: ${update.masteryLevel}`
        );
      }
    }
  }, [data]);

  if (loading) return <div>Connecting to real-time updates...</div>;

  return (
    <div>
      <p>✅ Real-time updates active</p>
      {data?.progressUpdate && (
        <div className="live-update">
          <p>Latest update: {data.progressUpdate.lessonId}</p>
          <p>Points: +{data.progressUpdate.pointsEarned}</p>
        </div>
      )}
    </div>
  );
}

// Helper function
function showNotification(title, message) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body: message });
  }
}

export default {
  LessonDetailExample,
  ProgressDashboardExample,
  RecommendationsExample,
  LeaderboardExample,
  QuizSubmissionExample,
  ProgressSubscriptionExample,
};
