<template>
  <div class="agent-chat">
    <!-- Agents List (Sidebar) -->
    <div class="agents-sidebar">
      <div class="sidebar-header">
        <h3>👥 Active Agents</h3>
      </div>
      <div class="agents-list">
        <button
          v-for="agent in activeAgents"
          :key="agent.id"
          class="agent-button"
          :class="{ active: selectedAgent === agent.id }"
          @click="selectedAgent = agent.id"
        >
          <span class="agent-avatar">{{ agent.avatar }}</span>
          <div class="agent-info">
            <span class="agent-name">{{ agent.name }}</span>
            <span class="agent-status">{{ agent.status }}</span>
          </div>
          <span v-if="agent.messageCount > 0" class="badge">{{ agent.messageCount }}</span>
        </button>
      </div>
    </div>

    <!-- Chat Area -->
    <div class="chat-area">
      <!-- Chat Header -->
      <div v-if="selectedAgent" class="chat-header">
        <div class="header-info">
          <span class="agent-avatar-large">{{ currentAgent?.avatar }}</span>
          <div>
            <h2>{{ currentAgent?.name }}</h2>
            <span class="status-text">{{ currentAgent?.status }}</span>
          </div>
        </div>
      </div>

      <!-- Messages -->
      <div class="messages-container">
        <div v-if="chatMessages.length === 0" class="empty-state">
          <p>👋 No messages yet. Agents will communicate here.</p>
        </div>
        <div v-else class="messages-list">
          <div
            v-for="msg in chatMessages"
            :key="msg.id"
            class="message"
            :class="{ 'own-message': msg.fromAgent === selectedAgent }"
          >
            <div class="message-avatar">{{ msg.avatar }}</div>
            <div class="message-content">
              <div class="message-header">
                <span class="message-sender">{{ msg.fromAgent }}</span>
                <span class="message-time">{{ formatTime(msg.timestamp) }}</span>
              </div>
              <div class="message-body">
                <MarkdownRenderer :content="msg.text" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useEventStore } from '../stores/eventStore'
import type { CrewAIEvent } from '../types/events'
import MarkdownRenderer from './MarkdownRenderer.vue'

const store = useEventStore()
const selectedAgent = ref<string | null>(null)

interface Agent {
  id: string
  name: string
  avatar: string
  status: string
  messageCount: number
}

interface ChatMessage {
  id: string
  fromAgent: string
  avatar: string
  text: string
  timestamp: string
  eventType: string
}

// Extract unique agents from events
const activeAgents = computed<Agent[]>(() => {
  const agents: Record<string, Agent> = {}

  store.events.forEach((event: CrewAIEvent) => {
    const agentRole = (event.data as any)?.agent_role
    const agentId = (event.data as any)?.agent_id

    if (agentRole) {
      const id = agentId || agentRole
      if (!agents[id]) {
        agents[id] = {
          id,
          name: agentRole,
          avatar: getAgentAvatar(agentRole),
          status: getAgentStatus(),
          messageCount: 0,
        }
      }

      // Count messages for this agent
      if (
        event.type.includes('reasoning') ||
        event.type.includes('task_started') ||
        event.type.includes('task_completed') ||
        event.type.includes('memory') ||
        event.type.includes('llm_call')
      ) {
        agents[id].messageCount++
      }
    }
  })

  return Object.values(agents).sort((a, b) => b.messageCount - a.messageCount)
})

const currentAgent = computed(() => {
  return activeAgents.value.find(a => a.id === selectedAgent.value)
})

// Generate chat messages from events
const chatMessages = computed<ChatMessage[]>(() => {
  if (!selectedAgent.value) return []

  const messages: ChatMessage[] = []

  store.events.forEach((event: CrewAIEvent) => {
    const eventData = event.data as any
    const agentRole = eventData?.agent_role
    const agentId = eventData?.agent_id
    const agentIdentifier = agentId || agentRole

    if (agentIdentifier !== selectedAgent.value) return

    let messageText = ''

    if (event.type.includes('agent_reasoning_started')) {
      messageText = `🧠 Starting reasoning phase...`
    } else if (event.type.includes('agent_reasoning_completed')) {
      messageText = `✅ Reasoning complete: ${eventData.plan || 'Plan generated'}`
    } else if (event.type.includes('agent_reasoning_failed')) {
      messageText = `❌ Reasoning failed: ${eventData.error || 'Unknown error'}`
    } else if (event.type.includes('task_started')) {
      messageText = `🚀 Started task: ${eventData.task_title || 'Task'}`
    } else if (event.type.includes('task_completed')) {
      messageText = `✨ Completed task: ${eventData.task_title || 'Task'}`
    } else if (event.type.includes('memory_query')) {
      messageText = `📚 Querying memory for: ${eventData.query || 'information'}`
    } else if (event.type.includes('memory_retrieval')) {
      messageText = `💾 Retrieved memory data`
    } else if (event.type.includes('llm_call_started')) {
      messageText = `🤖 Calling LLM (${eventData.model || 'model'})`
    } else if (event.type.includes('llm_call_completed')) {
      messageText = `✅ LLM responded`
    } else if (event.type.includes('tool_usage')) {
      messageText = `🔧 Using tool: ${eventData.tool_name || 'tool'}`
    } else if (event.type.includes('a2a')) {
      messageText = `🔗 Agent-to-agent communication`
    } else {
      messageText = `📌 ${event.type}`
    }

    if (messageText) {
      messages.push({
        id: `${event.timestamp}-${Math.random()}`,
        fromAgent: agentIdentifier || 'Unknown',
        avatar: getAgentAvatar(agentRole || ''),
        text: messageText,
        timestamp: event.timestamp as string || new Date().toISOString(),
        eventType: event.type,
      })
    }
  })

  return messages.reverse() // Reverse so newest messages appear at top
})

// Initialize with first agent if available
if (activeAgents.value.length > 0 && !selectedAgent.value) {
  selectedAgent.value = activeAgents.value[0].id
}

function getAgentAvatar(agentRole: string): string {
  const role = agentRole?.toLowerCase() || ''
  if (role.includes('researcher')) return '🔬'
  if (role.includes('analyst')) return '📊'
  if (role.includes('writer')) return '✍️'
  if (role.includes('manager')) return '📋'
  if (role.includes('developer')) return '💻'
  if (role.includes('designer')) return '🎨'
  if (role.includes('qa')) return '🧪'
  if (role.includes('coordinator')) return '📞'
  return '🤖'
}

function getAgentStatus(): string {
  return 'Active'
}

function formatTime(timestamp: string | number | null | undefined): string {
  if (!timestamp) return 'Just now'
  try {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    })
  } catch {
    return 'Just now'
  }
}
</script>

<style scoped>
.agent-chat {
  display: flex;
  height: 100%;
  gap: 1rem;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.agents-sidebar {
  width: 280px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
}

.sidebar-header h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #333;
}

.agents-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.agent-button {
  padding: 0.75rem;
  background: white;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.2s;
  text-align: left;
  position: relative;
}

.agent-button:hover {
  background: #f0f0f0;
  border-color: #667eea;
}

.agent-button.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.agent-avatar {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.agent-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.agent-name {
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.agent-status {
  font-size: 0.75rem;
  opacity: 0.7;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #f44336;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  min-width: 0; /* Important: allows flex items to shrink */
}

.chat-header {
  padding: 1rem;
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.agent-avatar-large {
  font-size: 2rem;
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.status-text {
  font-size: 0.85rem;
  color: #999;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  background: #f9f9f9;
  scroll-behavior: smooth;
  min-width: 0; /* Important: allows children to wrap */
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 1rem;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
}

.message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
  min-width: 0; /* Important: allows flex children to shrink below their content size */
}

.message.own-message {
  flex-direction: row-reverse;
}

.message-avatar {
  font-size: 1.5rem;
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  flex: 0 1 70%;
  min-width: 0; /* Important: allows content to wrap properly */
  overflow-wrap: break-word;
}

.message.own-message .message-content {
  margin-left: auto;
}

.message-header {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
  font-size: 0.85rem;
}

.message-sender {
  font-weight: 600;
  color: #333;
}

.message-time {
  color: #999;
}

.message-body {
  background: white;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  border-left: 3px solid #667eea;
  color: #333;
  line-height: 1.4;
  word-break: break-word;
  overflow-wrap: break-word;
  min-width: 0; /* Important: allows markdown content to wrap */
}

.message-body :deep(.markdown-renderer) {
  margin: 0;
}

.message-body :deep(.markdown-renderer p) {
  margin: 0;
  padding: 0;
}

.message-body :deep(.markdown-renderer *) {
  margin: 0.25rem 0;
  padding: 0;
  line-height: 1.4;
}

.message-body :deep(.markdown-renderer code) {
  background: #f0f0f0;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-size: 0.9em;
}

.message.own-message .message-body {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-left: none;
  border-right: 3px solid #764ba2;
}

.message.own-message .message-body :deep(.markdown-renderer a) {
  color: #e0e7ff;
  text-decoration: underline;
}

.message.own-message .message-body :deep(.markdown-renderer code) {
  background: rgba(0, 0, 0, 0.2);
  color: #f0f0f0;
}

.message.own-message .message-body :deep(.markdown-renderer blockquote) {
  border-left-color: rgba(255, 255, 255, 0.5);
  color: rgba(255, 255, 255, 0.9);
}
</style>
