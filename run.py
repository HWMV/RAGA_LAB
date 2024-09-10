# 뇌모듈 MAS
# ==== 회의 후 수정 코드 ==== #
import os, asyncio
import re
from dotenv import load_dotenv

from crewai import Crew
from crewai import Agent
from crewai.process import Process
from langchain_openai import ChatOpenAI

from stock.agents import Agents
from stock.tasks import *

from brain.brain_agents import *
from brain.brain_tasks import *

load_dotenv()

os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo-0125"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

from crewai import Crew
from crewai.process import Process
from langchain_openai import ChatOpenAI

from stock.agents import *
from stock.tasks import *

from brain.brain_agents import *
from brain.brain_tasks import Brain_tasks

# 백 테스트 시 기록을 위한 필요 태그 추출 함수
def extract_price_predictions(result):
    six_month_price = re.search(r'\[6month_price_target\]:\s*\$?(\d+(\.\d+)?)', result)
    twelve_month_price = re.search(r'\[12month_price_target\]:\s*\$?(\d+(\.\d+)?)', result)
    
    return {
        '6MONTH_PRICE_TARGET': six_month_price.group(1) if six_month_price else "Not found",
        '12MONTH_PRICE_TARGET': twelve_month_price.group(1) if twelve_month_price else "Not found"
    }

def main():
    # Second_crew에서 ticker를 입력으로 못 받아서 수정 (직접 명시)
    company = "microsoft"
    # ticker = "CRM"  # 회사의 실제 ticker를 사용

    # 왜 따로 정의를 다시 해야 되는거지?? 정의 안하고 Agents 바로 객체를 사용하면 self 인자 에러 발생. 정적 메서드 vs 인스턴스 메서드 차이?
    agents = Agents()
    tasks = Tasks()
    brain_agents = Brain_agents()
    brain_tasks = Brain_tasks()

    # 첫 번째 Crew 설정
    researcher = agents.researcher()
    technical_analyst = agents.technical_analyst()
    financial_analyst = agents.financial_analyst()
    # 노마더 코더
    # hedge_fund_manager 대신 뇌 모듈 : 뇌모듈로 종합 분석 보고서를 작성
    left_brain = brain_agents.left_brain()
    right_brain = brain_agents.right_brain()
    brain_agent = brain_agents.brain_agent()

    research_task = tasks.research(researcher)
    technical_task = tasks.technical_analysis(technical_analyst)
    financial_task = tasks.financial_analysis(financial_analyst)

    # brainModule apply, hedge_fund_manager 대신 뇌모듈
    # 을 추가 (recommendation task를 수행)
    left_brain_task = brain_tasks.left_brain_task(
        left_brain, [
            technical_task,
            financial_task,
        ]
    )
    right_brain_task = brain_tasks.right_brain_task(
        right_brain, [
            research_task,
            technical_task,
        ]
    )

    brain_agent_task = brain_tasks.brain_agent_task(
        brain_agent, [
            left_brain_task,
            right_brain_task,
        ]
    )

    # left_brain_task = brain_tasks.left_brain_task(left_brain)
    # right_brain_task = brain_tasks.right_brain_task(right_brain)
    # brain_agent_task = brain_tasks.brain_agent_task(brain_agent)

    first_crew = Crew(
        agents=[researcher, 
                technical_analyst, 
                financial_analyst,
                left_brain,
                right_brain,
                brain_agent
                ], 

        tasks=[research_task, 
                technical_task, 
                financial_task,
                left_brain_task,
                right_brain_task,
                brain_agent_task,
                ],

        process=Process.sequential, # hierarchical,
        # manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"), # "gpt-4o"),
        memory=True,
    )

    # 첫 번째 크루 실행 (비동기)
    final_result = first_crew.kickoff(inputs={"company": company})

    # # 결과에서 가격 예측 추출
    # price_predictions = extract_price_predictions(final_result)

    # print(f"\nAnalysis complete for {company}") # ({ticker})")
    # print(f"6-month price prediction: ${price_predictions['6MONTH_PRICE_TARGET']}")
    # print(f"12-month price prediction: ${price_predictions['12MONTH_PRICE_TARGET']}")

    # # 예측 가격만 따로 저장
    # with open(f"{company}__price_predictions.txt", "w") as f:
    #     f.write(f"Company: {company}\n")
    #     f.write(f"6month price target prediction: ${price_predictions['6MONTH_PRICE_TARGET']}\n")
    #     f.write(f"12month price target prediction: ${price_predictions['12MONTH_PRICE_TARGET']}\n")

    return final_result

if __name__ == "__main__":
    final_result = main()
    print(final_result)


# ==== 수정 전 코드 ==== #
# import os, asyncio
# from dotenv import load_dotenv

# from crewai import Crew
# from crewai.process import Process
# from langchain_openai import ChatOpenAI

# from stock.agents import Agents
# from stock.tasks import *

# from brain.brain_agents import *
# from brain.brain_tasks import *

# load_dotenv()

# os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo-0125"
# OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# from crewai import Crew
# from crewai.process import Process
# from langchain_openai import ChatOpenAI

# from stock.agents import *
# from stock.tasks import *

# from brain.brain_agents import *
# from brain.brain_tasks import *

# def main():
#     # Second_crew에서 ticker를 입력으로 못 받아서 수정 (직접 명시)
#     company = "Salesforce"
#     ticker = "CRM"  # 회사의 실제 ticker를 사용

#     # 첫 번째 Crew 설정 (비동기 실행)
#     agents = Agents()
#     tasks = Tasks()
#     researcher = agents.researcher()
#     technical_analyst = agents.technical_analyst()
#     financial_analyst = agents.financial_analyst()

#     research_task = tasks.research(researcher)
#     technical_task = tasks.technical_analysis(technical_analyst)
#     financial_task = tasks.financial_analysis(financial_analyst)

#     # financial_analyst에게 Key Financial Metrics 도구 사용 강조
#     financial_analyst.tools.append(Tools.get_key_metrics)

#     first_crew = Crew(
#         agents=[researcher, technical_analyst, financial_analyst], 
#         tasks=[research_task, technical_task, financial_task],
#         process=Process.hierarchical,
#         manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"), # "gpt-4o"),
#         memory=True,
#     )

#     # 첫 번째 크루 실행 (비동기)
#     first_result = asyncio.run(first_crew.kickoff_async(inputs={"company": company, "ticker": ticker}))

#     # 두 번째 Crew 설정 (동기 실행)
#     second_agents = Brain_agents()
#     second_tasks = Brain_tasks()

#     left_brain = second_agents.left_brain()
#     right_brain = second_agents.right_brain()
#     brain_agent = second_agents.brain_agent()

#     # left_brain과 right_brain에게 Key Financial Metrics 도구 사용 강조
#     left_brain.tools.append(Tools.get_key_metrics)
#     right_brain.tools.append(Tools.get_key_metrics)

#     # second_crew ticker 직접 입력 수정
#     analyze_report_task = second_tasks.analyze_report(left_brain, right_brain, first_result, ticker)

#     second_crew = Crew(
#         agents=[left_brain, right_brain],
#         tasks=[analyze_report_task],
#         manager_agent=brain_agent,
#         verbose=2,
#         process=Process.hierarchical,
#         manager_llm=ChatOpenAI(model="gpt-3.5-turbo-0125"), # "gpt-4o"),
#         memory=True,
#     )

#     # 두 번째 크루 실행 (동기)
#     # Key financial metric 명확하게 전부 출력하는지 확인하기 위해 로직 추가
#     # Key Financial Metrics 가져오기
#     second_result = second_crew.kickoff(inputs={"report": first_result, "ticker": ticker}) 

#     # Key Financial Metrics 확인
#     # 결과에 Key Financial Metrics 섹션이 없으면 직접 추가
#     if "Key Financial Metrics:" not in second_result:
#         key_metrics = Tools.get_key_metrics(ticker)
#         second_result = f"Key Financial Metrics:\n{key_metrics}\n\n{second_result}"

#     # 결과 파일에 쓰기
#     with open("final_recommendation_report.md", "w") as f:
#         f.write(second_result)

#     # Key Financial Metrics 확인
#     if "Key Financial Metrics:" not in second_result:
#         print("Warning: Key Financial Metrics section is missing in the final report.")
#     else:
#         print("Key Financial Metrics section is present in the final report.")

#     return second_result

# if __name__ == "__main__":
#     final_result = main()
#     print(final_result)