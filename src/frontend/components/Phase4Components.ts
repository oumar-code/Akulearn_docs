/**
 * Phase 4 Components - Practice Questions
 * 
 * Export all Phase 4 components and hooks for easy importing
 */

// Hooks
export { usePhase4Questions } from '../hooks/usePhase4Questions';
export type {
  QuestionInfo,
  QuestionDetail,
  AnswerValidation,
  Phase4Stats,
  SubjectStats,
  QuizGenerationOptions
} from '../hooks/usePhase4Questions';

// Components
export { QuestionViewer } from './QuestionViewer';
export { QuizInterface } from './QuizInterface';
export type { QuizConfig, QuizResults } from './QuizInterface';
export { ResultsSummary } from './ResultsSummary';
export { Phase4QuizExample } from './Phase4QuizExample';

// Default exports for convenience
export { default as usePhase4QuestionsHook } from '../hooks/usePhase4Questions';
export { default as QuestionViewerComponent } from './QuestionViewer';
export { default as QuizInterfaceComponent } from './QuizInterface';
export { default as ResultsSummaryComponent } from './ResultsSummary';
export { default as Phase4QuizExampleComponent } from './Phase4QuizExample';
