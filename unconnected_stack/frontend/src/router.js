
import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from './views/Dashboard.vue';
import Quiz from './views/Quiz.vue';
import Chat from './views/Chat.vue';
import Login from './views/Login.vue';
import { store } from './store';

const routes = [
  { path: '/', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/quiz', component: Quiz, meta: { requiresAuth: true } },
  { path: '/chat', component: Chat, meta: { requiresAuth: true } },
  { path: '/login', component: Login }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

export default router;
