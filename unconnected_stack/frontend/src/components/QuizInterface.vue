<template>
  <div class="card">
    <h2>Quiz</h2>
    <div v-for="(question, idx) in questions" :key="idx">
      <p>{{ question.text }}</p>
      <input class="input" v-model="answers[idx]" :placeholder="'Your answer'" />
    </div>
    <button class="button" @click="submit">Submit</button>
  </div>
</template>
<script>
export default {
  props: ['questions'],
  data() {
    return { answers: [] }
  },
  methods: {
    submit() {
      this.$emit('submit', this.answers)
    }
  }
}
</script>
<style src="../assets/styles.css"></style>
