# Client SDK Examples

Reference implementations for integrating with the Aku Platform Wave 3 APIs.  
All files live in [`client_examples/`](https://github.com/oumar-code/Akulearn_docs/tree/main/client_examples) at the repo root.

---

## Overview

The Wave 3 API surface has three integration points:

| Protocol | Endpoint | Use |
|----------|----------|-----|
| **GraphQL** (Apollo) | `/graphql` | Queries, mutations, subscriptions for lessons, progress, recommendations |
| **WebSocket** | `/ws/{studentId}` | Real-time progress updates, leaderboard events |
| **REST** | `/api/v1/...` | File upload, auth, admin |

---

## File Reference

### Foundation — Apollo & GraphQL

| File | Purpose |
|------|---------|
| `apolloClient.js` | Apollo Client setup — HTTP + WebSocket split link, auth headers, error handling |
| `graphqlQueries.js` | All GQL definitions: `GET_LESSON`, `GET_STUDENT_PROGRESS`, `GET_RECOMMENDATIONS`, `GET_LEADERBOARD`, `RECORD_QUIZ_RESULT`, `SUBSCRIBE_TO_PROGRESS_UPDATES` |
| `ApolloUsageExamples.jsx` | React components using `useQuery` / `useMutation` / `useSubscription` — ready-to-copy lesson, progress, and leaderboard UIs |

### Real-Time Updates

| File | Purpose |
|------|---------|
| `WebSocketClient.js` | Standalone JS class — connect, auto-reconnect with backoff, ping/pong keep-alive, typed event emission |

### Data Visualizations

| File | Purpose |
|------|---------|
| `KnowledgeGraphVisualization.jsx` + `.css` | D3.js force-directed knowledge graph — filter by subject/difficulty, zoom/pan, node click handlers |
| `LearningPathwayVisualization.jsx` + `.css` | Learning pathway UI — path selection, lesson status badges (completed / in-progress / locked) |
| `RecommendationsWidget.jsx` + `.css` | Recommendations card widget |
| `VisualizationIntegrationExample.jsx` + `.css` | Combined dashboard page composing all three visualizations |

### Mobile (React Native)

| File | Purpose |
|------|---------|
| `ReactNativeExamples.jsx` | React Native integration — fetch lessons, record quiz results, handle offline state |

---

## Quick Start

### 1. Install Apollo Client

```bash
npm install @apollo/client graphql
```

### 2. Configure the client

```js
// client_examples/apolloClient.js
import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

const httpLink = new HttpLink({ uri: 'http://localhost:8000/graphql' });

const wsLink = new GraphQLWsLink(
  createClient({ url: 'ws://localhost:8000/graphql' })
);

export const client = new ApolloClient({
  link: split(({ query }) => { /* subscription split */ }, wsLink, httpLink),
  cache: new InMemoryCache(),
});
```

### 3. Fetch a lesson

```jsx
// from ApolloUsageExamples.jsx
import { useQuery } from '@apollo/client';
import { GET_LESSON } from './graphqlQueries';

export function LessonDetail({ lessonId }) {
  const { loading, error, data } = useQuery(GET_LESSON, { variables: { lessonId } });
  if (loading) return <p>Loading…</p>;
  return <h1>{data.lesson.title}</h1>;
}
```

### 4. Subscribe to real-time updates

```jsx
import { useSubscription } from '@apollo/client';
import { SUBSCRIBE_TO_PROGRESS_UPDATES } from './graphqlQueries';

export function ProgressListener({ studentId }) {
  const { data } = useSubscription(SUBSCRIBE_TO_PROGRESS_UPDATES, {
    variables: { studentId },
  });
  return <p>Progress: {data?.progressUpdate?.completionPercentage}%</p>;
}
```

### 5. WebSocket (no Apollo)

```js
// client_examples/WebSocketClient.js
import { Wave3WebSocketClient } from './WebSocketClient';

const ws = new Wave3WebSocketClient('student-42', {
  url: 'ws://localhost:8000/ws',
  reconnectInterval: 3000,
});

ws.on('progress_update', (data) => console.log('Progress:', data));
ws.connect();
```

---

## Knowledge Graph Integration

The `KnowledgeGraphVisualization` component takes a `graphData` prop from the
`GET_KNOWLEDGE_GRAPH` GraphQL query and renders a filterable D3 force graph:

```jsx
import { KnowledgeGraphVisualization } from '../client_examples/KnowledgeGraphVisualization';

<KnowledgeGraphVisualization
  graphData={data.knowledgeGraph}
  studentProgress={progressData}
  onNodeClick={(node) => navigate(`/lesson/${node.id}`)}
/>
```

---

## Related Docs

- [API Specifications](../02-backend/api-specs.md)
- [Backend Services Overview](../02-backend/index.md)
- [Akudemy Content API](../service-migrations/index.md)
- [Platform Contracts](../aku-platform-contracts.md)
