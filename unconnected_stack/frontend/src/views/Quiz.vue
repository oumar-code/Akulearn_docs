<template>
  <div>
    <Navbar :role="'student'" />
    <QuizInterface :questions="questions" @submit="handleSubmit" />
  </div>
</template>
<script>
import Navbar from '../components/Navbar.vue';
import QuizInterface from '../components/QuizInterface.vue';
export default {
  components: { Navbar, QuizInterface },
  data() { return { questions: [{ text: 'What is 2+2?' }] } },
  methods: { handleSubmit(answers) { /* handle answers */ } }
}
</script>
