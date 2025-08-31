<template>
  <div>
    <Navbar :role="'student'" />
    <ChatInterface :messages="messages" @send="handleSend" />
  </div>
</template>
<script>
import Navbar from '../components/Navbar.vue';
import ChatInterface from '../components/ChatInterface.vue';
export default {
  components: { Navbar, ChatInterface },
  data() { return { messages: [{ sender: 'AI', text: 'Hello!' }] } },
  methods: { handleSend(msg) { /* handle message */ } }
}
</script>
