LATEST_AGENT_STATE = {
    "prompt": "",
    "agent_result": None,
    "results": [],
}


def save_latest_agent_state(prompt, agent_result):
    """
    Store the latest AI Agent result in memory.

    This keeps the AI panel visible when the user opens emails
    from the AI result list.
    """

    LATEST_AGENT_STATE["prompt"] = prompt
    LATEST_AGENT_STATE["agent_result"] = agent_result
    LATEST_AGENT_STATE["results"] = agent_result.get("emails", [])


def get_latest_agent_state():
    """
    Return the latest AI Agent result.
    """

    return LATEST_AGENT_STATE


def clear_latest_agent_state():
    """
    Clear the latest AI Agent result.
    """

    LATEST_AGENT_STATE["prompt"] = ""
    LATEST_AGENT_STATE["agent_result"] = None
    LATEST_AGENT_STATE["results"] = []