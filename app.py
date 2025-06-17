from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

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

add_routes(
    app,
    prompt | llm | parser,
    path="/gatekeeper",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,

)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
