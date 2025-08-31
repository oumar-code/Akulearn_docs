// React Context for user role
import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const UserContext = createContext();

export function UserProvider({ children }) {
  const [role, setRole] = useState('student');
  useEffect(() => {
    AsyncStorage.getItem('role').then(r => r && setRole(r));
  }, []);
  return (
    <UserContext.Provider value={{ role, setRole }}>
      {children}
    </UserContext.Provider>
  );
}
