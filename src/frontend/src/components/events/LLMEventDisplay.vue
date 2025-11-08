<template>
  <div v-if="isLLM" class="llm-event" :class="eventClass">
    <div v-if="event.type === 'llm_call_started'" class="event-content">
      <h4>🤖 LLM Call Started</h4>
      <p><strong>Model:</strong> {{ event.llm_name }}</p>
      <p v-if="event.temperature"><strong>Temperature:</strong> {{ event.temperature }}</p>
      <p v-if="event.messages"><strong>Messages:</strong> {{ Array.isArray(event.messages) ? event.messages.length : '?' }}</p>
    </div>

    <div v-else-if="event.type === 'llm_call_completed'" class="event-content">
      <h4>✅ LLM Call Completed</h4>
      <p><strong>Model:</strong> {{ event.llm_name }}</p>
      <p v-if="event.call_type"><strong>Type:</strong> {{ event.call_type }}</p>
      <details v-if="event.response">
        <summary>Response</summary>
        <pre>{{ JSON.stringify(event.response, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'llm_call_failed'" class="event-content error">
      <h4>❌ LLM Call Failed</h4>
      <p><strong>Model:</strong> {{ event.llm_name }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'llm_stream_chunk'" class="event-content">
      <h4>📡 LLM Stream Chunk</h4>
      <p><strong>Model:</strong> {{ event.llm_name }}</p>
      <p v-if="event.chunk"><strong>Chunk:</strong> {{ String(event.chunk).substring(0, 100) }}...</p>
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

const isLLM = computed(() => {
  return [
    'llm_call_started',
    'llm_call_completed',
    'llm_call_failed',
    'llm_stream_chunk',
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
.llm-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.llm-event.info {
  background-color: #fff3e0;
  border-left-color: #ff9800;
}

.llm-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.llm-event.error {
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
  max-height: 300px;
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
