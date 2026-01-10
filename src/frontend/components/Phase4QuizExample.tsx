/**
 * Phase 4 Practice Quiz Example
 * Demonstrates usage of Phase 4 components
 */

import React, { useState } from 'react';
import { usePhase4Questions } from '../hooks/usePhase4Questions';
import QuizInterface, { QuizResults } from './QuizInterface';
import ResultsSummary from './ResultsSummary';

export const Phase4QuizExample: React.FC = () => {
  const [quizActive, setQuizActive] = useState(false);
  const [quizResults, setQuizResults] = useState<QuizResults | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<string>('Mathematics');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('medium');
  const [questionCount, setQuestionCount] = useState<number>(10);

  const { stats, fetchStats } = usePhase4Questions({ autoFetch: true });

  const handleStartQuiz = () => {
    setQuizActive(true);
    setQuizResults(null);
  };

  const handleQuizComplete = (results: QuizResults) => {
    setQuizActive(false);
    setQuizResults(results);
  };

  const handleQuizExit = () => {
    setQuizActive(false);
    setQuizResults(null);
  };

  const handleRestart = () => {
    setQuizResults(null);
    setQuizActive(true);
  };

  if (quizActive) {
    return (
      <QuizInterface
        quizConfig={{
          subject: selectedSubject,
          difficulty: selectedDifficulty,
          questionCount: questionCount,
          timeLimit: 15,
          showFeedback: true,
          allowReview: true
        }}
        onQuizComplete={handleQuizComplete}
        onQuizExit={handleQuizExit}
      />
    );
  }

  if (quizResults) {
    return (
      <ResultsSummary
        results={quizResults}
        onRestart={handleRestart}
        onExit={handleQuizExit}
        showDetailedReview={true}
      />
    );
  }

  return (
    <div className="phase4-quiz-example">
      <div className="quiz-setup">
        <h1>Practice Quiz</h1>
        <p className="subtitle">Test your knowledge with interactive questions</p>

        {stats && (
          <div className="stats-overview">
            <div className="stat-card">
              <div className="stat-value">{stats.total_questions}</div>
              <div className="stat-label">Total Questions</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.subjects}</div>
              <div className="stat-label">Subjects</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.total_points}</div>
              <div className="stat-label">Total Points</div>
            </div>
          </div>
        )}

        <div className="quiz-config">
          <h2>Quiz Settings</h2>
          
          <div className="form-group">
            <label>Subject</label>
            <select 
              value={selectedSubject} 
              onChange={(e) => setSelectedSubject(e.target.value)}
            >
              <option value="Mathematics">Mathematics</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Biology">Biology</option>
            </select>
          </div>

          <div className="form-group">
            <label>Difficulty</label>
            <select 
              value={selectedDifficulty} 
              onChange={(e) => setSelectedDifficulty(e.target.value)}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div className="form-group">
            <label>Number of Questions</label>
            <input 
              type="number" 
              value={questionCount} 
              onChange={(e) => setQuestionCount(parseInt(e.target.value))}
              min="5"
              max="20"
            />
          </div>

          <button className="start-button" onClick={handleStartQuiz}>
            Start Quiz
          </button>
        </div>

        <div className="info-section">
          <h3>How It Works</h3>
          <ul>
            <li>Answer all questions to complete the quiz</li>
            <li>Get instant feedback on your answers</li>
            <li>Review detailed explanations</li>
            <li>Track your progress and performance</li>
          </ul>
        </div>
      </div>

      <style jsx>{`
        .phase4-quiz-example {
          max-width: 800px;
          margin: 0 auto;
          padding: 40px 24px;
        }

        .quiz-setup {
          background: white;
          border-radius: 16px;
          padding: 40px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        h1 {
          margin: 0 0 8px 0;
          font-size: 32px;
          color: #333;
        }

        .subtitle {
          margin: 0 0 32px 0;
          font-size: 16px;
          color: #666;
        }

        .stats-overview {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 16px;
          margin-bottom: 40px;
        }

        .stat-card {
          text-align: center;
          padding: 20px;
          background: #f5f5f5;
          border-radius: 12px;
        }

        .stat-value {
          font-size: 32px;
          font-weight: 700;
          color: #2196f3;
          margin-bottom: 8px;
        }

        .stat-label {
          font-size: 12px;
          color: #999;
          text-transform: uppercase;
          font-weight: 600;
        }

        .quiz-config {
          margin-bottom: 32px;
        }

        .quiz-config h2 {
          margin: 0 0 24px 0;
          font-size: 20px;
          color: #333;
        }

        .form-group {
          margin-bottom: 20px;
        }

        .form-group label {
          display: block;
          margin-bottom: 8px;
          font-weight: 600;
          color: #333;
          font-size: 14px;
        }

        .form-group select,
        .form-group input {
          width: 100%;
          padding: 12px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 16px;
          transition: border-color 0.2s;
        }

        .form-group select:focus,
        .form-group input:focus {
          outline: none;
          border-color: #2196f3;
        }

        .start-button {
          width: 100%;
          padding: 16px;
          background: #2196f3;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 18px;
          font-weight: 600;
          cursor: pointer;
          transition: background 0.2s;
        }

        .start-button:hover {
          background: #1976d2;
        }

        .info-section {
          padding-top: 32px;
          border-top: 2px solid #f0f0f0;
        }

        .info-section h3 {
          margin: 0 0 16px 0;
          font-size: 18px;
          color: #333;
        }

        .info-section ul {
          margin: 0;
          padding-left: 24px;
          color: #666;
          line-height: 2;
        }

        @media (max-width: 768px) {
          .stats-overview {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default Phase4QuizExample;
