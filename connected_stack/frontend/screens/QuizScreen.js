import React from 'react';
import Navbar from '../components/Navbar';
import QuizInterface from '../components/QuizInterface';

export default function QuizScreen() {
  const questions = [{ text: 'What is 2+2?' }];
  return (
    <>
      <Navbar role="student" />
      <QuizInterface questions={questions} onSubmit={answers => {/* handle answers */}} />
    </>
  );
}
