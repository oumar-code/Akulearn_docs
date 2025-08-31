import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import ChatInterface from '../components/ChatInterface';

export default function ChatScreen() {
  const [messages, setMessages] = useState([{ sender: 'AI', text: 'Hello!' }]);
  return (
    <>
      <Navbar role="student" />
      <ChatInterface messages={messages} onSend={msg => {/* handle message */}} />
    </>
  );
}
