<template>
  <div class="solar-status">
    <h2>Solar Power Status</h2>
    <div>Battery Level: {{ status.battery_level }}%</div>
    <div>Panel Output: {{ status.panel_output }}W</div>
    <div>Inverter: {{ status.inverter_status }}</div>
    <div>Charge Controller: {{ status.charge_controller_status }}</div>
    <div v-if="status.battery_level < 20" style="color: red; font-weight: bold;">Warning: Battery Low!</div>
  </div>
</template>
<script>
import { fetchSolarStatus } from '../api/solar';
export default {
  data() {
    return { status: {} };
  },
  mounted() {
    this.loadStatus();
    this.timer = setInterval(this.loadStatus, 60000);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    async loadStatus() {
      try {
        this.status = await fetchSolarStatus();
      } catch (e) {
        this.status = { battery_level: 0, panel_output: 0, inverter_status: 'Error', charge_controller_status: 'Error' };
      }
    }
  }
}
</script>
<style scoped>
.solar-status {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  font-size: 1.5em;
}
</style>
