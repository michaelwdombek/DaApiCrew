from os import getenv, path

from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun, tool


getenv("OPENAI_API_KEY")

# Working Directory Constants
WORKING_DIR = "./workdir"


@tool("open a file and read it")
def read_file(file_path):
    """Useful for when you need to load content from a file on the filesystem.
    The input should be a file path as a string."""

    if not file_path.startswith(WORKING_DIR):
        # if the filepath doest not start with the working directory, then just use workindirectory/filename
        file_path = WORKING_DIR + "/" + path.basename(file_path)
    with open(file_path) as file:
        return file.read()


# Search info from DuckDuckGo
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
    tools=[search_tool, read_file])

# Create a task
task = Task(
    name='Analyze Ansible Semaphore API',
    description="""Read the provided API Specification api.yaml and analyze the Ansible Semaphore API, identify all use cases and involved components search if needed detailed information from the web.
  Present your findings in a markdown list covering each use case and involved component.""",
    agent=researcher,
    tools=[search_tool, read_file]
)

# Create a crew
crew = Crew(
    agents=[researcher],
    tasks=[task],
    verbose=2)

result = crew.kickoff()

print("#####here we go#####")
print(result)
