<template>
  <div v-if="isCrew" class="crew-event" :class="eventClass">
    <div v-if="event.type === 'crew_kickoff_started'" class="event-content">
      <h4>🚀 Crew Kickoff Started</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <details v-if="event.inputs">
        <summary>Inputs</summary>
        <pre>{{ JSON.stringify(event.inputs, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'crew_kickoff_completed'" class="event-content">
      <h4>✅ Crew Kickoff Completed</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p v-if="event.total_tokens"><strong>Tokens:</strong> {{ event.total_tokens }}</p>
      <details v-if="event.output">
        <summary>Output</summary>
        <pre>{{ JSON.stringify(event.output, null, 2) }}</pre>
      </details>
    </div>

    <div v-else-if="event.type === 'crew_kickoff_failed'" class="event-content error">
      <h4>❌ Crew Kickoff Failed</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'crew_train_started'" class="event-content">
      <h4>🎓 Crew Training Started</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Iterations:</strong> {{ event.n_iterations }}</p>
      <p><strong>File:</strong> {{ event.filename }}</p>
    </div>

    <div v-else-if="event.type === 'crew_train_completed'" class="event-content">
      <h4>✅ Crew Training Completed</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Iterations:</strong> {{ event.n_iterations }}</p>
    </div>

    <div v-else-if="event.type === 'crew_train_failed'" class="event-content error">
      <h4>❌ Crew Training Failed</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'crew_test_started'" class="event-content">
      <h4>🧪 Crew Testing Started</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Iterations:</strong> {{ event.n_iterations }}</p>
    </div>

    <div v-else-if="event.type === 'crew_test_completed'" class="event-content">
      <h4>✅ Crew Testing Completed</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
    </div>

    <div v-else-if="event.type === 'crew_test_failed'" class="event-content error">
      <h4>❌ Crew Testing Failed</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Error:</strong> {{ event.error }}</p>
    </div>

    <div v-else-if="event.type === 'crew_test_result'" class="event-content">
      <h4>📊 Crew Test Result</h4>
      <p><strong>Crew:</strong> {{ event.crew_name }}</p>
      <p><strong>Quality:</strong> {{ event.quality?.toFixed(2) }}</p>
      <p><strong>Duration:</strong> {{ event.execution_duration }}ms</p>
      <p><strong>Model:</strong> {{ event.model }}</p>
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

const isCrew = computed(() => {
  return [
    'crew_kickoff_started',
    'crew_kickoff_completed',
    'crew_kickoff_failed',
    'crew_train_started',
    'crew_train_completed',
    'crew_train_failed',
    'crew_test_started',
    'crew_test_completed',
    'crew_test_failed',
    'crew_test_result',
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
.crew-event {
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 4px solid #ccc;
}

.crew-event.info {
  background-color: #e3f2fd;
  border-left-color: #2196f3;
}

.crew-event.success {
  background-color: #e8f5e9;
  border-left-color: #4caf50;
}

.crew-event.error {
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
