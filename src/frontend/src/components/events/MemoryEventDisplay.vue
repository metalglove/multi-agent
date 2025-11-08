<template>
  <div v-if="isMemory" class="memory-event" :class="eventClass">
    <div v-if="event.type === 'memory_retrieval_started'" class="event-content">
      <h4>🔍 Memory Retrieval Started</h4>
      <p v-if="event.task_name"><strong>Task:</strong> {{ event.task_name }}</p>
      <p v-if="event.agent_role"><strong>Agent:</strong> {{ event.agent_role }}</p>
    </div>

    <div v-else-if="event.type === 'memory_retrieval_completed'" class="event-content">
      <h4>✅ Memory Retrieved</h4>
      <p v-if="event.task_name"><strong>Task:</strong> {{ event.task_name }}</p>
      <p v-if="event.retrieval_time_ms"><strong>Time:</strong> {{ event.retrieval_time_ms }}ms</p>
      <details v-if="event.memory_content">
        <summary>Memory Content</summary>
        <pre>{{ JSON.stringify(event.memory_content, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'memory_query_started'" class="event-content">
      <h4>❓ Memory Query Started</h4>
      <p v-if="event.query"><strong>Query:</strong> {{ event.query }}</p>
      <p v-if="event.agent_role"><strong>Agent:</strong> {{ event.agent_role }}</p>
    </div>

    <div v-else-if="event.type === 'memory_query_completed'" class="event-content">
      <h4>✅ Memory Query Completed</h4>
      <p v-if="event.query"><strong>Query:</strong> {{ event.query }}</p>
      <p v-if="event.query_time_ms"><strong>Time:</strong> {{ event.query_time_ms }}ms</p>
      <p v-if="event.results"><strong>Results:</strong> {{ Array.isArray(event.results) ? event.results.length : '?' }} items</p>
    </div>

    <div v-else-if="event.type === 'memory_query_failed'" class="event-content error">
      <h4>❌ Memory Query Failed</h4>
      <p v-if="event.query"><strong>Query:</strong> {{ event.query }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'memory_save_started'" class="event-content">
      <h4>💾 Memory Save Started</h4>
      <p v-if="event.agent_role"><strong>Agent:</strong> {{ event.agent_role }}</p>
      <details v-if="event.value">
        <summary>Value</summary>
        <pre>{{ JSON.stringify(event.value, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'memory_save_completed'" class="event-content">
      <h4>✅ Memory Saved</h4>
      <p v-if="event.save_time_ms"><strong>Time:</strong> {{ event.save_time_ms }}ms</p>
    </div>

    <div v-else-if="event.type === 'memory_save_failed'" class="event-content error">
      <h4>❌ Memory Save Failed</h4>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <p class="timestamp">{{ formatTime(event.timestamp) }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EventType } from '../../types/events'

interface Props {
  event: EventType
}

const props = defineProps<Props>()

const isMemory = computed(() => {
  return [
    'memory_retrieval_started',
    'memory_retrieval_completed',
    'memory_query_started',
    'memory_query_completed',
    'memory_query_failed',
    'memory_save_started',
    'memory_save_completed',
    'memory_save_failed',
  ].includes(props.event.type)
})

const eventClass = computed(() => {
  if (props.event.type?.includes('failed')) return 'error'
  if (props.event.type?.includes('completed')) return 'success'
  return 'info'
})

const formatTime = (timestamp: any): string => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString()
}
</script>

<style scoped>
.memory-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.memory-event.info {
  background-color: #e0f2f1;
  border-left-color: #009688;
}

.memory-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.memory-event.error {
  background-color: #ffebee;
  border-left-color: #f44336;
}

.event-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.event-content p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.event-content strong {
  color: #333;
}

.event-content pre {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.5rem;
  border-radius: 2px;
  overflow-x: auto;
  font-size: 0.85rem;
  max-height: 200px;
}

details {
  margin-top: 0.5rem;
}

summary {
  cursor: pointer;
  color: #666;
  font-weight: 500;
  padding: 0.25rem;
}

.timestamp {
  font-size: 0.8rem;
  color: #999;
  margin-top: 0.5rem;
}

.error {
  color: #c62828;
}
</style>
