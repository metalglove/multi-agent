<template>
  <div v-if="isToolUsage" class="tool-event" :class="eventClass">
    <div v-if="event.type === 'tool_usage_started'" class="event-content">
      <h4>🔧 Tool Usage Started</h4>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
      <p v-if="event.agent_role"><strong>Agent:</strong> {{ event.agent_role }}</p>
      <details v-if="event.tool_args">
        <summary>Arguments</summary>
        <pre>{{ JSON.stringify(event.tool_args, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'tool_usage_finished'" class="event-content">
      <h4>✅ Tool Usage Finished</h4>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
      <p v-if="event.from_cache"><strong>Cached:</strong> {{ event.from_cache }}</p>
      <details v-if="event.output">
        <summary>Output</summary>
        <pre>{{ JSON.stringify(event.output, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'tool_usage_error'" class="event-content error">
      <h4>❌ Tool Usage Error</h4>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'tool_selection_error'" class="event-content error">
      <h4>❌ Tool Selection Error</h4>
      <p v-if="event.tool_name"><strong>Tool:</strong> {{ event.tool_name }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'tool_execution_error'" class="event-content error">
      <h4>❌ Tool Execution Error</h4>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
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

const isToolUsage = computed(() => {
  return [
    'tool_usage_started',
    'tool_usage_finished',
    'tool_usage_error',
    'tool_selection_error',
    'tool_execution_error',
  ].includes(props.event.type)
})

const eventClass = computed(() => {
  if (props.event.type?.includes('error')) return 'error'
  if (props.event.type?.includes('finished')) return 'success'
  return 'info'
})

const formatTime = (timestamp: any): string => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString()
}
</script>

<style scoped>
.tool-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.tool-event.info {
  background-color: #ede7f6;
  border-left-color: #673ab7;
}

.tool-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.tool-event.error {
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
  max-height: 250px;
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
