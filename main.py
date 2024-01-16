import logging
from os import path
import yaml
from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun, tool
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List


WORKING_DIR = "./workdir"

api_yaml = f"{WORKING_DIR}/api.yaml"
list_of_loaded_docs = []


def _load_swagger_file(uri: str) -> dict:
    """Load a swagger file and return it as a dict"""
    if not uri.startswith(WORKING_DIR):
    # if the filepath doest not start with the working directory, then just use workindirectory/filename
        uri = WORKING_DIR + "/" + path.basename(uri)
    with open(uri) as file:
        return yaml.load(file, Loader=yaml.FullLoader)


RAW_SWAGGER = _load_swagger_file(api_yaml)


def _document_builder(documents: list, content: dict, api_endpoint: bool = False):
    for key, value in content.items():
        if isinstance(value, dict) and key == "paths":
            _document_builder(documents, value, api_endpoint=True)
        else:
            metadata = {
                "endpoint": api_endpoint,
                "source": api_yaml,
                "name": key,
                "type": "swagger",
                "api_version": RAW_SWAGGER["info"]["version"],
                "api_name": RAW_SWAGGER["info"]["title"],
                "api_description": RAW_SWAGGER["info"]["description"]}
            documents.append(
                Document(
                    metadata=metadata,
                    page_content=str(content[key])))
    return documents


CHROMA_DB = Chroma.from_documents(
    _document_builder(
        documents=[],
        content=RAW_SWAGGER), OpenAIEmbeddings())



@tool("question api documentation for information")
def question_api_info(data: str) -> List[any]:
    """Useful to query the api documentation for information. The Input should be an easy-to-understand question.
        For example: What endpoint lists all projects?"""
    top_k = 3
    logging.info(f"query_api_info: {data}")
    #embedding_vector = OpenAIEmbeddings().embed_query(data)
    #response_docs = CHROMA_DB.similarity_search_by_vector(embedding_vector, top_k)
    response_docs = CHROMA_DB.similarity_search(data, top_k)
    return [doc.page_content for doc in response_docs]

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
                description=f"""Analyze the {endpoint} endpoint and provide a markdown of its capabilities.""",
                agent=agent,
                tools=[question_api_info, read_file]
            )
        )
    return tasks


def main():

    # initialize tools
    api_info = question_api_info
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
        tools=[api_info])

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
