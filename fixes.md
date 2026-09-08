# Tool Fixes

## 1. Tavily Search

### Before

```python
async def tavily_search():
    tools = await client.get_tools()
    search_tool = next(t for t in tools if t.name == "tavily_search")
    return [search_tool]
```

### After

```python
@tool
async def tavily_search(query: str, max_results: int = 5):
    tools = await client.get_tools(server_name="Tavily_MCP")
    search_tool = next(t for t in tools if t.name == "tavily_search")
    return await search_tool.ainvoke({
        "query": query,
        "max_results": max_results,
    })
```

### Why it changed

The old function returned a tool definition instead of executing a search. It
also accepted no query, so the agent could not request hotel or place data. The
new function is a real LangChain tool and returns actual Tavily search results.

## 2. Flight Search

### Before

```python
return await route_tool.ainvoke({
    "dep_iata": departure_airport,
    "arr_iata": arrival_airport,
    "limit": limit,
})
```

### After

```python
departure_code = await _airport_code(departure_airport)
arrival_code = await _airport_code(arrival_airport)
return await route_tool.ainvoke({
    "dep_iata": departure_code,
    "arr_iata": arrival_code,
    "limit": limit,
})
```

### Why it changed

The old version required the model to know valid IATA codes. The new version
accepts either airport names or codes and uses Aviationstack airport search
when a name is supplied. It then calls the available `list_routes` MCP tool.

## 3. Railway Search

### Before

```python
bs = boarding_station
ds = destination_station
response = await client.get(f".../{bs}/{ds}")
```

### After

```python
bs = _station_code(boarding_station)
ds = _station_code(destination_station)
response = await client.get(f".../{bs}/{ds}")
```

### Why it changed

The query processor returns station names, while the railway API needs station
codes. The new version accepts both names and codes, reads the station JSON
relative to the tool file, validates `RAILRADAR_API_KEY`, and handles an empty
train list without raising a key error.

## Resulting Flow

```text
Agent -> tavily_search(query) -> actual hotel/place results
Agent -> search_flights(source, destination) -> route results
Agent -> get_train_details(source, destination) -> train results
```

The itinerary agent now receives tool outputs rather than tool definitions.
