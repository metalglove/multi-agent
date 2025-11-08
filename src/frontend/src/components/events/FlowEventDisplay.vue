<template>
  <div v-if="isFlow" class="flow-event" :class="eventClass">
    <div v-if="event.type === 'flow_started'" class="event-content">
      <h4>▶️ Flow Started</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
      <details v-if="event.inputs">
        <summary>Inputs</summary>
        <pre>{{ JSON.stringify(event.inputs, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'flow_created'" class="event-content">
      <h4>✨ Flow Created</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
    </div>

    <div v-else-if="event.type === 'flow_finished'" class="event-content">
      <h4>✅ Flow Finished</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
      <details v-if="event.result">
        <summary>Result</summary>
        <pre>{{ JSON.stringify(event.result, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'flow_plot'" class="event-content">
      <h4>📊 Flow Plot</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
      <details v-if="event.meta">
        <summary>Metadata</summary>
        <pre>{{ JSON.stringify(event.meta, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'method_execution_started'" class="event-content">
      <h4>▶️ Method Execution Started</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
      <p><strong>Method:</strong> {{ event.method_name }}</p>
    </div>

    <div v-else-if="event.type === 'method_execution_finished'" class="event-content">
      <h4>✅ Method Execution Finished</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
      <p><strong>Method:</strong> {{ event.method_name }}</p>
      <details v-if="event.result">
        <summary>Result</summary>
        <pre>{{ JSON.stringify(event.result, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'method_execution_failed'" class="event-content error">
      <h4>❌ Method Execution Failed</h4>
      <p><strong>Flow:</strong> {{ event.flow_name }}</p>
      <p><strong>Method:</strong> {{ event.method_name }}</p>
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

const isFlow = computed(() => {
  return [
    'flow_started',
    'flow_created',
    'flow_finished',
    'flow_plot',
    'method_execution_started',
    'method_execution_finished',
    'method_execution_failed',
  ].includes(props.event.type)
})

const eventClass = computed(() => {
  if (props.event.type?.includes('failed')) return 'error'
  if (props.event.type?.includes('finished') || props.event.type?.includes('created')) return 'success'
  return 'info'
})

const formatTime = (timestamp: any): string => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString()
}
</script>

<style scoped>
.flow-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.flow-event.info {
  background-color: #eceff1;
  border-left-color: #37474f;
}

.flow-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.flow-event.error {
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
