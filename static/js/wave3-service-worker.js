/* 
Wave 3 Service Worker - Offline Support
Provides PWA functionality and offline access to lessons
*/

const CACHE_VERSION = 'wave3-v1';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const DYNAMIC_CACHE = `${CACHE_VERSION}-dynamic`;
const LESSONS_CACHE = `${CACHE_VERSION}-lessons`;

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/js/api.js',
  '/offline.html'
];

// Cache size limits
const CACHE_LIMITS = {
  [DYNAMIC_CACHE]: 50,
  [LESSONS_CACHE]: 100
};

// === Installation ===
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('[Service Worker] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// === Activation ===
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(name => name.startsWith('wave3-') && name !== CACHE_VERSION)
            .map(name => {
              console.log('[Service Worker] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => self.clients.claim())
  );
});

// === Fetch Strategy ===
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }
  
  // Route to appropriate strategy
  if (isAPIRequest(url)) {
    event.respondWith(networkFirstStrategy(request));
  } else if (isLessonContent(url)) {
    event.respondWith(cacheFirstStrategy(request, LESSONS_CACHE));
  } else if (isStaticAsset(url)) {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
  } else {
    event.respondWith(staleWhileRevalidateStrategy(request));
  }
});

// === Caching Strategies ===

// Network First (for API requests)
async function networkFirstStrategy(request) {
  try {
    const response = await fetch(request);
    
    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, response.clone());
      trimCache(DYNAMIC_CACHE, CACHE_LIMITS[DYNAMIC_CACHE]);
    }
    
    return response;
  } catch (error) {
    console.log('[Service Worker] Network failed, trying cache:', request.url);
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page for navigation requests
    if (request.mode === 'navigate') {
      return caches.match('/offline.html');
    }
    
    // Return offline JSON response for API requests
    if (isAPIRequest(new URL(request.url))) {
      return new Response(
        JSON.stringify({
          error: 'Offline',
          message: 'You are currently offline. Some features may be unavailable.'
        }),
        {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
    
    throw error;
  }
}

// Cache First (for static assets and lesson content)
async function cacheFirstStrategy(request, cacheName) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
      trimCache(cacheName, CACHE_LIMITS[cacheName]);
    }
    
    return response;
  } catch (error) {
    console.error('[Service Worker] Cache and network failed:', request.url);
    throw error;
  }
}

// Stale While Revalidate (for dynamic content)
async function staleWhileRevalidateStrategy(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cachedResponse = await cache.match(request);
  
  const fetchPromise = fetch(request)
    .then(response => {
      if (response.ok) {
        cache.put(request, response.clone());
        trimCache(DYNAMIC_CACHE, CACHE_LIMITS[DYNAMIC_CACHE]);
      }
      return response;
    })
    .catch(() => cachedResponse);
  
  return cachedResponse || fetchPromise;
}

// === Helper Functions ===

function isAPIRequest(url) {
  return url.pathname.startsWith('/api/');
}

function isLessonContent(url) {
  return url.pathname.startsWith('/api/v3/lessons/') ||
         url.pathname.startsWith('/api/v3/content/');
}

function isStaticAsset(url) {
  return url.pathname.startsWith('/static/') ||
         url.pathname.match(/\.(css|js|png|jpg|jpeg|svg|woff2?)$/);
}

async function trimCache(cacheName, maxItems) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  
  if (keys.length > maxItems) {
    const toDelete = keys.slice(0, keys.length - maxItems);
    await Promise.all(toDelete.map(key => cache.delete(key)));
  }
}

// === Background Sync ===
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] Background sync:', event.tag);
  
  if (event.tag === 'sync-progress') {
    event.waitUntil(syncProgressData());
  } else if (event.tag === 'sync-analytics') {
    event.waitUntil(syncAnalyticsData());
  }
});

async function syncProgressData() {
  try {
    // Get pending progress updates from IndexedDB
    const db = await openDB();
    const pendingUpdates = await db.getAll('pendingProgress');
    
    // Send to server
    for (const update of pendingUpdates) {
      const response = await fetch('/api/v3/progress/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(update)
      });
      
      if (response.ok) {
        await db.delete('pendingProgress', update.id);
      }
    }
    
    console.log('[Service Worker] Progress data synced');
  } catch (error) {
    console.error('[Service Worker] Sync failed:', error);
    throw error; // Retry later
  }
}

async function syncAnalyticsData() {
  try {
    const db = await openDB();
    const pendingEvents = await db.getAll('pendingAnalytics');
    
    if (pendingEvents.length > 0) {
      const response = await fetch('/api/v3/analytics/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ events: pendingEvents })
      });
      
      if (response.ok) {
        await db.clear('pendingAnalytics');
      }
    }
    
    console.log('[Service Worker] Analytics synced');
  } catch (error) {
    console.error('[Service Worker] Analytics sync failed:', error);
  }
}

// === Push Notifications ===
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};
  
  const title = data.title || 'Akulearn Notification';
  const options = {
    body: data.body || 'You have a new notification',
    icon: '/static/icons/icon-192.png',
    badge: '/static/icons/badge-72.png',
    data: data,
    actions: data.actions || []
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  const urlToOpen = event.notification.data?.url || '/';
  
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(windowClients => {
        // Focus existing window if available
        for (const client of windowClients) {
          if (client.url === urlToOpen && 'focus' in client) {
            return client.focus();
          }
        }
        
        // Open new window
        if (clients.openWindow) {
          return clients.openWindow(urlToOpen);
        }
      })
  );
});

// === IndexedDB Helper ===
async function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('Wave3OfflineDB', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      
      if (!db.objectStoreNames.contains('pendingProgress')) {
        db.createObjectStore('pendingProgress', { keyPath: 'id', autoIncrement: true });
      }
      
      if (!db.objectStoreNames.contains('pendingAnalytics')) {
        db.createObjectStore('pendingAnalytics', { keyPath: 'id', autoIncrement: true });
      }
      
      if (!db.objectStoreNames.contains('cachedLessons')) {
        db.createObjectStore('cachedLessons', { keyPath: 'lesson_id' });
      }
    };
  });
}

// === Message Handler ===
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_LESSON') {
    event.waitUntil(cacheLessonContent(event.data.lessonId));
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then(names => Promise.all(names.map(n => caches.delete(n))))
    );
  }
});

async function cacheLessonContent(lessonId) {
  try {
    const cache = await caches.open(LESSONS_CACHE);
    const lessonUrl = `/api/v3/lessons/${lessonId}`;
    
    const response = await fetch(lessonUrl);
    if (response.ok) {
      await cache.put(lessonUrl, response.clone());
      
      // Store in IndexedDB for richer offline experience
      const db = await openDB();
      const lesson = await response.json();
      
      const transaction = db.transaction(['cachedLessons'], 'readwrite');
      const store = transaction.objectStore('cachedLessons');
      await store.put(lesson);
      
      console.log('[Service Worker] Lesson cached:', lessonId);
    }
  } catch (error) {
    console.error('[Service Worker] Failed to cache lesson:', error);
  }
}

console.log('[Service Worker] Loaded');
