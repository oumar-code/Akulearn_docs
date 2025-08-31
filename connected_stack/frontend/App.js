import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Dashboard from './screens/Dashboard';
import Login from './screens/Login';
import { UserProvider, UserContext } from './UserContext';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Login" component={Login} />
        <Stack.Screen name="Dashboard" component={Dashboard} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

function AppNavigator() {
  const { user, token } = useContext(UserContext);
  useEffect(() => {
    // Optionally, validate token or fetch user role on mount
  }, [token]);
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={token ? "Dashboard" : "Login"}>
        {!token ? (
          <Stack.Screen name="Login" component={Login} />
        ) : (
          <Stack.Screen name="Dashboard" component={Dashboard} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <UserProvider>
      <AppNavigator />
    </UserProvider>
  );
}
