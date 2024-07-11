# Define the router
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


# 1. Define the model for the agent
class RouterQuery(BaseModel):
    """Route the user among the different services"""
    route: Literal["Vector_storage", "Memory", "Generate"] = Field(
        description="""Given a user query, route the user among the different services
        The services are: Vector_storage, Memory, Generate"""
    )

def runnables_route_question(memory_context, vector_storage_context, question):
    """Route the question to generate, vectorstore or memory
    
    Returns:
        str: Next node to call"""

    # 2. Create the LLM chat
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0
    )
    # 3. Bound the tool and structure the output
    structured_llm_router = llm.with_structured_output(RouterQuery)
    # 4. Create the prompt
    system_prompt = f"""
    You are an expert at routing a user question among Vector_storage, Memory or Generate,
    based on the next contexts, if the memory context does not answer the question, 
    switch to the vector storage context, if neither of the two contexts resolves 
    the question it directs the question to 'Generate':

    MEMORY CONTEXT:
    {memory_context}
    END MEMORY CONTEXT.

    VECTOR_STORAGE CONTEXT:
    {vector_storage_context}
    END VECTOR_STORAGE CONTEXT.  

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