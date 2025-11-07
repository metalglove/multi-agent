from pydantic import BaseModel, Field  # For structured outputs
from typing import List


# # Pydantic model for structured proposal outputs (e.g., list of ideas)
# class Proposal(BaseModel):
#     idea: str = Field(description="Description of the idea")
#     pros: List[str] = Field(description="List of pros")
#     cons: List[str] = Field(description="List of cons")
#     tech_stack: str = Field(description="Recommended tech stack")

# class ProposalsList(BaseModel):
#     proposals: List[Proposal] = Field(description="List of 3-5 proposals")
