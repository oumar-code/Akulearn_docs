/**
 * Wave 3 WebSocket Client
 * Standalone JavaScript client for Wave 3 real-time updates
 * 
 * Usage:
 *   const client = new Wave3WebSocketClient('student_001');
 *   client.connect();
 *   client.subscribe('mastery_update', (data) => console.log(data));
 */

class Wave3WebSocketClient {
  constructor(studentId, options = {}) {
    this.studentId = studentId;
    this.wsUrl = options.wsUrl || `ws://localhost:8000/ws/${studentId}`;
    this.reconnectInterval = options.reconnectInterval || 5000;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 5;
    
    this.ws = null;
    this.reconnectAttempts = 0;
    this.subscribers = new Map();
    this.isConnected = false;
    this.reconnectTimer = null;
  }

  /**
   * Connect to WebSocket server
   */
  connect() {
    try {
      this.ws = new WebSocket(this.wsUrl);
      
      this.ws.onopen = () => {
        console.log('[Wave3WS] Connected');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this.emit('connection_established', { studentId: this.studentId });
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleMessage(data);
        } catch (error) {
          console.error('[Wave3WS] Parse error:', error);
        }
      };

      this.ws.onerror = (error) => {
        console.error('[Wave3WS] Error:', error);
        this.emit('error', { error });
      };

      this.ws.onclose = () => {
        console.log('[Wave3WS] Disconnected');
        this.isConnected = false;
        this.emit('disconnected', {});
        this.attemptReconnect();
      };
    } catch (error) {
      console.error('[Wave3WS] Connection error:', error);
      this.attemptReconnect();
    }
  }

  /**
   * Handle incoming WebSocket message
   */
  handleMessage(data) {
    const { type, ...payload } = data;
    
    console.log('[Wave3WS] Message:', type, payload);
    
    // Emit to specific subscribers
    if (this.subscribers.has(type)) {
      const callbacks = this.subscribers.get(type);
      callbacks.forEach(callback => callback(payload));
    }
    
    // Emit to wildcard subscribers
    if (this.subscribers.has('*')) {
      const callbacks = this.subscribers.get('*');
      callbacks.forEach(callback => callback(data));
    }
  }

  /**
   * Subscribe to specific message type
   */
  subscribe(messageType, callback) {
    if (!this.subscribers.has(messageType)) {
      this.subscribers.set(messageType, []);
    }
    this.subscribers.get(messageType).push(callback);
    
    return () => this.unsubscribe(messageType, callback);
  }

  /**
   * Unsubscribe from message type
   */
  unsubscribe(messageType, callback) {
    if (this.subscribers.has(messageType)) {
      const callbacks = this.subscribers.get(messageType);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  /**
   * Emit event to subscribers
   */
  emit(type, payload) {
    this.handleMessage({ type, ...payload });
  }

  /**
   * Send message to server
   */
  send(type, data = {}) {
    if (!this.isConnected) {
      console.warn('[Wave3WS] Not connected, cannot send message');
      return false;
    }
    
    try {
      const message = JSON.stringify({ type, ...data });
      this.ws.send(message);
      return true;
    } catch (error) {
      console.error('[Wave3WS] Send error:', error);
      return false;
    }
  }

  /**
   * Subscribe to topic (if server supports topic-based subscriptions)
   */
  subscribeTopic(topic) {
    return this.send('subscribe', { topic });
  }

  /**
   * Unsubscribe from topic
   */
  unsubscribeTopic(topic) {
    return this.send('unsubscribe', { topic });
  }

  /**
   * Attempt to reconnect
   */
  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('[Wave3WS] Max reconnect attempts reached');
      this.emit('max_reconnect_attempts', {});
      return;
    }

    this.reconnectAttempts++;
    console.log(`[Wave3WS] Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
    
    this.reconnectTimer = setTimeout(() => {
      this.connect();
    }, this.reconnectInterval);
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    this.isConnected = false;
    this.subscribers.clear();
  }

  /**
   * Get connection status
   */
  getStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      subscriberCount: this.subscribers.size
    };
  }
}

// Example Usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Wave3WebSocketClient;
}

// Browser example
if (typeof window !== 'undefined') {
  // Create client instance
  const client = new Wave3WebSocketClient('student_001', {
    wsUrl: 'ws://localhost:8000/ws/student_001',
    reconnectInterval: 5000,
    maxReconnectAttempts: 5
  });

  // Subscribe to specific events
  client.subscribe('mastery_update', (data) => {
    console.log('Mastery updated:', data);
    // Update UI with new mastery data
    updateMasteryUI(data);
  });

  client.subscribe('achievement_unlocked', (data) => {
    console.log('Achievement unlocked:', data);
    // Show achievement notification
    showAchievementNotification(data.achievement);
  });

  client.subscribe('progress_update', (data) => {
    console.log('Progress updated:', data);
    // Update progress bars
    updateProgressUI(data);
  });

  client.subscribe('quiz_result', (data) => {
    console.log('Quiz result:', data);
    // Show quiz results
    showQuizResults(data);
  });

  client.subscribe('leaderboard_update', (data) => {
    console.log('Leaderboard updated:', data);
    // Refresh leaderboard
    refreshLeaderboard(data.leaderboard);
  });

  // Subscribe to all messages (wildcard)
  client.subscribe('*', (data) => {
    console.log('WebSocket message:', data);
  });

  // Connect to server
  client.connect();

  // Subscribe to topics
  client.subscribeTopic('achievements');
  client.subscribeTopic('leaderboard');

  // Example UI update functions (implement based on your UI framework)
  function updateMasteryUI(data) {
    const element = document.getElementById(`mastery-${data.lesson_id}`);
    if (element) {
      element.textContent = `${data.mastery_data.mastery_percentage}%`;
      element.className = `mastery-badge mastery-${data.mastery_data.mastery_level}`;
    }
  }

  function showAchievementNotification(achievement) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'achievement-notification';
    notification.innerHTML = `
      <div class="achievement-icon">${achievement.icon}</div>
      <div class="achievement-content">
        <h4>${achievement.name}</h4>
        <p>${achievement.description}</p>
        <span class="badge-level">${achievement.badge_level}</span>
      </div>
    `;
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => notification.remove(), 5000);
  }

  function updateProgressUI(data) {
    const progressBar = document.getElementById(`progress-${data.lesson_id}`);
    if (progressBar) {
      progressBar.style.width = `${data.progress}%`;
    }
  }

  function showQuizResults(data) {
    const modal = document.getElementById('quiz-results-modal');
    if (modal) {
      modal.querySelector('.score').textContent = `${data.score}/${data.max_score}`;
      modal.querySelector('.percentage').textContent = `${Math.round((data.score/data.max_score)*100)}%`;
      modal.style.display = 'block';
    }
  }

  function refreshLeaderboard(leaderboard) {
    const list = document.getElementById('leaderboard-list');
    if (list) {
      list.innerHTML = leaderboard.map((entry, index) => `
        <div class="leaderboard-entry">
          <span class="rank">${index + 1}</span>
          <span class="name">${entry.student_name}</span>
          <span class="points">${entry.points}</span>
        </div>
      `).join('');
    }
  }

  // Clean up on page unload
  window.addEventListener('beforeunload', () => {
    client.disconnect();
  });

  // Export for global access
  window.Wave3Client = client;
}
