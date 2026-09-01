from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from dotenv import load_dotenv
import os


load_dotenv()



async def main():
    client = MultiServerMCPClient(
        {
            "Tavily_MCP":{
                "transport": "http",
                "url": rf"https://mcp.tavily.com/mcp/?tavilyApiKey={os.environ['TAVILY_API_KEY']}",
                
            },
            "Railway_client":{
                "transport": "streamable_http",
                "url": "https://railway-mcp.amithv.xyz/mcp",
            }
        }
    )
    tools = await client.get_tools()

    for tool in tools:
        print(tool.name)


if __name__ == "__main__":
    asyncio.run(main())