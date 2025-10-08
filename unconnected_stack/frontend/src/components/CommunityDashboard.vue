<template>
  <div class="community-dashboard">
    <h2>Marketplace & Community</h2>
    <section>
      <h3>Marketplace</h3>
      <ul>
        <li v-for="item in marketplace" :key="item.id">
          {{ item.title }} - {{ item.price }} AKU
          <button @click="buyItem(item.id)">Buy</button>
        </li>
      </ul>
    </section>
    <section>
      <h3>Community Compensation</h3>
      <ul>
        <li v-for="user in community" :key="user.id">
          {{ user.name }} - {{ user.role }} - {{ user.aku }} AKU
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
export default {
  name: 'CommunityDashboard',
  data() {
    return {
      marketplace: [],
      community: []
    };
  },
  methods: {
    async fetchMarketplace() {
      const response = await fetch('/marketplace_service/items', { headers: { Authorization: 'Bearer admin-token' } });
      this.marketplace = await response.json();
    },
    async fetchCommunity() {
      const response = await fetch('/community_service/compensation', { headers: { Authorization: 'Bearer admin-token' } });
      this.community = await response.json();
    },
    async buyItem(itemId) {
      const response = await fetch(`/marketplace_service/buy/${itemId}`, {
        method: 'POST',
        headers: { Authorization: 'Bearer admin-token' }
      });
      const result = await response.json();
      alert(result.message);
    }
  },
  mounted() {
    this.fetchMarketplace();
    this.fetchCommunity();
  }
};
</script>

<style scoped>
.community-dashboard {
  padding: 2rem;
  background: #f4f8fb;
  border-radius: 8px;
}
section {
  margin-bottom: 2rem;
}
</style>
