<template>
  <div class="event-monitor">
    <div class="controls">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          class="tab"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          <span class="tab-label">{{ tab.label }}</span>
          <span class="tab-count">{{ tab.count }}</span>
        </button>
      </div>
      <button class="btn-clear" @click="store.clearEvents">
        🗑️ Clear
      </button>
    </div>

    <div class="events-container">
      <div v-if="displayedEvents.length === 0" class="empty-state">
        <p>Waiting for events...</p>
      </div>
      <div v-else class="events-list">
        <EventCard 
          v-for="event in displayedEvents" 
          :key="event.id"
          :event="event"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useEventStore } from '../stores/eventStore'
import EventCard from './EventCard.vue'

const store = useEventStore()
const activeTab = ref<'all' | 'agents' | 'tasks' | 'errors'>('all')

type TabId = 'all' | 'agents' | 'tasks' | 'errors'
type Tab = { id: TabId; label: string; count: number }

const tabs = computed<Tab[]>(() => [
  { id: 'all', label: 'All Events', count: store.events.length },
  { id: 'agents', label: 'Agent Activity', count: store.agentEvents.length },
  { id: 'tasks', label: 'Tasks', count: store.taskEvents.length },
  { id: 'errors', label: 'Errors', count: store.errorEvents.length },
])

const displayedEvents = computed(() => {
  switch (activeTab.value) {
    case 'agents':
      return store.agentEvents
    case 'tasks':
      return store.taskEvents
    case 'errors':
      return store.errorEvents
    default:
      return store.events
  }
})
</script>

<style scoped>
.event-monitor {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 1rem;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tab {
  padding: 0.5rem 1rem;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab:hover {
  border-color: #667eea;
  color: #667eea;
}

.tab.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  min-width: 24px;
  height: 24px;
  font-size: 0.75rem;
  font-weight: 600;
}

.btn-clear {
  padding: 0.5rem 1rem;
  background: #f44336;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-clear:hover {
  background: #d32f2f;
  transform: translateY(-2px);
}

.events-container {
  flex: 1;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.5rem;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
</style>
