/**
 * Wave 3 Apollo GraphQL Integration
 * Complete setup for GraphQL client with Wave 3 backend
 */

import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

// Configuration
const config = {
  graphqlUrl: process.env.REACT_APP_GRAPHQL_URL || 'http://localhost:8000/graphql',
  wsUrl: process.env.REACT_APP_WS_URL || 'ws://localhost:8000/graphql',
};

/**
 * Create HTTP Link for queries and mutations
 */
const httpLink = new HttpLink({
  uri: config.graphqlUrl,
  headers: {
    authorization: localStorage.getItem('token') 
      ? `Bearer ${localStorage.getItem('token')}` 
      : '',
  },
});

/**
 * Create WebSocket Link for subscriptions (optional)
 */
const wsLink = new GraphQLWsLink(
  createClient({
    url: config.wsUrl,
    connectionParams: () => ({
      authorization: localStorage.getItem('token')
        ? `Bearer ${localStorage.getItem('token')}`
        : '',
    }),
  })
);

/**
 * Split traffic between HTTP and WebSocket
 */
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

/**
 * Create Apollo Client instance
 */
export const apolloClient = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          recommendations: {
            merge(existing = [], incoming) {
              return incoming;
            },
          },
          leaderboard: {
            merge(existing = [], incoming) {
              return incoming;
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
      errorPolicy: 'all',
    },
    query: {
      fetchPolicy: 'network-only',
      errorPolicy: 'all',
    },
    mutate: {
      errorPolicy: 'all',
    },
  },
});

/**
 * Update auth token
 */
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('token', token);
  } else {
    localStorage.removeItem('token');
  }
  // Reset Apollo cache to refetch with new token
  apolloClient.resetStore();
};

/**
 * Clear auth token
 */
export const clearAuthToken = () => {
  localStorage.removeItem('token');
  apolloClient.clearStore();
};

export default apolloClient;
