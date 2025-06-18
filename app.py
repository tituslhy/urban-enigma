from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

from typing import Dict, Literal

app = FastAPI(
    title="LangChain Llama Guard Server",
    version="1.0",
    description="A Llama Guard Runnable built using Langchain's Runnable interfaces served on LangSmith",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Define runnable
llm = OllamaLLM(model="llama-guard3", temperature=0)
parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant."
        ),
        ("human", "{input}")
    ]
)
guard_chain = prompt | llm | parser

# Second runnable
def is_superuser(
    credentials: Dict[
        Literal["username", "password"], str
    ]
) -> bool:
    username = credentials.get("username", None)
    password = credentials.get("password", None)
    if username == "admin" and password == "admin":
        return True
    return False

runnable = RunnableLambda(is_superuser)

# Final runnable
map_chain = RunnableParallel(
    guard_chain = guard_chain,
    superuser_chain = runnable,
)

add_routes(
    app,
    map_chain,
    path="/gatekeeper"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
