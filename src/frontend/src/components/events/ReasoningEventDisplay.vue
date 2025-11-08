<template>
  <div v-if="isReasoning" class="reasoning-event" :class="eventClass">
    <div v-if="event.type === 'agent_reasoning_started'" class="event-content">
      <h4>🧠 Agent Reasoning Started</h4>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.task_name"><strong>Task:</strong> {{ event.task_name }}</p>
      <p v-if="event.attempt"><strong>Attempt:</strong> {{ event.attempt }}</p>
    </div>

    <div v-else-if="event.type === 'agent_reasoning_completed'" class="event-content">
      <h4>✅ Agent Reasoning Completed</h4>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.task_name"><strong>Task:</strong> {{ event.task_name }}</p>
      <p v-if="event.ready" :class="{ 'ready': event.ready }"><strong>Ready:</strong> {{ event.ready }}</p>
      <details v-if="event.plan">
        <summary>Plan</summary>
        <pre>{{ event.plan }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'agent_reasoning_failed'" class="event-content error">
      <h4>❌ Agent Reasoning Failed</h4>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.task_name"><strong>Task:</strong> {{ event.task_name }}</p>
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

const isReasoning = computed(() => {
  return [
    'agent_reasoning_started',
    'agent_reasoning_completed',
    'agent_reasoning_failed',
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
.reasoning-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.reasoning-event.info {
  background-color: #fce4ec;
  border-left-color: #e91e63;
}

.reasoning-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.reasoning-event.error {
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

.event-content .ready {
  color: #4caf50;
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
  max-height: 300px;
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
