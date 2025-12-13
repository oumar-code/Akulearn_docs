import React, { useState, useContext } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  StyleSheet
} from 'react-native';
import { UserContext } from '../UserContext';
import { verifyOtp } from '../api';

export default function OtpVerificationScreen({ navigation, route }) {
  const { login } = useContext(UserContext);
  const { email, userId } = route.params;
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);

  const handleVerifyOtp = async () => {
    if (!otp || otp.length !== 6) {
      Alert.alert('Error', 'Please enter a valid 6-digit OTP');
      return;
    }

    setLoading(true);
    try {
      const result = await verifyOtp(email, otp);

      if (result.verified) {
        Alert.alert(
          'Success',
          'Email verified successfully! Please login to continue.',
          [
            {
              text: 'OK',
              onPress: () => navigation.navigate('Login')
            }
          ]
        );
      }
    } catch (error) {
      Alert.alert('Verification Failed', error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    // TODO: Implement resend OTP functionality
    Alert.alert('Info', 'OTP resend functionality will be implemented');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Verify Your Email</Text>

      <Text style={styles.subtitle}>
        We've sent a 6-digit code to {email}
      </Text>

      <TextInput
        style={styles.otpInput}
        placeholder="Enter 6-digit code"
        value={otp}
        onChangeText={setOtp}
        keyboardType="numeric"
        maxLength={6}
        textAlign="center"
        fontSize={24}
        letterSpacing={8}
      />

      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={handleVerifyOtp}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Verify</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.resendButton}
        onPress={handleResendOtp}
      >
        <Text style={styles.resendText}>Didn't receive code? Resend</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.backButton}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.backText}>Back to Registration</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 40,
    color: '#666',
    lineHeight: 22,
  },
  otpInput: {
    borderWidth: 2,
    borderColor: '#3498db',
    padding: 20,
    marginBottom: 30,
    borderRadius: 12,
    fontSize: 24,
    textAlign: 'center',
    letterSpacing: 8,
    backgroundColor: '#f9f9f9',
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 20,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  resendButton: {
    alignItems: 'center',
    marginBottom: 30,
  },
  resendText: {
    color: '#3498db',
    fontSize: 16,
    textDecorationLine: 'underline',
  },
  backButton: {
    alignItems: 'center',
  },
  backText: {
    color: '#666',
    fontSize: 16,
  },
});