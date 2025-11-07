<template>
  <div class="app">
    <header class="header">
      <h1>🤖 CrewAI Event Monitor</h1>
      <div class="status" :class="connectionStatus">
        {{ connectionStatus === 'connected' ? '✓ Connected' : '✗ Disconnected' }}
      </div>
    </header>

    <main class="container">
      <EventMonitor />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import EventMonitor from './components/EventMonitor.vue'
import { useEventStore } from './stores/eventStore'

const store = useEventStore()

const connectionStatus = computed(() => store.connectionStatus)

onMounted(() => {
  store.connectToServer()
})
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.header {
  background: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.status {
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.status.connected {
  background: rgba(76, 175, 80, 0.3);
  color: #4caf50;
}

.status.disconnected {
  background: rgba(244, 67, 54, 0.3);
  color: #f44336;
}

.container {
  flex: 1;
  overflow: auto;
  padding: 1.5rem;
}
</style>
