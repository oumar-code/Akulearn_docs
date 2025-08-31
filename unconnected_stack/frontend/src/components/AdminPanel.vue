<template>
  <div class="card">
    <h2>Admin Panel</h2>
    <p>Manage users, content uploads, and view analytics.</p>
    <div v-if="loading">Loading...</div>
    <div v-if="error" style="color: var(--error)">{{ error }}</div>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.name }} ({{ user.role }})
        <button class="button" @click="removeUser(user.id)">Remove</button>
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  data() {
    return { users: [], loading: false, error: '' };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      try {
        // Replace with actual API call
        this.users = [{ id: 1, name: 'Alice', role: 'teacher' }];
      } catch (e) {
        this.error = 'Failed to load users.';
      } finally {
        this.loading = false;
      }
    },
    async removeUser(id) {
      try {
        // Replace with actual API call
        alert('Removed user ' + id);
      } catch (e) {
        this.error = 'Remove failed.';
      }
    }
  }
}
</script>
<style src="../assets/styles.css"></style>
