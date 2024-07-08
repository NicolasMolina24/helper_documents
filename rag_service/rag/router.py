# Define the router
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


# 1. Define the model for the agent
class RouterQuery(BaseModel):
    """Route the user among the different services"""
    route: Literal["vector_storage", "memory", "None"] = Field(
        description="""Given a user query, route the user among the different services
        The services are: "vector_storage or memory"""
    )

def runnables_route_question(question):
    """Route the question to web search, vectorstore or memory
    
    Returns:
        str: Next node to call"""

    # 2. Create the LLM chat
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )
    # 3. Bound the tool and structure the output
    structured_llm_router = llm.with_structured_output(RouterQuery)
    # 4. Create the prompt
    system_prompt = f"""
    You are an expert at routing a user question, Use the vectorstore to answer 
    questions or the memory for retrieve information about our conversation history."
    """
    
    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}")
        ]
    )
    # 5. Create the LCE
    chain =  route_prompt | structured_llm_router
    return chain.invoke({"question": question})