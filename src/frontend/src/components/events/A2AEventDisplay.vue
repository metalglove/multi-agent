<template>
  <div v-if="isA2A" class="a2a-event" :class="eventClass">
    <div v-if="event.type === 'a2a_delegation_started'" class="event-content">
      <h4>🔀 A2A Delegation Started</h4>
      <p><strong>From Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.endpoint"><strong>Endpoint:</strong> {{ event.endpoint }}</p>
      <p v-if="event.is_multiturn"><strong>Multiturn:</strong> {{ event.is_multiturn }}</p>
    </div>

    <div v-else-if="event.type === 'a2a_delegation_completed'" class="event-content">
      <h4>✅ A2A Delegation Completed</h4>
      <p><strong>Status:</strong> {{ event.status }}</p>
      <p v-if="event.result"><strong>Result:</strong> {{ event.result }}</p>
    </div>

    <div v-else-if="event.type === 'a2a_conversation_started'" class="event-content">
      <h4>💬 A2A Conversation Started</h4>
      <p><strong>From Agent:</strong> {{ event.agent_role }}</p>
      <p v-if="event.a2a_agent_name"><strong>A2A Agent:</strong> {{ event.a2a_agent_name }}</p>
    </div>

    <div v-else-if="event.type === 'a2a_message_sent'" class="event-content">
      <h4>📤 Message Sent</h4>
      <p><strong>From:</strong> {{ event.agent_role }}</p>
      <p v-if="event.turn_number"><strong>Turn:</strong> {{ event.turn_number }}</p>
      <p v-if="event.message"><strong>Message:</strong> {{ String(event.message).substring(0, 100) }}...</p>
    </div>

    <div v-else-if="event.type === 'a2a_response_received'" class="event-content">
      <h4>📥 Response Received</h4>
      <p><strong>Status:</strong> {{ event.status }}</p>
      <p v-if="event.turn_number"><strong>Turn:</strong> {{ event.turn_number }}</p>
      <p v-if="event.response"><strong>Response:</strong> {{ String(event.response).substring(0, 100) }}...</p>
    </div>

    <div v-else-if="event.type === 'a2a_conversation_completed'" class="event-content">
      <h4>✅ A2A Conversation Completed</h4>
      <p><strong>Status:</strong> {{ event.status }}</p>
      <p v-if="event.total_turns"><strong>Total Turns:</strong> {{ event.total_turns }}</p>
      <p v-if="event.final_result"><strong>Result:</strong> {{ event.final_result }}</p>
      <p v-if="event.error" class="error"><strong>Error:</strong> {{ event.error }}</p>
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

const isA2A = computed(() => {
  return [
    'a2a_delegation_started',
    'a2a_delegation_completed',
    'a2a_conversation_started',
    'a2a_message_sent',
    'a2a_response_received',
    'a2a_conversation_completed',
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
.a2a-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.a2a-event.info {
  background-color: #c8e6c9;
  border-left-color: #388e3c;
}

.a2a-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.a2a-event.error {
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
