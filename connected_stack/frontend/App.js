import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';
import { UserProvider } from './UserContext';

// Import screens
import RegisterScreen from './screens/RegisterScreen';
import OtpVerificationScreen from './screens/OtpVerificationScreen';
import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import SearchScreen from './screens/SearchScreen';
import QuizScreen from './screens/QuizScreen';
import ProgressScreen from './screens/ProgressScreen';
import LearnScreen from './screens/LearnScreen';
import ContentReaderScreen from './screens/ContentReaderScreen';

// New feature screens
import CodePlaygroundScreen from './screens/CodePlaygroundScreen';
import DatasetExplorerScreen from './screens/DatasetExplorerScreen';
import EncyclopediaScreen from './screens/EncyclopediaScreen';
import FlashcardScreen from './screens/FlashcardScreen';
import GameHubScreen from './screens/GameHubScreen';
import ResearchHubScreen from './screens/ResearchHubScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#3498db',
        tabBarInactiveTintColor: '#666',
        tabBarStyle: {
          backgroundColor: '#fff',
          borderTopColor: '#e0e0e0',
        },
        headerStyle: {
          backgroundColor: '#3498db',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Text style={{ color, fontSize: size }}>🏠</Text>
          ),
        }}
      />
      <Tab.Screen
        name="Search"
        component={SearchScreen}
        options={{
          title: 'Search',
          tabBarIcon: ({ color, size }) => (
            <Text style={{ color, fontSize: size }}>🔍</Text>
          ),
        }}
      />
      <Tab.Screen
        name="Learn"
        component={LearnScreen}
        options={{
          title: 'Learn',
          tabBarIcon: ({ color, size }) => (
            <Text style={{ color, fontSize: size }}>📚</Text>
          ),
        }}
      />
      <Tab.Screen
        name="Progress"
        component={ProgressScreen}
        options={{
          title: 'Progress',
          tabBarIcon: ({ color, size }) => (
            <Text style={{ color, fontSize: size }}>📊</Text>
          ),
        }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <UserProvider>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="Login"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#3498db',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen
            name="Login"
            component={LoginScreen}
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="Register"
            component={RegisterScreen}
            options={{ title: 'Register' }}
          />
          <Stack.Screen
            name="OtpVerification"
            component={OtpVerificationScreen}
            options={{ title: 'Verify Email' }}
          />
          <Stack.Screen
            name="MainTabs"
            component={TabNavigator}
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="ContentReader"
            component={ContentReaderScreen}
            options={{ title: 'Content' }}
          />
          <Stack.Screen
            name="CodePlayground"
            component={CodePlaygroundScreen}
            options={{ title: 'Code Playground' }}
          />
          <Stack.Screen
            name="DatasetExplorer"
            component={DatasetExplorerScreen}
            options={{ title: 'Dataset Explorer' }}
          />
          <Stack.Screen
            name="Encyclopedia"
            component={EncyclopediaScreen}
            options={{ title: 'Encyclopedia' }}
          />
          <Stack.Screen
            name="Flashcard"
            component={FlashcardScreen}
            options={{ title: 'Flashcards' }}
          />
          <Stack.Screen
            name="GameHub"
            component={GameHubScreen}
            options={{ title: 'Game Hub' }}
          />
          <Stack.Screen
            name="ResearchHub"
            component={ResearchHubScreen}
            options={{ title: 'Research Hub' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </UserProvider>
  );
}
