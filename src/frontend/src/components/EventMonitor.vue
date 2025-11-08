<template>
  <div class="event-monitor">
    <!-- Main Tabs -->
    <div class="main-tabs">
      <button 
        v-for="tab in mainTabs" 
        :key="tab.id"
        class="main-tab"
        :class="{ active: activeMainTab === tab.id }"
        @click="activeMainTab = tab.id"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
      </button>
    </div>

    <!-- Events View -->
    <div v-if="activeMainTab === 'events'" class="view-container">
      <div class="controls">
        <div class="filter-tabs">
          <button 
            v-for="tab in eventGroupTabs" 
            :key="tab.id"
            class="filter-tab"
            :class="{ active: activeEventGroup === tab.id }"
            @click="activeEventGroup = tab.id"
          >
            <span class="tab-icon">{{ tab.icon }}</span>
            <span class="tab-label">{{ tab.label }}</span>
            <span class="tab-count">{{ tab.count }}</span>
          </button>
        </div>
        <button class="btn-clear" @click="store.clearEvents">
          🗑️ Clear
        </button>
      </div>

      <div class="events-container">
        <div v-if="filteredEvents.length === 0" class="empty-state">
          <p>{{ emptyMessage }}</p>
        </div>
        <div v-else class="events-list">
          <EventCard 
            v-for="event in filteredEvents" 
            :key="event.id"
            :event="event"
          />
        </div>
      </div>
    </div>

    <!-- Agent Chat View -->
    <AgentChat v-else-if="activeMainTab === 'chat'" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useEventStore } from '../stores/eventStore'
import EventCard from './EventCard.vue'
import AgentChat from './AgentChat.vue'
import type { CrewAIEvent } from '../types/events'

const store = useEventStore()
const activeMainTab = ref<'events' | 'chat'>('events')
const activeEventGroup = ref<string>('all')

const mainTabs = [
  { id: 'events' as const, label: 'Events', icon: '📊' },
  { id: 'chat' as const, label: 'Agent Chat', icon: '💬' },
]

type EventGroup = {
  id: string
  label: string
  icon: string
  filter: (event: CrewAIEvent) => boolean
}

const eventGroups: EventGroup[] = [
  {
    id: 'all',
    label: 'All Events',
    icon: '📊',
    filter: () => true,
  },
  {
    id: 'crew',
    label: 'Crew',
    icon: '👥',
    filter: (e) => e.type.includes('crew'),
  },
  {
    id: 'task',
    label: 'Tasks',
    icon: '✅',
    filter: (e) => e.type.includes('task'),
  },
  {
    id: 'reasoning',
    label: 'Reasoning',
    icon: '🧠',
    filter: (e) => e.type.includes('reasoning'),
  },
  {
    id: 'memory',
    label: 'Memory',
    icon: '💾',
    filter: (e) => e.type.includes('memory'),
  },
  {
    id: 'llm',
    label: 'LLM',
    icon: '🤖',
    filter: (e) => e.type.includes('llm'),
  },
  {
    id: 'tool',
    label: 'Tools',
    icon: '🔧',
    filter: (e) => e.type.includes('tool'),
  },
  {
    id: 'knowledge',
    label: 'Knowledge',
    icon: '📚',
    filter: (e) => e.type.includes('knowledge'),
  },
  {
    id: 'flow',
    label: 'Flow',
    icon: '🔀',
    filter: (e) => e.type.includes('flow'),
  },
  {
    id: 'mcp',
    label: 'MCP',
    icon: '🔌',
    filter: (e) => e.type.includes('mcp'),
  },
  {
    id: 'a2a',
    label: 'Agent-to-Agent',
    icon: '🔗',
    filter: (e) => e.type.includes('a2a'),
  },
  {
    id: 'errors',
    label: 'Errors',
    icon: '❌',
    filter: (e) => e.type.includes('failed') || e.type.includes('error'),
  },
]

const eventGroupTabs = computed(() => {
  return eventGroups.map(group => ({
    ...group,
    count: store.events.filter(group.filter).length,
  }))
})

const filteredEvents = computed(() => {
  const selectedGroup = eventGroups.find(g => g.id === activeEventGroup.value)
  if (!selectedGroup) return []
  return store.events.filter(selectedGroup.filter)
})

const emptyMessage = computed(() => {
  if (store.events.length === 0) return 'Waiting for events...'
  return `No ${activeEventGroup.value} events yet`
})
</script>

<style scoped>
.event-monitor {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 1rem;
}

.main-tabs {
  display: flex;
  gap: 0.5rem;
  background: white;
  padding: 0.75rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.main-tab {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.95rem;
}

.main-tab:hover {
  border-color: #667eea;
  color: #667eea;
}

.main-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.tab-icon {
  font-size: 1.2rem;
}

.view-container {
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
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  flex: 1;
}

.filter-tab {
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
  font-size: 0.85rem;
}

.filter-tab:hover {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.filter-tab.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  min-width: 24px;
  height: 20px;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 0 0.3rem;
}

.filter-tab.active .tab-count {
  background: rgba(255, 255, 255, 0.3);
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
  white-space: nowrap;
}

.btn-clear:hover {
  background: #d32f2f;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3);
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
