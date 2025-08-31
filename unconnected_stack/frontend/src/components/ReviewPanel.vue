<template>
  <div class="card">
    <h2>Review Panel</h2>
    <p>Review and approve submitted content here.</p>
    <div v-if="loading">Loading...</div>
    <div v-if="error" style="color: var(--error)">{{ error }}</div>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.title }}
        <button class="button" @click="approve(item.id)">Approve</button>
        <button class="button secondary" @click="reject(item.id)">Reject</button>
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  data() {
    return { items: [], loading: false, error: '' };
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      this.loading = true;
      try {
        // Replace with actual API call
        this.items = [{ id: 1, title: 'Math Video' }];
      } catch (e) {
        this.error = 'Failed to load items.';
      } finally {
        this.loading = false;
      }
    },
    async approve(id) {
      try {
        // Replace with actual API call
        alert('Approved ' + id);
      } catch (e) {
        this.error = 'Approval failed.';
      }
    },
    async reject(id) {
      try {
        // Replace with actual API call
        alert('Rejected ' + id);
      } catch (e) {
        this.error = 'Rejection failed.';
      }
    }
  }
}
</script>
<style src="../assets/styles.css"></style>
