/**
 * Canonical CrewAI event payloads forwarded from the backend.
 * Most fields are optional because the backend builds payloads with
 * getattr(event, "field", None).
 */
export interface CrewAIEvent {
  type: string
  timestamp?: string | number | null
  // Other top-level fields vary per-event and are listed on each interface
  [key: string]: any
}

// --- Crew / Kickoff events
export interface CrewKickoffStartedEvent extends CrewAIEvent {
  crew_name?: string
  inputs?: Record<string, any> | any[]
}

export interface CrewKickoffCompletedEvent extends CrewAIEvent {
  crew_name?: string
  output?: any
  total_tokens?: number
}

export interface CrewKickoffFailedEvent extends CrewAIEvent {
  crew_name?: string
  error?: any
}

export interface CrewTrainStartedEvent extends CrewAIEvent {
  crew_name?: string
  n_iterations?: number
  filename?: string
  inputs?: Record<string, any> | any[]
}

export interface CrewTrainCompletedEvent extends CrewAIEvent {
  crew_name?: string
  n_iterations?: number
  filename?: string
}

export interface CrewTrainFailedEvent extends CrewAIEvent {
  crew_name?: string
  error?: any
}

export interface CrewTestStartedEvent extends CrewAIEvent {
  crew_name?: string
  n_iterations?: number
  eval_llm?: any
  inputs?: Record<string, any> | any[]
}

export interface CrewTestCompletedEvent extends CrewAIEvent {
  crew_name?: string
}

export interface CrewTestFailedEvent extends CrewAIEvent {
  crew_name?: string
  error?: any
}

export interface CrewTestResultEvent extends CrewAIEvent {
  crew_name?: string
  quality?: number
  execution_duration?: number
  model?: string
}

// --- Task events
export interface TaskStartedEvent extends CrewAIEvent {
  start_time?: string | number | null
  agent_id?: string
  agent_role?: string
  task_title?: string
  task?: string
  prompt_context?: any
}

export interface TaskCompletedEvent extends CrewAIEvent {
  start_time?: string | number | null
  end_time?: string | number | null
  agent_id?: string
  agent_role?: string
  task_title?: string
  task?: string
  output?: any
  prompt_context?: any
}

export interface TaskFailedEvent extends CrewAIEvent {
  start_time?: string | number | null
  end_time?: string | number | null
  agent_id?: string
  agent_role?: string
  task_title?: string
  task?: string
  error?: any
}

// --- Reasoning (agent planning) events
export interface AgentReasoningStartedEvent extends CrewAIEvent {
  attempt?: number
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
}

export interface AgentReasoningCompletedEvent extends CrewAIEvent {
  attempt?: number
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  ready?: boolean
  plan?: any
}

export interface AgentReasoningFailedEvent extends CrewAIEvent {
  attempt?: number
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  error?: any
}

// --- Memory events
export interface MemoryRetrievalStartedEvent extends CrewAIEvent {
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MemoryRetrievalCompletedEvent extends CrewAIEvent {
  task_id?: string
  task_name?: string
  memory_content?: any
  retrieval_time_ms?: number
  from_task?: string | null
  from_agent?: string | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MemoryQueryStartedEvent extends CrewAIEvent {
  query?: string
  limit?: number
  score_threshold?: number
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MemoryQueryCompletedEvent extends CrewAIEvent {
  query?: string
  results?: any[]
  limit?: number
  score_threshold?: number
  query_time_ms?: number
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MemoryQueryFailedEvent extends CrewAIEvent {
  query?: string
  limit?: number
  score_threshold?: number
  error?: any
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MemorySaveStartedEvent extends CrewAIEvent {
  value?: any
  metadata?: Record<string, any>
  agent_role?: string | null
  agent_id?: string | null
}

export interface MemorySaveCompletedEvent extends CrewAIEvent {
  value?: any
  metadata?: Record<string, any>
  save_time_ms?: number
  agent_role?: string | null
  agent_id?: string | null
}

export interface MemorySaveFailedEvent extends CrewAIEvent {
  value?: any
  metadata?: Record<string, any>
  error?: any
  agent_role?: string | null
  agent_id?: string | null
}

// --- LLM events
export interface LLMCallStartedEvent extends CrewAIEvent {
  llm_name?: string
  messages?: any[]
  tools?: any[]
  from_task?: string | null
  from_agent?: string | null
  temperature?: number | null
  callbacks?: any[]
  available_functions?: Record<string, any>
}

export interface LLMCallCompletedEvent extends CrewAIEvent {
  call_type?: string | null
  llm_name?: string
  temperature?: number | null
  messages?: any[]
  response?: any
  from_task?: string | null
  from_agent?: string | null
}

export interface LLMCallFailedEvent extends CrewAIEvent {
  llm_name?: string
  from_task?: string | null
  from_agent?: string | null
  error?: any
}

export interface LLMStreamChunkEvent extends CrewAIEvent {
  llm_name?: string
  chunk?: any
  tool_call?: any
}

// --- Tool usage events
export interface ToolUsageBase extends CrewAIEvent {
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  timestamp?: string | number | null
}

export interface ToolUsageStartedEvent extends ToolUsageBase {
  tool_name?: string
  tools_args?: any
  tool_args?: any
  llm_name?: string | null
  tool_class?: string | null
}

export interface ToolUsageErrorEvent extends ToolUsageBase {
  tool_name?: string
  tools_args?: any
  error?: any
  llm_name?: string | null
  tool_class?: string | null
  delegations?: any
  run_attempts?: number | null
}

export interface ToolUsageFinishedEvent extends ToolUsageBase {
  started_at?: string | number | null
  finished_at?: string | number | null
  from_cache?: boolean | null
  tool_name?: string
  tool_args?: any
  output?: any
  llm_name?: string | null
  tool_class?: string | null
  delegations?: any
  run_attempts?: number | null
}

export interface ToolSelectionErrorEvent extends ToolUsageBase {
  error?: any
  tool_name?: string | null
  tool_args?: any
  tool_class?: string | null
}

export interface ToolExecutionErrorEvent extends ToolUsageBase {
  error?: any
  tool_name?: string | null
  tool_args?: any
  tool_class?: string | null
}

// --- Knowledge events
export interface KnowledgeQueryStartedEvent extends CrewAIEvent {
  task_prompt?: string
  source_type?: string | null
  source_id?: string | null
}

export interface KnowledgeQueryCompletedEvent extends CrewAIEvent {
  query?: string
  source_type?: string | null
  source_id?: string | null
}

export interface KnowledgeQueryFailedEvent extends CrewAIEvent {
  error?: any
  source_type?: string | null
  source_id?: string | null
}

export interface KnowledgeRetrievalStartedEvent extends CrewAIEvent {
  source_type?: string | null
  source_id?: string | null
  query?: string
}

export interface KnowledgeRetrievalCompletedEvent extends CrewAIEvent {
  query?: string
  retrieved_knowledge?: any
  source_type?: string | null
  source_id?: string | null
}

export interface KnowledgeSearchQueryFailedEvent extends CrewAIEvent {
  query?: string
  error?: any
  source_type?: string | null
  source_id?: string | null
}

// --- Flow events
export interface FlowStartedEvent extends CrewAIEvent {
  flow_name?: string
  inputs?: any
}

export interface FlowCreatedEvent extends CrewAIEvent {
  flow_name?: string
}

export interface FlowFinishedEvent extends CrewAIEvent {
  flow_name?: string
  result?: any
}

export interface FlowPlotEvent extends CrewAIEvent {
  flow_name?: string
  meta?: Record<string, any>
}

export interface MethodExecutionStartedEvent extends CrewAIEvent {
  flow_name?: string
  method_name?: string
  state?: any
  params?: any
}

export interface MethodExecutionFinishedEvent extends CrewAIEvent {
  flow_name?: string
  method_name?: string
  result?: any
  state?: any
}

export interface MethodExecutionFailedEvent extends CrewAIEvent {
  flow_name?: string
  method_name?: string
  error?: any
}

// --- MCP events
export interface MCPConnectionStartedEvent extends CrewAIEvent {
  server_name?: string
  server_url?: string
  transport_type?: string
  connect_timeout?: number | null
  is_reconnect?: boolean | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MCPConnectionCompletedEvent extends CrewAIEvent {
  server_name?: string
  server_url?: string
  connection_duration_ms?: number | null
  is_reconnect?: boolean | null
  started_at?: string | number | null
  completed_at?: string | number | null
  agent_id?: string | null
  agent_role?: string | null
}

export interface MCPConnectionFailedEvent extends CrewAIEvent {
  server_name?: string
  server_url?: string
  error?: any
  error_type?: string | null
  started_at?: string | number | null
  failed_at?: string | number | null
}

export interface MCPToolExecutionStartedEvent extends CrewAIEvent {
  server_name?: string
  tool_name?: string
  tool_args?: any
}

export interface MCPToolExecutionCompletedEvent extends CrewAIEvent {
  server_name?: string
  tool_name?: string
  tool_args?: any
  result?: any
  execution_duration_ms?: number | null
}

export interface MCPToolExecutionFailedEvent extends CrewAIEvent {
  server_name?: string
  tool_name?: string
  tool_args?: any
  error?: any
  error_type?: string | null
  started_at?: string | number | null
  failed_at?: string | number | null
}

// --- Logging events
export interface AgentLogsStartedEvent extends CrewAIEvent {
  agent_role?: string
  task_description?: string
  verbose?: boolean | null
}

export interface AgentLogsExecutionEvent extends CrewAIEvent {
  agent_role?: string
  formatted_answer?: any
  verbose?: boolean | null
}

// --- Guardrail events
export interface LLMGuardrailStartedEvent extends CrewAIEvent {
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_role?: string | null
  agent_id?: string | null
  guardrail?: any
  retry_count?: number | null
}

export interface LLMGuardrailCompletedEvent extends CrewAIEvent {
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_role?: string | null
  agent_id?: string | null
  success?: boolean | null
  result?: any
  error?: any
  retry_count?: number | null
}

export interface LLMGuardrailFailedEvent extends CrewAIEvent {
  task_id?: string
  task_name?: string
  from_task?: string | null
  from_agent?: string | null
  agent_role?: string | null
  agent_id?: string | null
  error?: any
  retry_count?: number | null
}

// --- A2A (agent-to-agent) events
export interface A2ADelegationStartedEvent extends CrewAIEvent {
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  endpoint?: string | null
  task_description?: string | null
  is_multiturn?: boolean | null
  turn_number?: number | null
}

export interface A2ADelegationCompletedEvent extends CrewAIEvent {
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  status?: string | null
  result?: any
  error?: any
  is_multiturn?: boolean | null
}

export interface A2AConversationStartedEvent extends CrewAIEvent {
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  endpoint?: string | null
  a2a_agent_name?: string | null
}

export interface A2AConversationCompletedEvent extends CrewAIEvent {
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  status?: string | null
  final_result?: any
  error?: any
  total_turns?: number | null
}

export interface A2AMessageSentEvent extends CrewAIEvent {
  from_agent_id?: string | null
  from_agent_role?: string | null
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  message?: any
  is_multiturn?: boolean | null
  turn_number?: number | null
}

export interface A2AResponseReceivedEvent extends CrewAIEvent {
  from_agent_id?: string | null
  from_agent_role?: string | null
  agent_id?: string
  agent_role?: string
  task_id?: string
  task_name?: string
  response?: any
  is_multiturn?: boolean | null
  turn_number?: number | null
  status?: string | null
}

// Union of known event interfaces (extend as needed)
export type EventType =
  | CrewKickoffStartedEvent
  | CrewKickoffCompletedEvent
  | CrewKickoffFailedEvent
  | CrewTrainStartedEvent
  | CrewTrainCompletedEvent
  | CrewTrainFailedEvent
  | CrewTestStartedEvent
  | CrewTestCompletedEvent
  | CrewTestFailedEvent
  | CrewTestResultEvent
  | TaskStartedEvent
  | TaskCompletedEvent
  | TaskFailedEvent
  | AgentReasoningStartedEvent
  | AgentReasoningCompletedEvent
  | AgentReasoningFailedEvent
  | MemoryRetrievalStartedEvent
  | MemoryRetrievalCompletedEvent
  | MemoryQueryStartedEvent
  | MemoryQueryCompletedEvent
  | MemoryQueryFailedEvent
  | MemorySaveStartedEvent
  | MemorySaveCompletedEvent
  | MemorySaveFailedEvent
  | LLMCallStartedEvent
  | LLMCallCompletedEvent
  | LLMCallFailedEvent
  | LLMStreamChunkEvent
  | ToolUsageStartedEvent
  | ToolUsageErrorEvent
  | ToolUsageFinishedEvent
  | ToolSelectionErrorEvent
  | ToolExecutionErrorEvent
  | KnowledgeQueryStartedEvent
  | KnowledgeQueryCompletedEvent
  | KnowledgeQueryFailedEvent
  | KnowledgeRetrievalStartedEvent
  | KnowledgeRetrievalCompletedEvent
  | KnowledgeSearchQueryFailedEvent
  | FlowStartedEvent
  | FlowCreatedEvent
  | FlowFinishedEvent
  | FlowPlotEvent
  | MethodExecutionStartedEvent
  | MethodExecutionFinishedEvent
  | MethodExecutionFailedEvent
  | MCPConnectionStartedEvent
  | MCPConnectionCompletedEvent
  | MCPConnectionFailedEvent
  | MCPToolExecutionStartedEvent
  | MCPToolExecutionCompletedEvent
  | MCPToolExecutionFailedEvent
  | AgentLogsStartedEvent
  | AgentLogsExecutionEvent
  | LLMGuardrailStartedEvent
  | LLMGuardrailCompletedEvent
  | LLMGuardrailFailedEvent
  | A2ADelegationStartedEvent
  | A2ADelegationCompletedEvent
  | A2AConversationStartedEvent
  | A2AConversationCompletedEvent
  | A2AMessageSentEvent
  | A2AResponseReceivedEvent

