from crewai import Task, Agent
from typing import List
from langchain_community.tools import tool

from tools.management_tools import talk_to_customer


class HighLevelTasks():
    """
    These tasks are very high level and should be broken down into smaller tasks handed of to sub crews by the llm
    """
    default_tools = [talk_to_customer]

    @classmethod
    def _add_management_tasks(cls, tools: List[tool] = None) -> List[tool]:
        """
        Check the provided tools and add the default tools if they are not already provided

        Args:
            tools (List[tool], optional): The tools that will be available to the agent. Defaults to None.
        Returns:
            List[tool]: The tools that will be available to the agent, including the default tools for high levle tasks
                        like talk_to_customer
        """
        return tools + cls.default_tools if tools is not None else cls.default_tools

    @classmethod
    def understand_customer(cls, agent: Agent = None, tools: List[tool] = None) -> Task:
        """
        Understand the customer and his needs, and starts as initial task for the llm

        Args:
            agent (Agent, optional): The agent that will be assigned to the task. Defaults to None.
            tools (List[tool], optional): The tools that will be available to the agent. Defaults to None.
        Returns:
            Task: The task to be completed
        """
        return Task(
            name="Understand the customer",
            description="Understand the customer and his needs",
            agent=agent,
            tools=cls._add_management_tasks(tools)




        )

