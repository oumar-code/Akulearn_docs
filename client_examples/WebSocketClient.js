/**
 * Wave 3 WebSocket Client
 * Standalone JavaScript WebSocket client for real-time updates
 */

class Wave3WebSocketClient {
  constructor(studentId, config = {}) {
    this.studentId = studentId;
    this.config = {
      url: config.url || 'ws://localhost:8000/ws',
      reconnectInterval: config.reconnectInterval || 3000,
      maxReconnectAttempts: config.maxReconnectAttempts || 5,
      pingInterval: config.pingInterval || 30000,
      ...config
    };
    
    this.ws = null;
    this.reconnectAttempts = 0;
    this.listeners = {};
    this.pingIntervalId = null;
    this.isConnected = false;
  }

  /**
   * Connect to WebSocket server
   */
  connect() {
    const wsUrl = `${this.config.url}/${this.studentId}`;
    
    console.log(`Connecting to ${wsUrl}...`);
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.startPing();
      this.emit('connected', { studentId: this.studentId });
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('WebSocket message received:', data);
        this.handleMessage(data);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    };

    this.ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      this.isConnected = false;
      this.stopPing();
      this.emit('disconnected', { code: event.code, reason: event.reason });
      this.attemptReconnect();
    };
  }

  /**
   * Handle incoming messages
   */
  handleMessage(data) {
    const { type } = data;

    // Emit type-specific event
    this.emit(type, data);

    // Emit general message event
    this.emit('message', data);

    // Handle specific message types
    switch (type) {
      case 'connection_established':
        console.log('Connection established for student:', data.student_id);
        break;

      case 'mastery_update':
        console.log('Mastery updated:', data.lesson_id, data.mastery_data);
        break;

      case 'achievement_unlocked':
        console.log('Achievement unlocked:', data.achievement);
        this.showNotification('Achievement Unlocked!', data.achievement.name);
        break;

      case 'progress_update':
        console.log('Progress updated:', data.lesson_id, data.progress);
        break;

      case 'quiz_completed':
        console.log('Quiz completed:', data.quiz_id, data.score);
        break;

      case 'leaderboard_update':
        console.log('Leaderboard updated:', data.leaderboard);
        break;

      case 'pong':
        console.log('Pong received');
        break;

      default:
        console.warn('Unknown message type:', type);
    }
  }

  /**
   * Send message to server
   */
  send(type, data = {}) {
    if (!this.isConnected) {
      console.error('WebSocket not connected');
      return false;
    }

    const message = { type, ...data };
    this.ws.send(JSON.stringify(message));
    return true;
  }

  /**
   * Subscribe to topic
   */
  subscribe(topic) {
    return this.send('subscribe', { topic });
  }

  /**
   * Unsubscribe from topic
   */
  unsubscribe(topic) {
    return this.send('unsubscribe', { topic });
  }

  /**
   * Start ping to keep connection alive
   */
  startPing() {
    this.pingIntervalId = setInterval(() => {
      if (this.isConnected) {
        this.send('ping');
      }
    }, this.config.pingInterval);
  }

  /**
   * Stop ping
   */
  stopPing() {
    if (this.pingIntervalId) {
      clearInterval(this.pingIntervalId);
      this.pingIntervalId = null;
    }
  }

  /**
   * Attempt to reconnect
   */
  attemptReconnect() {
    if (this.reconnectAttempts >= this.config.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.emit('reconnect_failed');
      return;
    }

    this.reconnectAttempts++;
    console.log(`Reconnecting... (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      this.connect();
    }, this.config.reconnectInterval);
  }

  /**
   * Add event listener
   */
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  /**
   * Remove event listener
   */
  off(event, callback) {
    if (!this.listeners[event]) return;
    
    if (callback) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    } else {
      delete this.listeners[event];
    }
  }

  /**
   * Emit event to listeners
   */
  emit(event, data) {
    if (!this.listeners[event]) return;
    
    this.listeners[event].forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`Error in ${event} listener:`, error);
      }
    });
  }

  /**
   * Show browser notification
   */
  showNotification(title, body) {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, { body, icon: '/icon.png' });
    }
  }

  /**
   * Request notification permission
   */
  static async requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission();
    }
  }

  /**
   * Close connection
   */
  close() {
    this.stopPing();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Get connection status
   */
  getStatus() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      studentId: this.studentId
    };
  }
}

// Usage Example
if (typeof window !== 'undefined') {
  window.Wave3WebSocketClient = Wave3WebSocketClient;
}

// Export for Node.js/Module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Wave3WebSocketClient;
}

/*
 * USAGE EXAMPLE:
 * 
 * // Create client
 * const client = new Wave3WebSocketClient('student_001', {
 *   url: 'ws://localhost:8000/ws',
 *   reconnectInterval: 3000,
 *   maxReconnectAttempts: 5
 * });
 * 
 * // Request notification permission
 * await Wave3WebSocketClient.requestNotificationPermission();
 * 
 * // Add event listeners
 * client.on('connected', (data) => {
 *   console.log('Connected!', data);
 *   client.subscribe('progress');
 *   client.subscribe('achievements');
 * });
 * 
 * client.on('mastery_update', (data) => {
 *   console.log('Mastery updated:', data);
 *   updateMasteryUI(data.mastery_data);
 * });
 * 
 * client.on('achievement_unlocked', (data) => {
 *   console.log('New achievement:', data.achievement);
 *   showAchievementModal(data.achievement);
 * });
 * 
 * client.on('progress_update', (data) => {
 *   console.log('Progress:', data);
 *   updateProgressBar(data.progress);
 * });
 * 
 * client.on('error', (error) => {
 *   console.error('WebSocket error:', error);
 * });
 * 
 * client.on('disconnected', (data) => {
 *   console.log('Disconnected:', data);
 * });
 * 
 * // Connect
 * client.connect();
 * 
 * // Cleanup on page unload
 * window.addEventListener('beforeunload', () => {
 *   client.close();
 * });
 */
