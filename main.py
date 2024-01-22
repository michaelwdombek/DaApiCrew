import logging
from os import path
import yaml
from crewai import Agent, Task, Crew

from langchain_community.tools import DuckDuckGoSearchRun, tool
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List

from tools.swagger_backend import SwaggerAPI
from tools.general_tools import write_file

from agents.management import Managers
from agents.engineering import Engineers


# Setting up basics
WORKING_DIR = "./workdir"

api_yaml = f"{WORKING_DIR}/api.yaml"

# Initializing tools
swagger_api = SwaggerAPI(api_path=api_yaml)


@tool("search for an endpoint")
def search_endpoint(query):
    """Useful for when you need to find an endpoint in the api
    The input should be the endpoint path or the beginning of the endpoint path. 
    ie '/project' will return all endpoints that start with '/project' including '/project/{project_id}' etc"""
    return swagger_api.endpoint_search(query)

@tool("get endpoint info")
def detailed_api_info(endpoint):
    """Useful for when you need to get detailed information about an endpoint
    The input must be the full endpoint path ie '/project/{project_id}', will return the endpoint as well as methods and parameters"""
    return swagger_api.get_endpoint(endpoint)




def _build_tasks(endpoints: list, agent: Agent):
    """Build tasks from a list of endpoints"""
    tasks = []
    for endpoint in endpoints:
        tasks.append(
            Task(
                name=f"Analyze {endpoint}",
                description=f"""Analyze the {endpoint} endpoint 
                and provide a very short description what the endpoint does and how it can be used. 
                Provide it in a markdown format. With the following structure, Name, Description, Parameters 
                and write it to a file called {endpoint}.md""",
                agent=agent,
                tools=[detailed_api_info, write_file]
            )
        )
    return tasks


def main():

    # initialize tools

    search_tool = DuckDuckGoSearchRun()

    researcher = Managers().api_researcher(tools=[detailed_api_info])

    # Create a crew
    crew = Crew(
        agents=[researcher],
        tasks=_build_tasks(['/projects', '/users'], researcher),
        verbose=2)

    result = crew.kickoff()

    print("#####here we go#####")
    print(result)

if __name__ == "__main__":
    main()
