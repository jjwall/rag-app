from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import chromadb
import os

# AI Framework Options - Choose one or mix:

# Option 1: LangChain (Traditional)
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# Option 2: LangGraph (Advanced workflows)
# from langgraph.graph import Graph
# from langgraph.prebuilt import ToolExecutor

# Option 3: FastAgency (Simple agents)
# from fastagency import FastAgency
# from fastagency.agents import Agent

# Option 4: CrewAI (Multi-agent)
# from crewai import Agent, Task, Crew

# Option 5: AutoGen (Conversational agents)
# from autogen import AssistantAgent, UserProxyAgent

# Option 6: LlamaIndex (RAG-focused)
# from llama_index import VectorStoreIndex, Document

app = FastAPI(title="AI Ticket Classifier", version="1.0.0")

# Initialize ChromaDB client
chroma_client = chromadb.HttpClient(
    host=os.getenv("CHROMA_HOST", "localhost"),
    port=int(os.getenv("CHROMA_PORT", "8001")),
)


class TicketRequest(BaseModel):
    title: str
    description: str
    user_type: str  # premium, standard, enterprise
    affected_systems: List[str]


class TicketResponse(BaseModel):
    priority: int  # 1-5, where 1 is highest
    reasoning: str
    confidence: float


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ticket-classifier"}


@app.post("/classify", response_model=TicketResponse)
async def classify_ticket(ticket: TicketRequest):
    """
    Classify a support ticket by priority (1-5, where 1 = highest)

    Requirements:
    - Must use ChromaDB for at least one lookup
    - Must make minimum 2 LLM calls/nodes
    - Use any AI framework (LangChain, FastAgency, CrewAI, etc.)

    Framework Examples:

    # LangChain Approach:
    # Step 1: Query ChromaDB
    # Step 2: First LLM call with PromptTemplate
    # Step 3: Second LLM call for final decision

    # FastAgency Approach:
    # Step 1: Create analyzer agent
    # Step 2: Create decision agent
    # Step 3: Chain agents together

    # CrewAI Approach:
    # Step 1: Research agent (ChromaDB query)
    # Step 2: Analysis agent (feature extraction)
    # Step 3: Decision agent (priority assignment)

    # LangGraph Approach:
    # Step 1: Define workflow nodes
    # Step 2: Connect ChromaDB → Analysis → Decision
    # Step 3: Execute graph
    """
    try:
        # TODO: Step 1 - Query ChromaDB for similar historical tickets
        # collection = chroma_client.get_collection("historical_tickets")
        # similar_tickets = collection.query(
        #     query_texts=[f"{ticket.title} {ticket.description}"],
        #     n_results=5,
        #     where={"user_type": ticket.user_type}  # Optional filtering
        # )

        # TODO: Step 2 - First LLM call/node to analyze similarity/features
        # Options:
        # - LangChain: analysis_chain = LLMChain(llm=llm, prompt=analysis_prompt)
        # - FastAgency: analyzer_agent.run(context)
        # - CrewAI: research_task.execute()

        # TODO: Step 3 - Second LLM call/node to determine final priority
        # Options:
        # - LangChain: priority_chain = LLMChain(llm=llm, prompt=priority_prompt)
        # - FastAgency: decision_agent.run(analysis_result)
        # - CrewAI: decision_task.execute()

        # TODO: Parse result and return structured response
        # Ensure response includes:
        # - priority: int (1-5)
        # - reasoning: str (explanation of decision)
        # - confidence: float (0.0-1.0)

        # Placeholder response - replace with your implementation
        return TicketResponse(
            priority=3,
            reasoning="TODO: Implement classification logic using your chosen framework",
            confidence=0.5,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
