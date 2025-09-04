<template>
  <div class="hardware-status">
    <h2>Hardware Status</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div style="margin-bottom: 8px;">Last Update: {{ lastUpdate }}</div>
      <div>
        <span :style="{color: status.voltage < 11.5 ? 'red' : 'green'}">🔋</span>
        Battery Voltage: {{ status.voltage }} V
      </div>
      <div>
        <span :style="{color: status.current > 8 ? 'orange' : 'green'}">⚡</span>
        Current: {{ status.current }} A
      </div>
      <div>
        <span :style="{color: status.temperature > 40 ? 'orange' : 'green'}">🌡️</span>
        Temperature: {{ status.temperature }} °C
      </div>
      <div>
        <span :style="{color: solar.panel_output < 20 ? 'gray' : 'green'}">☀️</span>
        Solar Panel Output: {{ solar.panel_output }} W
      </div>
      <div>
        <span :style="{color: solar.inverter_status !== 'OK' ? 'red' : 'green'}">🔌</span>
        Inverter Status: {{ solar.inverter_status }}
      </div>
      <div>
        <span :style="{color: solar.charge_controller_status !== 'Charging' ? 'orange' : 'green'}">🔋</span>
        Charge Controller: {{ solar.charge_controller_status }}
      </div>
      <div v-if="status.voltage < 11.5" style="color: red; font-weight: bold;">Warning: Low Battery!</div>
      <div v-if="solar.inverter_status !== 'OK'" style="color: red; font-weight: bold;">Alert: Inverter Fault!</div>
      <div v-if="solar.charge_controller_status !== 'Charging'" style="color: orange; font-weight: bold;">Alert: Charge Controller Issue!</div>
    </div>
  </div>
</template>
<script>
import { fetchSolarStatus } from '../api/solar';
export default {
  data() {
    return {
      status: {},
      solar: {},
      loading: true,
      lastUpdate: ''
    };
  },
  mounted() {
    this.loadStatus();
    this.timer = setInterval(this.loadStatus, 15000); // Poll every 15 seconds for regular status
    this.setupWebSocket();
  },
  beforeDestroy() {
    clearInterval(this.timer);
    if (this.ws) {
      this.ws.close();
    }
  },
  methods: {
    setupWebSocket() {
      // Connect to backend WebSocket for instant hardware updates
      this.ws = new WebSocket('ws://localhost:8000/ws/hardware');
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.lastUpdate = new Date().toLocaleTimeString();
        if (data.type === 'sensor') {
          this.status = data.payload;
        } else if (data.type === 'solar') {
          this.solar = data.payload;
        }
      };
      this.ws.onerror = () => {
        // Fallback to polling if WebSocket fails
      };
    },
    async loadStatus() {
      this.loading = true;
      try {
        // Fetch sensor status from backend
        const sensorRes = await fetch('/pcb/status');
        this.status = await sensorRes.json();
        // Fetch solar status from backend
        this.solar = await fetchSolarStatus();
        this.lastUpdate = new Date().toLocaleTimeString();
      } catch (e) {
        this.status = { voltage: 0, current: 0, temperature: 0 };
        this.solar = { panel_output: 0, inverter_status: 'Error', charge_controller_status: 'Error' };
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
<style scoped>
.hardware-status {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  font-size: 1.2em;
}
</style>
