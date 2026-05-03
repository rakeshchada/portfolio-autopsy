"""Web search tool for the agent to look up market news and context."""

from ddgs import DDGS


MAX_RESULTS = 5


def web_search(query: str, max_results: int = MAX_RESULTS) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return "No results found."

        output = []
        for r in results:
            output.append(f"**{r.get('title', 'No title')}**")
            output.append(f"  {r.get('href', '')}")
            body = r.get('body', '')
            if body:
                output.append(f"  {body[:300]}")
            output.append("")

        return '\n'.join(output)
    except Exception as e:
        return f"Search error: {e}"
