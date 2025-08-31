<template>
  <div class="card">
    <h2>Login</h2>
    <input class="input" v-model="username" placeholder="Username" />
    <input class="input" v-model="password" type="password" placeholder="Password" />
    <button class="button" @click="login" :disabled="loading">Login</button>
    <p v-if="error" style="color: var(--error)">{{ error }}</p>
    <p v-if="loading">Loading...</p>
  </div>
</template>
<script>
import { login } from '../api';
export default {
  data() { return { username: '', password: '', error: '', loading: false }; },
  methods: {
    async login() {
      this.loading = true;

      <template>
        <div>
          <h2>Login</h2>
          <form @submit.prevent="login">
            <input v-model="username" placeholder="Username" />
            <input v-model="password" type="password" placeholder="Password" />
            <button type="submit">Login</button>
          </form>
          <div v-if="error" style="color: red">{{ error }}</div>
          <div v-if="loading">Logging in...</div>
        </div>
      </template>
      <script>
      import { store } from '../store';
      import { loginUser } from '../api';
      export default {
        data() {
          return { username: '', password: '', error: '', loading: false };
        },
        methods: {
          async login() {
            this.loading = true;
            this.error = '';
            try {
              const result = await loginUser(this.username, this.password);
              localStorage.setItem('token', result.token);
              store.role = result.role;
              this.$router.push('/dashboard');
            } catch (e) {
              this.error = 'Invalid credentials';
            } finally {
              this.loading = false;
            }
          }
        }
      }
      </script>
