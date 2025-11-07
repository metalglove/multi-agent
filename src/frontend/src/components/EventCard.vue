<template>
  <div class="event-card" :class="eventClass">
    <div class="event-header">
      <span class="event-icon">{{ eventIcon }}</span>
      <div class="event-title">
        <h3>{{ eventLabel }}</h3>
        <span class="event-time">{{ formatTime(event.timestamp) }}</span>
      </div>
    </div>
    <div class="event-body">
      <div v-if="event.data?.agent_role" class="event-detail">
        <span class="label">Agent:</span>
        <span class="value">{{ event.data.agent_role }}</span>
      </div>
      <div v-if="event.data?.agent_name" class="event-detail">
        <span class="label">Name:</span>
        <span class="value">{{ event.data.agent_name }}</span>
      </div>
      <div v-if="event.data?.task_title" class="event-detail">
        <span class="label">Task:</span>
        <span class="value">{{ event.data.task_title }}</span>
      </div>
      <div v-if="event.data?.reasoning_plan" class="event-detail">
        <span class="label">Reasoning:</span>
        <p class="value-long">{{ event.data.reasoning_plan }}</p>
      </div>
      <div v-if="event.data?.task_description" class="event-detail">
        <span class="label">Description:</span>
        <p class="value-long">{{ event.data.task_description }}</p>
      </div>
      <div v-if="event.data?.task_output" class="event-detail">
        <span class="label">Output:</span>
        <p class="value-long">{{ event.data.task_output }}</p>
      </div>
      <div v-if="event.data?.error" class="event-detail">
        <span class="label">Error:</span>
        <p class="value-error">{{ event.data.error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { CrewAIEvent } from '../types/events'

interface Props {
  event: CrewAIEvent
}

const props = defineProps<Props>()

const eventClass = computed(() => {
  return {
    'type-agent': props.event.type.includes('agent') || props.event.type.includes('reasoning'),
    'type-task': props.event.type.includes('task'),
    'type-error': props.event.type.includes('failed'),
    'type-completed': props.event.type.includes('completed'),
  }
})

const eventIcon = computed(() => {
  const type = props.event.type
  if (type.includes('reasoning_started')) return '🔄'
  if (type.includes('reasoning_completed')) return '✅'
  if (type.includes('reasoning_failed')) return '❌'
  if (type.includes('task_started')) return '🚀'
  if (type.includes('task_completed')) return '✨'
  if (type.includes('task_failed')) return '💥'
  return '📌'
})

const eventLabel = computed(() => {
  const type = props.event.type
  const labels: Record<string, string> = {
    'agent_reasoning_started': 'Agent Reasoning Started',
    'agent_reasoning_completed': 'Agent Reasoning Completed',
    'agent_reasoning_failed': 'Agent Reasoning Failed',
    'task_started': 'Task Started',
    'task_completed': 'Task Completed',
    'task_failed': 'Task Failed',
  }
  return labels[type] || type
})

function formatTime(timestamp?: string): string {
  if (!timestamp) return 'Just now'
  try {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit',
      hour12: false 
    })
  } catch {
    return 'Just now'
  }
}
</script>

<style scoped>
.event-card {
  background: white;
  border-left: 4px solid #e0e0e0;
  border-radius: 6px;
  padding: 1rem;
  transition: all 0.2s ease;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.event-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.event-card.type-agent {
  border-left-color: #667eea;
}

.event-card.type-task {
  border-left-color: #4caf50;
}

.event-card.type-error {
  border-left-color: #f44336;
  background: #ffebee;
}

.event-card.type-completed {
  border-left-color: #4caf50;
}

.event-header {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.event-icon {
  font-size: 1.5rem;
  line-height: 1.5;
}

.event-title {
  flex: 1;
}

.event-title h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
}

.event-time {
  font-size: 0.75rem;
  color: #999;
  display: block;
  margin-top: 0.25rem;
}

.event-body {
  margin-left: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.event-detail {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
  font-size: 0.875rem;
}

.label {
  font-weight: 600;
  color: #666;
  min-width: 70px;
}

.value {
  color: #333;
  flex: 1;
  word-break: break-word;
}

.value-long {
  margin: 0;
  color: #555;
  font-size: 0.8rem;
  line-height: 1.4;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 4px;
  max-height: 100px;
  overflow-y: auto;
}

.value-error {
  margin: 0;
  color: #d32f2f;
  font-weight: 500;
  font-size: 0.8rem;
  padding: 0.5rem;
  background: #ffebee;
  border-radius: 4px;
}
</style>
