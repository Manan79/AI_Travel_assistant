from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from dotenv import load_dotenv
import os


load_dotenv()

client = MultiServerMCPClient(
    {
        "Tavily_MCP":{
            "transport": "http",
            "url": rf"https://mcp.tavily.com/mcp/?tavilyApiKey={os.environ['TAVILY_API_KEY']}",
            
        }
    }
)