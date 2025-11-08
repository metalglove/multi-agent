<template>
  <div v-if="isKnowledge" class="knowledge-event" :class="eventClass">
    <div v-if="event.type === 'knowledge_query_started'" class="event-content">
      <h4>📚 Knowledge Query Started</h4>
      <p v-if="event.task_prompt"><strong>Prompt:</strong> {{ event.task_prompt.substring(0, 100) }}...</p>
      <p v-if="event.source_type"><strong>Source:</strong> {{ event.source_type }}</p>
    </div>

    <div v-else-if="event.type === 'knowledge_query_completed'" class="event-content">
      <h4>✅ Knowledge Query Completed</h4>
      <p v-if="event.query"><strong>Query:</strong> {{ event.query }}</p>
      <p v-if="event.source_type"><strong>Source:</strong> {{ event.source_type }}</p>
    </div>

    <div v-else-if="event.type === 'knowledge_query_failed'" class="event-content error">
      <h4>❌ Knowledge Query Failed</h4>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'knowledge_search_query_started'" class="event-content">
      <h4>🔍 Knowledge Retrieval Started</h4>
      <p v-if="event.source_type"><strong>Source:</strong> {{ event.source_type }}</p>
    </div>

    <div v-else-if="event.type === 'knowledge_search_query_completed'" class="event-content">
      <h4>✅ Knowledge Retrieved</h4>
      <p v-if="event.query"><strong>Query:</strong> {{ event.query }}</p>
      <details v-if="event.retrieved_knowledge">
        <summary>Knowledge</summary>
        <pre>{{ String(event.retrieved_knowledge).substring(0, 500) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'knowledge_search_query_failed'" class="event-content error">
      <h4>❌ Knowledge Retrieval Failed</h4>
      <p v-if="event.query"><strong>Query:</strong> {{ event.query }}</p>
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

const isKnowledge = computed(() => {
  return [
    'knowledge_query_started',
    'knowledge_query_completed',
    'knowledge_query_failed',
    'knowledge_search_query_started',
    'knowledge_search_query_completed',
    'knowledge_search_query_failed',
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
.knowledge-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.knowledge-event.info {
  background-color: #e0f2f1;
  border-left-color: #00897b;
}

.knowledge-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.knowledge-event.error {
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
