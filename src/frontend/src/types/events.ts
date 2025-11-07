export interface CrewAIEvent {
  id?: string
  type: string
  timestamp?: string
  receivedAt?: Date
  data?: Record<string, any>
}

export interface AgentReasoningStartedEvent extends CrewAIEvent {
  type: 'agent_reasoning_started'
  data: {
    agent_role: string
    agent_name: string
  }
}

export interface AgentReasoningCompletedEvent extends CrewAIEvent {
  type: 'agent_reasoning_completed'
  data: {
    reasoning_plan: string
    agent_role: string
  }
}

export interface TaskStartedEvent extends CrewAIEvent {
  type: 'task_started'
  data: {
    task_title: string
    task_description: string
  }
}

export interface TaskCompletedEvent extends CrewAIEvent {
  type: 'task_completed'
  data: {
    task_title: string
    task_output: string
  }
}

export type EventType =
  | AgentReasoningStartedEvent
  | AgentReasoningCompletedEvent
  | TaskStartedEvent
  | TaskCompletedEvent
