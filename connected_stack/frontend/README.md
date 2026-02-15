# Akulearn Connected App - Frontend

A React Native application for Nigerian students preparing for WAEC, NECO, and JAMB exams.

## Features

### Authentication
- User registration with email/phone and exam board selection
- OTP email verification
- JWT-based login and token management
- Secure logout functionality

### Question Search & Discovery
- Advanced search with filters (exam board, subject, topic, difficulty, year)
- Real-time question search with keyword matching
- Browse questions by different criteria
- View full question details with explanations

### Quiz System
- Timed quizzes with configurable duration (default 30 minutes)
- Multiple choice questions with 4 options
- Answer logging and progress tracking
- Quiz completion with results summary

### Progress Analytics
- Overall accuracy tracking
- Performance breakdown by exam board and subject
- Weak topic identification
- Study streak tracking
- Visual progress indicators

## Project Structure

```
connected_stack/frontend/
├── App.js                 # Main app with navigation setup
├── UserContext.js         # User authentication context
├── api.js                 # API service functions
├── theme.js              # App theming (if used)
├── package.json          # Dependencies and scripts
├── screens/
│   ├── LoginScreen.js           # User login
│   ├── RegisterScreen.js        # User registration
│   ├── OtpVerificationScreen.js # OTP verification
│   ├── HomeScreen.js            # Dashboard/home screen
│   ├── SearchScreen.js          # Question search interface
│   ├── QuizScreen.js            # Quiz taking interface
│   └── ProgressScreen.js        # Progress dashboard
└── components/
    ├── QuizInterface.js    # Quiz components (legacy)
    └── ProgressDashboard.js # Progress components (legacy)
```

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- React Native development environment
- Android Studio (for Android) or Xcode (for iOS)

### Installation

1. Navigate to the frontend directory:
```bash
cd connected_stack/frontend
```

2. Install dependencies:
```bash
npm install
```

3. For iOS (macOS only):
```bash
cd ios && pod install && cd ..
```

### Running the App

1. Start the Metro bundler:
```bash
npm start
```

2. Run on Android:
```bash
npm run android
```

3. Run on iOS:
```bash
npm run ios
```

## Backend Connection

The app connects to a FastAPI backend running on `http://localhost:8000`. Make sure the backend is running before using the app.

### Backend Setup
```bash
cd connected_stack/backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Integration

The app uses the following API endpoints:

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/verify-otp` - OTP verification
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh-token` - Token refresh

### Questions
- `GET /api/questions/search` - Search questions with filters
- `GET /api/questions/{id}` - Get specific question
- `GET /api/questions/random` - Get random questions
- `POST /api/questions/attempt` - Submit answer attempt

### Progress
- `GET /api/user/progress` - Get user progress statistics

## Key Components

### Navigation
- Stack navigation for auth flow (Login → Register → OTP → Main App)
- Tab navigation for main app (Home, Search, Quiz, Progress)

### State Management
- React Context for user authentication state
- AsyncStorage for persistent login sessions
- Local component state for UI interactions

### UI/UX Features
- Custom dropdown modals (Picker alternative)
- Loading states and error handling
- Responsive design with proper spacing
- Color-coded difficulty indicators
- Progress bars and visual feedback

## Development Notes

### Custom Dropdowns
Instead of using `@react-native-picker/picker`, the app uses custom Modal-based dropdowns for better cross-platform compatibility and styling control.

### Error Handling
All API calls include proper error handling with user-friendly messages displayed via Alert dialogs.

### Performance
- FlatList for efficient question rendering
- Proper key props for list items
- Optimized re-renders with proper state management

## Testing

The app has been designed to work with the backend API. Make sure to:

1. Start the backend server first
2. Register a new user through the app
3. Verify email with OTP (check backend logs for OTP)
4. Login and test all features

## Future Enhancements

- Offline question caching
- Push notifications for study reminders
- Social features (leaderboards, study groups)
- Advanced analytics and insights
- PWA support for web deployment</content>
<parameter name="filePath">c:\Users\hp\Documents\Akulearn_docs\connected_stack\frontend\README.md