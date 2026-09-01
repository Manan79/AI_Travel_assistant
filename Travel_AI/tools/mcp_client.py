from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from dotenv import load_dotenv
import os


load_dotenv()



client = MultiServerMCPClient(
      {
          "Tavily_MCP": {
              "transport": "http",
              "url": rf"https://mcp.tavily.com/mcp/?tavilyApiKey={os.environ['TAVILY_API_KEY']}",
          },
          "Aviationstack_MCP": {
              "transport": "stdio",
              "command": "uvx",
              "args": ["--with", "mcp<2", "aviationstack-mcp"],
              "env": {
                  "AVIATIONSTACK_API_KEY": os.environ.get(
                      "AVIATIONSTACK_API_KEY",
                      os.environ.get("AVIVATIONSTACK_API_KEY", ""),
                  )
              },
          },
      }
  )
