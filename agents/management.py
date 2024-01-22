from textwrap import dedent
from crewai import Agent
from typing import List
from langchain_community.tools import tool


class Managers():

    def senior_requirements(self, tools: List[tool] = None) -> Agent:
        return Agent(
            role='Senior Requirements Engineer',
            goal='Understand the high level needs and brake them down into smaller requirements',
            backstory=dedent("""\
                You are a veteran Senior Requirements Engineer, at a leading consulting firm. You interface with the
                customer and understand his requirments and painpoints. You Analyse his goals and consult with the
                customer if clarification is needed."""),
            allow_delegation=False,
            verbose=True,
            tools=tools,
            )

    def api_researcher(self, tools: List[tool]) -> Agent:
        return Agent(
            role='Senior API Analyst',
            goal='Research and analyze the latest changes to the Ansible Semaphore API',
            backstory=dedent("""\
                You are a Senior API Analyst at a leading tech company. 
                Your expertise lies in identifying all use cases of an API and involved components. 
                You have a knack for dissecting complex data and presenting actionable insights."""),
            allow_delegation=True,
            verbose=True,
            tools=tools,
            )

