import React, { useState, useContext } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
  StyleSheet,
  Modal
} from 'react-native';
import { UserContext } from '../UserContext';
import { registerUser } from '../api';

const SUBJECTS = [
  'Mathematics',
  'Physics',
  'Chemistry',
  'Biology',
  'English Language',
  'Use of English',
  'Geography',
  'History',
  'Economics',
  'Commerce',
  'Accounting',
  'Literature in English',
  'Government',
  'Christian Religious Studies',
  'Islamic Religious Studies'
];

const EXAM_BOARDS = ['WAEC', 'NECO', 'JAMB'];

export default function RegisterScreen({ navigation }) {
  const { login } = useContext(UserContext);
  const [formData, setFormData] = useState({
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    examBoard: 'WAEC',
    targetSubjects: []
  });
  const [showExamBoardPicker, setShowExamBoardPicker] = useState(false);

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const toggleSubject = (subject) => {
    setFormData(prev => ({
      ...prev,
      targetSubjects: prev.targetSubjects.includes(subject)
        ? prev.targetSubjects.filter(s => s !== subject)
        : [...prev.targetSubjects, subject]
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email || !formData.email.includes('@')) {
      newErrors.email = 'Valid email is required';
    }
    if (!formData.phone || formData.phone.length < 10) {
      newErrors.phone = 'Valid phone number is required';
    }
    if (!formData.password || formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    }
    if (formData.targetSubjects.length === 0) {
      newErrors.targetSubjects = 'Select at least one subject';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleRegister = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      const result = await registerUser({
        email: formData.email,
        phone: formData.phone,
        password: formData.password,
        full_name: formData.fullName,
        exam_board: formData.examBoard,
        target_subjects: formData.targetSubjects
      });

      Alert.alert(
        'Registration Successful',
        'Please check your email for OTP verification',
        [
          {
            text: 'OK',
            onPress: () => navigation.navigate('OtpVerification', {
              email: formData.email,
              userId: result.user_id
            })
          }
        ]
      );
    } catch (error) {
      Alert.alert('Registration Failed', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Create Account</Text>

      <TextInput
        style={[styles.input, errors.email && styles.inputError]}
        placeholder="Email"
        value={formData.email}
        onChangeText={(value) => updateFormData('email', value)}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      {errors.email && <Text style={styles.errorText}>{errors.email}</Text>}

      <TextInput
        style={[styles.input, errors.phone && styles.inputError]}
        placeholder="Phone Number"
        value={formData.phone}
        onChangeText={(value) => updateFormData('phone', value)}
        keyboardType="phone-pad"
      />
      {errors.phone && <Text style={styles.errorText}>{errors.phone}</Text>}

      <TextInput
        style={[styles.input, errors.fullName && styles.inputError]}
        placeholder="Full Name"
        value={formData.fullName}
        onChangeText={(value) => updateFormData('fullName', value)}
      />
      {errors.fullName && <Text style={styles.errorText}>{errors.fullName}</Text>}

      <TextInput
        style={[styles.input, errors.password && styles.inputError]}
        placeholder="Password"
        value={formData.password}
        onChangeText={(value) => updateFormData('password', value)}
        secureTextEntry
      />
      {errors.password && <Text style={styles.errorText}>{errors.password}</Text>}

      <TextInput
        style={[styles.input, errors.confirmPassword && styles.inputError]}
        placeholder="Confirm Password"
        value={formData.confirmPassword}
        onChangeText={(value) => updateFormData('confirmPassword', value)}
        secureTextEntry
      />
      {errors.confirmPassword && <Text style={styles.errorText}>{errors.confirmPassword}</Text>}

      <Text style={styles.label}>Exam Board</Text>
      <TouchableOpacity
        style={styles.pickerContainer}
        onPress={() => setShowExamBoardPicker(true)}
      >
        <Text style={styles.pickerText}>{formData.examBoard}</Text>
      </TouchableOpacity>

      <Modal visible={showExamBoardPicker} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Select Exam Board</Text>
            {EXAM_BOARDS.map(board => (
              <TouchableOpacity
                key={board}
                style={styles.modalOption}
                onPress={() => {
                  updateFormData('examBoard', board);
                  setShowExamBoardPicker(false);
                }}
              >
                <Text style={[
                  styles.modalOptionText,
                  formData.examBoard === board && styles.modalOptionSelected
                ]}>
                  {board}
                </Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity
              style={styles.modalClose}
              onPress={() => setShowExamBoardPicker(false)}
            >
              <Text style={styles.modalCloseText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      <Text style={styles.label}>Target Subjects</Text>
      <View style={styles.subjectsContainer}>
        {SUBJECTS.map(subject => (
          <TouchableOpacity
            key={subject}
            style={[
              styles.subjectChip,
              formData.targetSubjects.includes(subject) && styles.subjectChipSelected
            ]}
            onPress={() => toggleSubject(subject)}
          >
            <Text style={[
              styles.subjectChipText,
              formData.targetSubjects.includes(subject) && styles.subjectChipTextSelected
            ]}>
              {subject}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {errors.targetSubjects && <Text style={styles.errorText}>{errors.targetSubjects}</Text>}

      <TouchableOpacity
        style={[styles.button, loading && styles.buttonDisabled]}
        onPress={handleRegister}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Register</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.linkButton}
        onPress={() => navigation.navigate('Login')}
      >
        <Text style={styles.linkText}>Already have an account? Login</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  pickerContainer: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 15,
    backgroundColor: '#fff',
    marginBottom: 20,
  },
  pickerText: {
    fontSize: 16,
    color: '#333',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    width: '80%',
    maxHeight: '60%',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  modalOption: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  modalOptionText: {
    fontSize: 16,
    color: '#333',
  },
  modalOptionSelected: {
    color: '#3498db',
    fontWeight: 'bold',
  },
  modalClose: {
    marginTop: 20,
    padding: 15,
    alignItems: 'center',
  },
  modalCloseText: {
    color: '#666',
    fontSize: 16,
  },marginBottom: 5,
    borderRadius: 8,
    fontSize: 16,
  },
  inputError: {
    borderColor: '#e74c3c',
  },
  errorText: {
    color: '#e74c3c',
    fontSize: 14,
    marginBottom: 10,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#333',
  },
  pickerContainer: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    marginBottom: 20,
  },
  picker: {
    height: 50,
  },
  subjectsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 10,
  },
  subjectChip: {
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    margin: 4,
  },
  subjectChipSelected: {
    backgroundColor: '#3498db',
  },
  subjectChipText: {
    fontSize: 14,
    color: '#333',
  },
  subjectChipTextSelected: {
    color: '#fff',
  },
  button: {
    backgroundColor: '#3498db',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  linkButton: {
    alignItems: 'center',
    marginTop: 20,
  },
  linkText: {
    color: '#3498db',
    fontSize: 16,
  },
});