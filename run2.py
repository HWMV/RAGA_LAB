# 노마더 코드
from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI
from stock.agents import Agents
from stock.tasks import Tasks

agents = Agents()
tasks = Tasks()

researcher = agents.researcher()
technical_analyst = agents.technical_analyst()
financial_analyst = agents.financial_analyst()
hedge_fund_manager = agents.hedge_fund_manager()

research_task = tasks.research(researcher)
technical_task = tasks.technical_analysis(technical_analyst)
financial_task = tasks.financial_analysis(financial_analyst)

# # 좌/우뇌 에이전트
# from brain.brain_agents import *
# from brain.brain_tasks import *

# brain_agents = Brain_agents()
# brain_tasks = Brain_tasks()

# left_brain = brain_agents.left_brain()
# right_brain = brain_agents.right_brain()

# left_brain_task = brain_tasks.left_brain_task(left_brain)
# right_brain_task = brain_tasks.right_brain_task(right_brain)

recommend_task = tasks.investment_recommendation(
    hedge_fund_manager,
    [
        research_task,
        technical_task,
        financial_task,
        # left_brain_task,
        # right_brain_task,
    ],
)

crew = Crew(
    agents=[
        researcher,
        technical_analyst,
        financial_analyst,
        hedge_fund_manager,
    ],
    tasks=[
        research_task,
        technical_task,
        financial_task,
        recommend_task,
    ],
    verbose=2,
    process=Process.sequential, # hierarchical,
    # manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"),
    memory=True,
)

result = crew.kickoff(
    inputs=dict(
        company="microsoft",
    ),
)