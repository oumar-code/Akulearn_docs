<template>
  <nav class="navbar">
    <span>Akulearn Hub</span>
    <div>
      <button class="button" v-if="role === 'student'">Dashboard</button>
      <button class="button secondary" v-if="role === 'teacher'">Review</button>
      <button class="button" v-if="role === 'admin'">Admin</button>
    </div>
  </nav>
</template>
<script>
export default {
  props: ['role']
}
</script>
<style src="../assets/styles.css"></style>
