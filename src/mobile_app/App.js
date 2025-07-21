import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './screens/auth/LoginScreen';
import SuperAdminDashboard from './screens/dashboards/SuperAdminDashboard';
import SchoolAdminDashboard from './screens/dashboards/SchoolAdminDashboard';
import TeacherDashboard from './screens/dashboards/TeacherDashboard';
import StudentDashboard from './screens/dashboards/StudentDashboard';
import GuardianDashboard from './screens/dashboards/GuardianDashboard';
import CorporateDashboard from './screens/dashboards/CorporateDashboard';
import GovernmentDashboard from './screens/dashboards/GovernmentDashboard';
import NgoPartnerDashboard from './screens/dashboards/NgoPartnerDashboard';
import ITSupportDashboard from './screens/dashboards/ITSupportDashboard';
import CreateSchoolScreen from './screens/dashboards/CreateSchoolScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="LoginScreen">
        <Stack.Screen name="LoginScreen" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen name="SuperAdminDashboard" component={SuperAdminDashboard} />
        <Stack.Screen name="SchoolAdminDashboard" component={SchoolAdminDashboard} />
        <Stack.Screen name="TeacherDashboard" component={TeacherDashboard} />
        <Stack.Screen name="StudentDashboard" component={StudentDashboard} />
        <Stack.Screen name="GuardianDashboard" component={GuardianDashboard} />
        <Stack.Screen name="CorporateDashboard" component={CorporateDashboard} />
        <Stack.Screen name="GovernmentDashboard" component={GovernmentDashboard} />
        <Stack.Screen name="NgoPartnerDashboard" component={NgoPartnerDashboard} />
        <Stack.Screen name="ITSupportDashboard" component={ITSupportDashboard} />
        <Stack.Screen name="CreateSchoolScreen" component={CreateSchoolScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
