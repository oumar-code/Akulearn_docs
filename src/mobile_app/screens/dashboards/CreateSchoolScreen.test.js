import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import CreateSchoolScreen from './CreateSchoolScreen';

jest.mock('react-native/Libraries/Alert/Alert', () => ({
  alert: jest.fn(),
}));

describe('CreateSchoolScreen', () => {
  it('renders all form fields', () => {
    const { getByPlaceholderText } = render(<CreateSchoolScreen navigation={{ goBack: jest.fn() }} />);
    expect(getByPlaceholderText('school name')).toBeTruthy();
    expect(getByPlaceholderText('address')).toBeTruthy();
    expect(getByPlaceholderText('city')).toBeTruthy();
    expect(getByPlaceholderText('state')).toBeTruthy();
    expect(getByPlaceholderText('contact email')).toBeTruthy();
    expect(getByPlaceholderText('phone number')).toBeTruthy();
    expect(getByPlaceholderText('Admin email')).toBeTruthy();
    expect(getByPlaceholderText('Admin password')).toBeTruthy();
    expect(getByPlaceholderText('Admin first name')).toBeTruthy();
    expect(getByPlaceholderText('Admin last name')).toBeTruthy();
  });

  it('shows error on failed submit', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        json: () => Promise.resolve({ detail: 'Failed to create school.' }),
      })
    );
    const { getByText } = render(<CreateSchoolScreen navigation={{ goBack: jest.fn() }} />);
    fireEvent.press(getByText('Create School'));
    await waitFor(() => getByText('Failed to create school.'));
  });

  it('shows success alert and navigates back on success', async () => {
    const goBack = jest.fn();
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({}),
      })
    );
    const { getByText } = render(<CreateSchoolScreen navigation={{ goBack }} />);
    fireEvent.press(getByText('Create School'));
    await waitFor(() => {
      expect(goBack).toHaveBeenCalled();
    });
  });
});
