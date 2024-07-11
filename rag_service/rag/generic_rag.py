from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def runnable_conext(context, question):
    """Rag to answer a question based on a context"""

    # Prompt
    prompt_template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    # Chain
    chain = prompt | llm

    # Run
    output = chain.invoke({"context":context,"question":question})
    return output


def runnable_generic(question):
    """Rag to answer a question based on a context"""

    # Prompt
    prompt_template = """You are an expert asistant answer this Question: {question}"""
    prompt = ChatPromptTemplate.from_template(prompt_template)
    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    # Chain
    chain = prompt | llm
    # Run
    output = chain.invoke({"question":question})
    return output
