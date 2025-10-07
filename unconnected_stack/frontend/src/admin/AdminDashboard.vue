<template>
  <div class="admin-dashboard">
    <h2>Aku Admin Portal</h2>
    <section>
      <h3>Node Status</h3>
      <button @click="fetchNodes">Refresh</button>
      <ul>
        <li v-for="node in nodes" :key="node.id">{{ node.id }} - {{ node.status }} (Last seen: {{ node.last_seen }})</li>
      </ul>
    </section>
    <section>
      <h3>Users</h3>
      <button @click="fetchUsers">Refresh</button>
      <ul>
        <li v-for="user in users" :key="user.id">{{ user.name }} - {{ user.role }}</li>
      </ul>
    </section>
    <section>
      <h3>Content</h3>
      <button @click="fetchContent">Refresh</button>
      <ul>
        <li v-for="item in content" :key="item.id">{{ item.title }} (v{{ item.version }}) - {{ item.type }}</li>
      </ul>
    </section>
    <section>
      <h3>OTA Update</h3>
      <input v-model="otaNodeId" placeholder="Node ID" />
      <input v-model="otaVersion" placeholder="Version" />
      <button @click="triggerOTA">Trigger OTA Update</button>
      <p v-if="otaMessage">{{ otaMessage }}</p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      nodes: [],
      users: [],
      content: [],
      otaNodeId: '',
      otaVersion: '',
      otaMessage: ''
    };
  },
  methods: {
    async fetchNodes() {
      const response = await fetch('/admin_portal_service/nodes', { headers: { Authorization: 'Bearer admin-token' } });
      this.nodes = await response.json();
    },
    async fetchUsers() {
      const response = await fetch('/admin_portal_service/users', { headers: { Authorization: 'Bearer admin-token' } });
      this.users = await response.json();
    },
    async fetchContent() {
      const response = await fetch('/admin_portal_service/content', { headers: { Authorization: 'Bearer admin-token' } });
      this.content = await response.json();
    },
    async triggerOTA() {
      const response = await fetch(`/admin_portal_service/ota/update?node_id=${this.otaNodeId}&version=${this.otaVersion}`, {
        method: 'POST',
        headers: { Authorization: 'Bearer admin-token' }
      });
      const result = await response.json();
      this.otaMessage = result.message;
    }
  },
  mounted() {
    this.fetchNodes();
    this.fetchUsers();
    this.fetchContent();
  }
};
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  background: #f9f9f9;
  border-radius: 8px;
}
section {
  margin-bottom: 2rem;
}
</style>
