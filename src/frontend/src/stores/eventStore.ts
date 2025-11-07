import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CrewAIEvent } from '../types/events'

export const useEventStore = defineStore('events', () => {
  const events = ref<CrewAIEvent[]>([])
  const connectionStatus = ref<'connected' | 'disconnected'>('disconnected')
  const ws = ref<WebSocket | null>(null)
  const maxEvents = ref(500) // Keep last 500 events

  const eventsByType = computed(() => {
    const grouped: Record<string, CrewAIEvent[]> = {}
    events.value.forEach(event => {
      if (!grouped[event.type]) {
        grouped[event.type] = []
      }
      grouped[event.type].push(event)
    })
    return grouped
  })

  const agentEvents = computed(() => {
    return events.value.filter(e => 
      e.type.includes('reasoning') || e.type.includes('agent')
    )
  })

  const taskEvents = computed(() => {
    return events.value.filter(e => 
      e.type.includes('task')
    )
  })

  const errorEvents = computed(() => {
    return events.value.filter(e => 
      e.type.includes('failed')
    )
  })

  function addEvent(event: CrewAIEvent) {
    events.value.unshift({
      ...event,
      id: `${Date.now()}-${Math.random()}`,
      receivedAt: new Date(),
    })

    // Keep only recent events
    if (events.value.length > maxEvents.value) {
      events.value = events.value.slice(0, maxEvents.value)
    }
  }

  function clearEvents() {
    events.value = []
  }

  function connectToServer() {
    // Get WebSocket URL from config
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws/events`

    try {
      ws.value = new WebSocket(wsUrl)

      ws.value.onopen = () => {
        console.log('WebSocket connected')
        connectionStatus.value = 'connected'
      }

      ws.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          addEvent({
            type: data.type,
            timestamp: data.timestamp || new Date().toISOString(),
            data: data,
          })
        } catch (e) {
          console.error('Failed to parse event:', e)
        }
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        connectionStatus.value = 'disconnected'
      }

      ws.value.onclose = () => {
        console.log('WebSocket disconnected')
        connectionStatus.value = 'disconnected'
        // Attempt to reconnect after 3 seconds
        setTimeout(connectToServer, 3000)
      }
    } catch (e) {
      console.error('Failed to connect to WebSocket:', e)
      connectionStatus.value = 'disconnected'
      // Retry connection
      setTimeout(connectToServer, 3000)
    }
  }

  function disconnect() {
    if (ws.value) {
      ws.value.close()
      ws.value = null
      connectionStatus.value = 'disconnected'
    }
  }

  return {
    events,
    connectionStatus,
    eventsByType,
    agentEvents,
    taskEvents,
    errorEvents,
    addEvent,
    clearEvents,
    connectToServer,
    disconnect,
  }
})
