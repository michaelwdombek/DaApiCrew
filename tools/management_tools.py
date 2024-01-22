from langchain_community.tools import tool


@tool("talk to the customer")
def talk_to_customer(query):
    """Useful for when you need to ask the customer a question or need clarification.
    The input should be a question as a string.
    i.e.
        "What is more important right now, creating projects or managing users?" "Creating projects"
    """
    return input(query+"\n")