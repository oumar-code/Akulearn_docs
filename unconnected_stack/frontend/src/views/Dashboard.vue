
<template>
  <div>
    <Navbar :role="store.role" />
    <div v-if="store.role === 'student'">
      <ProgressDashboard :progress="progress" />
    </div>
    <div v-else-if="store.role === 'teacher'">
      <ReviewPanel />
    </div>
    <div v-else-if="store.role === 'admin'">
      <AdminPanel />
    </div>
    <div v-if="error" style="color: var(--error)">{{ error }}</div>
    <div v-if="loading">Loading...</div>
  </div>
</template>
<script>
import { store } from '../store';
import Navbar from '../components/Navbar.vue';
import ProgressDashboard from '../components/ProgressDashboard.vue';
import ReviewPanel from '../components/ReviewPanel.vue';
import AdminPanel from '../components/AdminPanel.vue';
import { fetchProgress } from '../api';
export default {
  components: { Navbar, ProgressDashboard, ReviewPanel, AdminPanel },
  data() {
    return { store, progress: 0, error: '', loading: false };
  },
  mounted() {
    this.loadProgress();
  },
  methods: {
    async loadProgress() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const data = await fetchProgress('student1', token);
        this.progress = data.progress;
      } catch (e) {
        this.error = 'Unable to load progress.';
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
