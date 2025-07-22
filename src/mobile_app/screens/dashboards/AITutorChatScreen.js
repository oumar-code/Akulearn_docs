
import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, FlatList, ActivityIndicator } from 'react-native';
import NetInfo from '@react-native-community/netinfo';
import { offlineAITutorResponses, offlineFallback } from './AITutorChatScreen.offlineResponses';

export default function AITutorChatScreen() {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Hello! I am your Akulearn AI Tutor. Ask me anything about your studies.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(true);
  const flatListRef = useRef();

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected);
    });
    return () => unsubscribe();
  }, []);

  const getOfflineResponse = (userInput) => {
    for (const item of offlineAITutorResponses) {
      if (item.match.test(userInput)) return item.response;
    }
    return offlineFallback;
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    let aiResponse = '';
    if (!isConnected) {
      aiResponse = getOfflineResponse(userMsg.text);
    } else {
      try {
        const res = await fetch('https://your-backend-api/ai-tutor', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userMsg.text })
        });
        const data = await res.json();
        aiResponse = data.response || offlineFallback;
      } catch {
        aiResponse = offlineFallback;
      }
    }
    setMessages(prev => [...prev, { sender: 'ai', text: aiResponse }]);
    setLoading(false);
    setTimeout(() => flatListRef.current?.scrollToEnd({ animated: true }), 100);
  };

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.title}>AI Tutor Chat</Text>
        <View style={styles.statusRow}>
          <View style={[styles.statusDot, { backgroundColor: isConnected ? '#28a745' : '#d9534f' }]} />
          <Text style={{ color: isConnected ? '#28a745' : '#d9534f', marginLeft: 4, fontWeight: 'bold' }}>
            {isConnected ? 'Online' : 'Offline'}
          </Text>
        </View>
      </View>
      {!isConnected && (
        <Text style={styles.offlineBanner}>You are currently offline, using local AI capabilities.</Text>
      )}
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(_, idx) => idx.toString()}
        renderItem={({ item }) => (
          <View style={[styles.msgBubble, item.sender === 'ai' ? styles.aiBubble : styles.userBubble]}>
            <Text style={styles.msgText}>{item.text}</Text>
          </View>
        )}
        contentContainerStyle={{ paddingVertical: 10 }}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
      />
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Type your question..."
          value={input}
          onChangeText={setInput}
          onSubmitEditing={sendMessage}
          editable={!loading}
        />
        <TouchableOpacity style={styles.sendBtn} onPress={sendMessage} disabled={loading || !input.trim()}>
          <Text style={styles.sendBtnText}>{loading ? '...' : 'Send'}</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f9f9f9', padding: 0 },
  headerRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', padding: 16, backgroundColor: '#fff', borderBottomWidth: 1, borderColor: '#eee' },
  title: { fontSize: 22, fontWeight: 'bold' },
  statusRow: { flexDirection: 'row', alignItems: 'center' },
  statusDot: { width: 10, height: 10, borderRadius: 5 },
  offlineBanner: { backgroundColor: '#fff3cd', color: '#856404', padding: 8, textAlign: 'center', fontSize: 15 },
  msgBubble: { marginHorizontal: 12, marginVertical: 4, padding: 12, borderRadius: 12, maxWidth: '80%' },
  aiBubble: { backgroundColor: '#e9ecef', alignSelf: 'flex-start' },
  userBubble: { backgroundColor: '#007bff', alignSelf: 'flex-end' },
  msgText: { color: '#222', fontSize: 16 },
  inputRow: { flexDirection: 'row', alignItems: 'center', padding: 12, backgroundColor: '#fff', borderTopWidth: 1, borderColor: '#eee' },
  input: { flex: 1, borderWidth: 1, borderColor: '#ccc', borderRadius: 20, padding: 10, backgroundColor: '#fff', marginRight: 8 },
  sendBtn: { backgroundColor: '#007bff', borderRadius: 20, paddingVertical: 10, paddingHorizontal: 18 },
  sendBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
});
