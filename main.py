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









@tool("open a file and read it")
def read_file(file_path):
    """Useful for when you need to load content from a file on the filesystem.
    The input should be a file path as a string."""

    if not file_path.startswith(WORKING_DIR):
        # if the filepath doest not start with the working directory, then just use workindirectory/filename
        file_path = WORKING_DIR + "/" + path.basename(file_path)
    with open(file_path) as file:
        return file.read()


def _build_tasks(endpoints: list, agent: Agent):
    """Build tasks from a list of endpoints"""
    tasks = []
    for endpoint in endpoints:
        tasks.append(
            Task(
                name=f"Analyze {endpoint}",
                description=f"""Analyze the {endpoint} endpoint and provide a short description what the endpoint does and how it can be used. Provide it in a markdown file. with the following structure, Name, Description, Parameters.""",
                agent=agent,
                tools=[question_api_info, read_file]
            )
        )
    return tasks


def main():

    # initialize tools

    search_tool = DuckDuckGoSearchRun()

    researcher = Agent(
        allow_delegation=True,
        role='Senior API Analyst',
        goal='Research and analyze the latest changes to the Ansible Semaphore API',
        backstory="""You are a Senior API Analyst at a leading tech company.
    Your expertise lies in identifying all use cases of an API and involved components. 
    You have a knack for dissecting complex data and presenting
    actionable insights.""",
        verbose=True,
        # Passing human tools to the agent
        tools=[])

    # Create a task
    #task = Task(
    #    name='Analyze Ansible Semaphore API',
    #    description="""Analyze the Ansible Semaphore API and provide a markdown report of all available endpoints and their use cases.""",
    #    agent=researcher
    #    #tools=[search_tool, read_file]
    #)

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
