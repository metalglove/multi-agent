## Frontend
Tools manager
- create tools (using MCP server)
- delete tools
- edit tools (only ones that are created by the users)
- list tools (this also includes tools provided by crewai api)

Agent manager interface
- create agents
- delete agents
- edit agents
- list agents

Task manager interface
- create tasks (and assign to agents)
- delete tasks
- edit tasks
- list tasks

Crew manager
- create crew
- delete crew (only crew, not agents, tasks, tools, etc)
- list crews

Run manager
- start runs
- list runs
- end runs

Run interface
- group chat 
- history
- progress

Artifact manager
- dictates where tools are allowed to place artifacts (scope of directory listings, reading and writing)

## bridge
Simple active connections panel and general information

## Runner
All events on the `crewai_event_bus` have to be forwarded.

- Figure out why a run cancels due to
    Received None or empty response from LLM call.
    An unknown error occurred. Please check the details below.
    Error details: Invalid response from LLM call - None or empty.
    An unknown error occurred. Please check the details below.
    Error details: Invalid response from LLM call - None or empty.
    Error during CrewAI kickoff: Invalid response from LLM call - None or empty.
