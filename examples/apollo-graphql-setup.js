/**
 * Apollo GraphQL Setup for Wave 3
 * Complete configuration and example queries
 * 
 * Installation:
 *   npm install @apollo/client graphql
 */

import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery, useLazyQuery } from '@apollo/client';
import React from 'react';

// ============================================================================
// Apollo Client Configuration
// ============================================================================

const createApolloClient = (authToken = null) => {
  return new ApolloClient({
    uri: 'http://localhost:8000/graphql',
    cache: new InMemoryCache(),
    headers: {
      ...(authToken && { authorization: `Bearer ${authToken}` })
    },
    defaultOptions: {
      watchQuery: {
        fetchPolicy: 'cache-and-network',
        errorPolicy: 'all',
      },
      query: {
        fetchPolicy: 'network-only',
        errorPolicy: 'all',
      },
    },
  });
};

// ============================================================================
// GraphQL Queries
// ============================================================================

// Get Single Lesson
export const GET_LESSON = gql`
  query GetLesson($lessonId: String!) {
    lesson(lessonId: $lessonId) {
      id
      title
      subject
      description
      durationMinutes
      difficultyLevel
      learningObjectives
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
        title
        url
        type
      }
      nerdcCodes
      waecTopics
      keywords
    }
  }
`;

// Get Student Progress
export const GET_STUDENT_PROGRESS = gql`
  query GetStudentProgress($studentId: String!) {
    studentProgress(studentId: $studentId) {
      studentId
      lessonsCompleted
      totalLessons
      averageMastery
      completionRate
      recentActivities {
        lessonId
        activityType
        timestamp
        durationSeconds
      }
    }
  }
`;

// Get Recommendations
export const GET_RECOMMENDATIONS = gql`
  query GetRecommendations($studentId: String!, $method: String, $limit: Int) {
    recommendations(studentId: $studentId, method: $method, limit: $limit) {
      lessonId
      score
      reason
      lesson {
        id
        title
        subject
        description
        difficultyLevel
        durationMinutes
      }
    }
  }
`;

// Search Lessons
export const SEARCH_LESSONS = gql`
  query SearchLessons($searchTerm: String!, $subject: String, $difficultyLevel: String) {
    searchLessons(searchTerm: $searchTerm, subject: $subject, difficultyLevel: $difficultyLevel) {
      id
      title
      subject
      description
      difficultyLevel
      durationMinutes
      nerdcCodes
      waecTopics
    }
  }
`;

// Get Leaderboard
export const GET_LEADERBOARD = gql`
  query GetLeaderboard($scope: String, $limit: Int) {
    leaderboard(scope: $scope, limit: $limit) {
      rank
      studentId
      studentName
      points
      level
      streak
      achievementCount
    }
  }
`;

// Get Student Achievements
export const GET_ACHIEVEMENTS = gql`
  query GetAchievements($studentId: String!) {
    achievements(studentId: $studentId) {
      id
      name
      description
      category
      icon
      badgeLevel
      pointsRequired
      unlockedAt
      progress {
        current
        required
        percentage
      }
    }
  }
`;

// ============================================================================
// React Hooks Examples
// ============================================================================

/**
 * Hook for fetching lesson details
 */
export const useLessonQuery = (lessonId) => {
  const { loading, error, data, refetch } = useQuery(GET_LESSON, {
    variables: { lessonId },
    skip: !lessonId,
  });

  return {
    lesson: data?.lesson,
    loading,
    error,
    refetch,
  };
};

/**
 * Hook for fetching student progress
 */
export const useStudentProgress = (studentId) => {
  const { loading, error, data, refetch } = useQuery(GET_STUDENT_PROGRESS, {
    variables: { studentId },
    skip: !studentId,
    pollInterval: 30000, // Refresh every 30 seconds
  });

  return {
    progress: data?.studentProgress,
    loading,
    error,
    refetch,
  };
};

/**
 * Hook for fetching recommendations
 */
export const useRecommendations = (studentId, method = 'hybrid', limit = 5) => {
  const { loading, error, data, refetch } = useQuery(GET_RECOMMENDATIONS, {
    variables: { studentId, method, limit },
    skip: !studentId,
  });

  return {
    recommendations: data?.recommendations || [],
    loading,
    error,
    refetch,
  };
};

/**
 * Hook for searching lessons (lazy query)
 */
export const useSearchLessons = () => {
  const [searchLessons, { loading, error, data }] = useLazyQuery(SEARCH_LESSONS);

  const search = (searchTerm, subject = null, difficultyLevel = null) => {
    searchLessons({ variables: { searchTerm, subject, difficultyLevel } });
  };

  return {
    search,
    lessons: data?.searchLessons || [],
    loading,
    error,
  };
};

// ============================================================================
// React Components Examples
// ============================================================================

/**
 * Lesson Detail Component
 */
export const LessonDetailComponent = ({ lessonId }) => {
  const { lesson, loading, error } = useLessonQuery(lessonId);

  if (loading) return <div>Loading lesson...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!lesson) return <div>Lesson not found</div>;

  return (
    <div className="lesson-detail">
      <h1>{lesson.title}</h1>
      <div className="meta">
        <span>{lesson.subject}</span>
        <span>{lesson.difficultyLevel}</span>
        <span>{lesson.durationMinutes} min</span>
      </div>
      
      <section>
        <h2>Description</h2>
        <p>{lesson.description}</p>
      </section>

      <section>
        <h2>Learning Objectives</h2>
        <ul>
          {lesson.learningObjectives.map((obj, i) => (
            <li key={i}>{obj}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Content</h2>
        {lesson.contentSections.map((section, i) => (
          <div key={i}>
            <h3>{section.title}</h3>
            <p>{section.content}</p>
          </div>
        ))}
      </section>

      <section>
        <h2>Worked Examples</h2>
        {lesson.workedExamples.map((example, i) => (
          <div key={i} className="example">
            <h4>Example {i + 1}</h4>
            <p><strong>Problem:</strong> {example.problem}</p>
            <p><strong>Solution:</strong> {example.solution}</p>
            <p><strong>Explanation:</strong> {example.explanation}</p>
          </div>
        ))}
      </section>
    </div>
  );
};

/**
 * Student Progress Dashboard Component
 */
export const ProgressDashboardComponent = ({ studentId }) => {
  const { progress, loading, error } = useStudentProgress(studentId);

  if (loading) return <div>Loading progress...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!progress) return <div>No progress data</div>;

  return (
    <div className="progress-dashboard">
      <h2>Your Progress</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{progress.lessonsCompleted}</div>
          <div className="stat-label">Lessons Completed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{Math.round(progress.completionRate * 100)}%</div>
          <div className="stat-label">Completion Rate</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{Math.round(progress.averageMastery * 100)}%</div>
          <div className="stat-label">Average Mastery</div>
        </div>
      </div>

      <h3>Recent Activities</h3>
      <div className="activities-list">
        {progress.recentActivities.map((activity, i) => (
          <div key={i} className="activity-item">
            <span>{activity.activityType}</span>
            <span>{activity.lessonId}</span>
            <span>{new Date(activity.timestamp).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

/**
 * Leaderboard Component
 */
export const LeaderboardComponent = ({ scope = 'global', limit = 10 }) => {
  const { loading, error, data } = useQuery(GET_LEADERBOARD, {
    variables: { scope, limit },
  });

  if (loading) return <div>Loading leaderboard...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const leaderboard = data?.leaderboard || [];

  return (
    <div className="leaderboard">
      <h2>🏆 Leaderboard</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Points</th>
            <th>Level</th>
            <th>Streak</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((entry) => (
            <tr key={entry.studentId}>
              <td>#{entry.rank}</td>
              <td>{entry.studentName}</td>
              <td>{entry.points}</td>
              <td>{entry.level}</td>
              <td>🔥 {entry.streak}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

/**
 * Search Component
 */
export const SearchComponent = () => {
  const { search, lessons, loading } = useSearchLessons();
  const [searchTerm, setSearchTerm] = React.useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      search(searchTerm);
    }
  };

  return (
    <div className="search-component">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search lessons..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      {loading && <div>Searching...</div>}

      <div className="search-results">
        {lessons.map((lesson) => (
          <div key={lesson.id} className="lesson-card">
            <h3>{lesson.title}</h3>
            <p>{lesson.description}</p>
            <div className="meta">
              {lesson.subject} • {lesson.difficultyLevel} • {lesson.durationMinutes} min
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// ============================================================================
// App Setup
// ============================================================================

/**
 * Main App with Apollo Provider
 */
export const App = ({ authToken, children }) => {
  const client = createApolloClient(authToken);

  return (
    <ApolloProvider client={client}>
      {children}
    </ApolloProvider>
  );
};

// Export configured client
export { createApolloClient };
export default createApolloClient;

// ============================================================================
// Usage Example
// ============================================================================

/*
import React from 'react';
import ReactDOM from 'react-dom';
import { App, LessonDetailComponent, ProgressDashboardComponent } from './apollo-graphql-setup';

const authToken = 'your-jwt-token-here';

ReactDOM.render(
  <App authToken={authToken}>
    <div className="app">
      <LessonDetailComponent lessonId="lesson_123" />
      <ProgressDashboardComponent studentId="student_001" />
    </div>
  </App>,
  document.getElementById('root')
);
*/
