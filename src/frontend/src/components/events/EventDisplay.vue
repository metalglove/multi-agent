<template>
  <div class="event-display-container">
    <CrewEventDisplay v-if="isCrew" :event="event" />
    <TaskEventDisplay v-else-if="isTask" :event="event" />
    <ReasoningEventDisplay v-else-if="isReasoning" :event="event" />
    <MemoryEventDisplay v-else-if="isMemory" :event="event" />
    <LLMEventDisplay v-else-if="isLLM" :event="event" />
    <ToolEventDisplay v-else-if="isTool" :event="event" />
    <KnowledgeEventDisplay v-else-if="isKnowledge" :event="event" />
    <FlowEventDisplay v-else-if="isFlow" :event="event" />
    <MCPEventDisplay v-else-if="isMCP" :event="event" />
    <A2AEventDisplay v-else-if="isA2A" :event="event" />
    <LoggingGuardrailEventDisplay v-else-if="isLoggingOrGuardrail" :event="event" />
    <div v-else class="unknown-event">
      <p><strong>Unknown Event:</strong> {{ event.type }}</p>
      <pre>{{ JSON.stringify(event, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { EventType } from '../../types/events'
import CrewEventDisplay from './CrewEventDisplay.vue'
import TaskEventDisplay from './TaskEventDisplay.vue'
import ReasoningEventDisplay from './ReasoningEventDisplay.vue'
import MemoryEventDisplay from './MemoryEventDisplay.vue'
import LLMEventDisplay from './LLMEventDisplay.vue'
import ToolEventDisplay from './ToolEventDisplay.vue'
import KnowledgeEventDisplay from './KnowledgeEventDisplay.vue'
import FlowEventDisplay from './FlowEventDisplay.vue'
import MCPEventDisplay from './MCPEventDisplay.vue'
import A2AEventDisplay from './A2AEventDisplay.vue'
import LoggingGuardrailEventDisplay from './LoggingGuardrailEventDisplay.vue'

interface Props {
  event: EventType
}

const props = defineProps<Props>()

const crewEvents = [
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
]

const taskEvents = ['task_started', 'task_completed', 'task_failed']

const reasoningEvents = [
  'agent_reasoning_started',
  'agent_reasoning_completed',
  'agent_reasoning_failed',
]

const memoryEvents = [
  'memory_retrieval_started',
  'memory_retrieval_completed',
  'memory_query_started',
  'memory_query_completed',
  'memory_query_failed',
  'memory_save_started',
  'memory_save_completed',
  'memory_save_failed',
]

const llmEvents = [
  'llm_call_started',
  'llm_call_completed',
  'llm_call_failed',
  'llm_stream_chunk',
]

const toolEvents = [
  'tool_usage_started',
  'tool_usage_finished',
  'tool_usage_error',
  'tool_selection_error',
  'tool_execution_error',
]

const knowledgeEvents = [
  'knowledge_query_started',
  'knowledge_query_completed',
  'knowledge_query_failed',
  'knowledge_search_query_started',
  'knowledge_search_query_completed',
  'knowledge_search_query_failed',
]

const flowEvents = [
  'flow_started',
  'flow_created',
  'flow_finished',
  'flow_plot',
  'method_execution_started',
  'method_execution_finished',
  'method_execution_failed',
]

const mcpEvents = [
  'mcp_connection_started',
  'mcp_connection_completed',
  'mcp_connection_failed',
  'mcp_tool_execution_started',
  'mcp_tool_execution_completed',
  'mcp_tool_execution_failed',
]

const a2aEvents = [
  'a2a_delegation_started',
  'a2a_delegation_completed',
  'a2a_conversation_started',
  'a2a_message_sent',
  'a2a_response_received',
  'a2a_conversation_completed',
]

const loggingGuardrailEvents = [
  'agent_logs_started',
  'agent_logs_execution',
  'llm_guardrail_started',
  'llm_guardrail_completed',
  'llm_guardrail_failed',
]

const isCrew = computed(() => crewEvents.includes(props.event.type))
const isTask = computed(() => taskEvents.includes(props.event.type))
const isReasoning = computed(() => reasoningEvents.includes(props.event.type))
const isMemory = computed(() => memoryEvents.includes(props.event.type))
const isLLM = computed(() => llmEvents.includes(props.event.type))
const isTool = computed(() => toolEvents.includes(props.event.type))
const isKnowledge = computed(() => knowledgeEvents.includes(props.event.type))
const isFlow = computed(() => flowEvents.includes(props.event.type))
const isMCP = computed(() => mcpEvents.includes(props.event.type))
const isA2A = computed(() => a2aEvents.includes(props.event.type))
const isLoggingOrGuardrail = computed(() => loggingGuardrailEvents.includes(props.event.type))
</script>

<style scoped>
.event-display-container {
  width: 100%;
}

.unknown-event {
  padding: 1rem;
  margin: 0.5rem 0;
  background-color: #f5f5f5;
  border: 1px dashed #ccc;
  border-radius: 4px;
}

.unknown-event p {
  margin: 0 0 0.5rem 0;
  font-weight: bold;
  color: #666;
}

.unknown-event pre {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.5rem;
  border-radius: 2px;
  overflow-x: auto;
  font-size: 0.85rem;
  max-height: 300px;
}
</style>
