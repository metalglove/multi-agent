<template>
  <div v-if="isMCP" class="mcp-event" :class="eventClass">
    <div v-if="event.type === 'mcp_connection_started'" class="event-content">
      <h4>🔌 MCP Connection Started</h4>
      <p><strong>Server:</strong> {{ event.server_name }}</p>
      <p v-if="event.server_url"><strong>URL:</strong> {{ event.server_url }}</p>
      <p v-if="event.transport_type"><strong>Transport:</strong> {{ event.transport_type }}</p>
      <p v-if="event.is_reconnect"><strong>Reconnect:</strong> {{ event.is_reconnect }}</p>
    </div>

    <div v-else-if="event.type === 'mcp_connection_completed'" class="event-content">
      <h4>✅ MCP Connected</h4>
      <p><strong>Server:</strong> {{ event.server_name }}</p>
      <p v-if="event.connection_duration_ms"><strong>Duration:</strong> {{ event.connection_duration_ms }}ms</p>
    </div>

    <div v-else-if="event.type === 'mcp_connection_failed'" class="event-content error">
      <h4>❌ MCP Connection Failed</h4>
      <p><strong>Server:</strong> {{ event.server_name }}</p>
      <p v-if="event.error_type"><strong>Error Type:</strong> {{ event.error_type }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'mcp_tool_execution_started'" class="event-content">
      <h4>🔧 MCP Tool Started</h4>
      <p><strong>Server:</strong> {{ event.server_name }}</p>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
      <details v-if="event.tool_args">
        <summary>Arguments</summary>
        <pre>{{ JSON.stringify(event.tool_args, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'mcp_tool_execution_completed'" class="event-content">
      <h4>✅ MCP Tool Completed</h4>
      <p><strong>Server:</strong> {{ event.server_name }}</p>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
      <p v-if="event.execution_duration_ms"><strong>Duration:</strong> {{ event.execution_duration_ms }}ms</p>
      <details v-if="event.result">
        <summary>Result</summary>
        <pre>{{ JSON.stringify(event.result, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'mcp_tool_execution_failed'" class="event-content error">
      <h4>❌ MCP Tool Failed</h4>
      <p><strong>Server:</strong> {{ event.server_name }}</p>
      <p><strong>Tool:</strong> {{ event.tool_name }}</p>
      <p v-if="event.error_type"><strong>Error Type:</strong> {{ event.error_type }}</p>
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

const isMCP = computed(() => {
  return [
    'mcp_connection_started',
    'mcp_connection_completed',
    'mcp_connection_failed',
    'mcp_tool_execution_started',
    'mcp_tool_execution_completed',
    'mcp_tool_execution_failed',
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
.mcp-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.mcp-event.info {
  background-color: #f3e5f5;
  border-left-color: #7b1fa2;
}

.mcp-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.mcp-event.error {
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
