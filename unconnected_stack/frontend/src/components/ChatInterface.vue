<template>
  <div class="chat">
    <h2>AI Tutor Chat</h2>
    <div v-for="(msg, idx) in messages" :key="idx">
      <div><strong>{{ msg.sender }}:</strong> {{ msg.text }}</div>
    </div>
    <input class="input" v-model="input" placeholder="Type your message..." @keyup.enter="send" />
    <button class="button" @click="send">Send</button>
  </div>
</template>
<script>
export default {
  props: ['messages'],
  data() {
    return { input: '' }
  },
  methods: {
    send() {
      if (this.input.trim()) {
        this.$emit('send', this.input)
        this.input = ''
      }
    }
  }
}
</script>
<style src="../assets/styles.css"></style>
