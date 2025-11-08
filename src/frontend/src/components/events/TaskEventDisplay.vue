<template>
  <div v-if="isTask" class="task-event" :class="eventClass">
    <div v-if="event.type === 'task_started'" class="event-content">
      <h4>▶️ Task Started</h4>
      <p><strong>Task:</strong> {{ event.task_title }}</p>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.task" class="description">{{ event.task }}</p>
    </div>

    <div v-else-if="event.type === 'task_completed'" class="event-content">
      <h4>✅ Task Completed</h4>
      <p><strong>Task:</strong> {{ event.task_title }}</p>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
      <details v-if="event.output">
        <summary>Output</summary>
        <pre>{{ JSON.stringify(event.output, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'task_failed'" class="event-content error">
      <h4>❌ Task Failed</h4>
      <p><strong>Task:</strong> {{ event.task_title }}</p>
      <p><strong>Agent:</strong> {{ event.agent_role }}</p>
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

const isTask = computed(() => {
  return ['task_started', 'task_completed', 'task_failed'].includes(props.event.type)
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
.task-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.task-event.info {
  background-color: #f3e5f5;
  border-left-color: #9c27b0;
}

.task-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.task-event.error {
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

.event-content .description {
  font-style: italic;
  color: #666;
  margin-top: 0.5rem;
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
