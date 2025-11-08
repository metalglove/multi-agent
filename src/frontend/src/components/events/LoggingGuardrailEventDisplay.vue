<template>
  <div v-if="isLogOrGuardrail" class="system-event" :class="eventClass">
    <div v-if="event.type === 'agent_logs_started'" class="event-content">
      <h4>📝 Agent Logs Started</h4>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.task_description"><strong>Task:</strong> {{ event.task_description }}</p>
      <p v-if="event.verbose"><strong>Verbose:</strong> {{ event.verbose }}</p>
    </div>

    <div v-else-if="event.type === 'agent_logs_execution'" class="event-content">
      <h4>📋 Agent Execution Log</h4>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <details v-if="event.formatted_answer">
        <summary>Answer</summary>
        <pre>{{ String(event.formatted_answer).substring(0, 500) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'llm_guardrail_started'" class="event-content">
      <h4>🛡️ Guardrail Started</h4>
      <p v-if="event.agent_role"><strong>Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.task_name"><strong>Task:</strong> {{ event.task_name }}</p>
      <p v-if="event.retry_count"><strong>Attempt:</strong> {{ event.retry_count }}</p>
    </div>

    <div v-else-if="event.type === 'llm_guardrail_completed'" class="event-content">
      <h4>✅ Guardrail Completed</h4>
      <p v-if="event.success" :class="{ 'success': event.success }"><strong>Success:</strong> {{ event.success }}</p>
      <p v-if="event.result"><strong>Result:</strong> {{ event.result }}</p>
      <p v-if="event.error" class="error"><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'llm_guardrail_failed'" class="event-content error">
      <h4>❌ Guardrail Failed</h4>
      <p v-if="event.agent_role"><strong>Agent:</strong> {{ event.agent_role }}</p>
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

const isLogOrGuardrail = computed(() => {
  return [
    'agent_logs_started',
    'agent_logs_execution',
    'llm_guardrail_started',
    'llm_guardrail_completed',
    'llm_guardrail_failed',
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
.system-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.system-event.info {
  background-color: #fce4ec;
  border-left-color: #c2185b;
}

.system-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.system-event.error {
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

.event-content.success {
  color: #2e7d32;
  font-weight: bold;
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
  white-space: pre-wrap;
  word-wrap: break-word;
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
