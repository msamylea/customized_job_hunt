from langchain_openai import ChatOpenAI


client = ChatOpenAI(model="llama3:latest", base_url="http://localhost:11434/v1", api_key="ollama")