import asyncio

from listeners import (
    A2AListener,
    CrewListener,
    FlowListener,
    GuardrailListener,
    KnowledgeListener,
    LLMListener,
    LoggingListener,
    MCPListener,
    ReasoningListener,
    TaskListener,
    ToolUsageListener,
    MemoryListener
)

from crewai.events.event_bus import CrewAIEventsBus

def setup_listeners(loop: asyncio.AbstractEventLoop, 
                    queue: asyncio.Queue, 
                    crewai_event_bus: CrewAIEventsBus) -> None:
    # Instantiate per-group listeners and let them register their handlers
    listeners = [
        TaskListener(loop, queue),
        CrewListener(loop, queue),
        ReasoningListener(loop, queue),
        LLMListener(loop, queue),
        ToolUsageListener(loop, queue),
        A2AListener(loop, queue),
        FlowListener(loop, queue),
        KnowledgeListener(loop, queue),
        MemoryListener(loop, queue),
        MCPListener(loop, queue),
        LoggingListener(loop, queue),
        GuardrailListener(loop, queue),
    ]
    for listener in listeners:
        listener.setup_listeners(crewai_event_bus)
    return listeners
