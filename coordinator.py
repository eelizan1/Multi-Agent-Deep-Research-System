import os
import json
from prompts import SUBAGENT_PROMPT_TEMPLATE, COORDINATOR_PROMPT_TEMPLATE
from planner import generate_research_plan
from task_splitter import split_into_subtasks
from smolagents import ToolCallingAgent, MCPClient, tool, InferenceClientModel


FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY")
MCP_URL = f"https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/mcp"

COORDINATOR_MODEL_ID = "meta-llama/Llama-4-Scout-17B-16E-Instruct"
SUBAGENT_MODEL_ID = "meta-llama/Llama-4-Scout-17B-16E-Instruct"


def run_deep_research(user_query: str) -> str:
    print("Running the deep research...")

    research_plan = generate_research_plan(user_query)
    subtasks = split_into_subtasks(research_plan)

    print("Initializing Coordinator")
    print("Coordinator Model: ", COORDINATOR_MODEL_ID)

    coordinator_model = InferenceClientModel(
        model_id=COORDINATOR_MODEL_ID,
        api_key=os.environ.get("HF_TOKEN"),
        provider="nscale",
        bill_to="huggingface",
    )

    subagent_model = InferenceClientModel(
        model_id=SUBAGENT_MODEL_ID,
        api_key=os.environ.get("HF_TOKEN"),
        provider="nscale",
        bill_to="huggingface",
    )

    with MCPClient({"url": MCP_URL, "transport": "streamable-http"}) as mcp_tools:

        @tool
        def initialize_subagent(subtask_id: str, subtask_title: str, subtask_description: str) -> str:
            print(f"Initializing Subagent for task {subtask_id}...")

            subagent = ToolCallingAgent(
                tools=mcp_tools,
                model=subagent_model,
                add_base_tools=False,
                name=f"subagent_{subtask_id}",
            )

            subagent_prompt = SUBAGENT_PROMPT_TEMPLATE.format(
                user_query=user_query,
                research_plan=research_plan,
                subtask_id=subtask_id,
                subtask_title=subtask_title,
                subtask_description=subtask_description,
            )

            return subagent.run(subagent_prompt)

        coordinator = ToolCallingAgent(
            tools=[initialize_subagent],
            model=coordinator_model,
            add_base_tools=False,
            name="coordinator_agent",
        )

        subtasks_json = json.dumps(subtasks, indent=2, ensure_ascii=False)

        coordinator_prompt = COORDINATOR_PROMPT_TEMPLATE.format(
            user_query=user_query,
            research_plan=research_plan,
            subtasks_json=subtasks_json,
        )

        final_report = coordinator.run(coordinator_prompt)
        return final_report
