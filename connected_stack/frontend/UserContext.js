// React Context for user authentication and data
import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const UserContext = createContext();

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load stored user data and token on app start
    const loadStoredData = async () => {
      try {
        const storedUser = await AsyncStorage.getItem('user');
        const storedToken = await AsyncStorage.getItem('token');
        if (storedUser && storedToken) {
          setUser(JSON.parse(storedUser));
          setToken(storedToken);
        }
      } catch (error) {
        console.error('Error loading stored data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadStoredData();
  }, []);

  const login = async (userData, accessToken) => {
    setUser(userData);
    setToken(accessToken);
    await AsyncStorage.setItem('user', JSON.stringify(userData));
    await AsyncStorage.setItem('token', accessToken);
  };

  const logout = async () => {
    setUser(null);
    setToken(null);
    await AsyncStorage.removeItem('user');
    await AsyncStorage.removeItem('token');
  };

  const updateUser = async (updatedUserData) => {
    const newUser = { ...user, ...updatedUserData };
    setUser(newUser);
    await AsyncStorage.setItem('user', JSON.stringify(newUser));
  };

  return (
    <UserContext.Provider value={{
      user,
      token,
      isLoading,
      login,
      logout,
      updateUser
    }}>
      {children}
    </UserContext.Provider>
  );
}
