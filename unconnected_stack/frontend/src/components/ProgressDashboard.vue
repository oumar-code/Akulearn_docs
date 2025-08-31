<template>
  <div class="card">
    <h2>Progress Tracker</h2>
    <div class="progress-bar">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>
    <p>{{ progress }}% completed</p>
  </div>
</template>
<script>
export default {
  props: ['progress']
}
</script>
<style src="../assets/styles.css"></style>
