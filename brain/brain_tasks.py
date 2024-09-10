# ======== 수정 전 코드 ========= #
from crewai import Task

class Brain_tasks:
    def left_brain_task(self, agent, context):
        return Task(
            description=f"""Conduct a comprehensive, quantitative analysis of {context} based on the results from the technical analysis and financial analysis:
            1. Review and synthesize the technical and financial analysis results.
            2. Analyze historical stock price data, financial statements, and industry trends.
            3. Provide logical and objective 6-month and 12-month price targets based on quantitative metrics.
            4. Support your analysis with specific financial ratios, valuation metrics, and historical performance data.
            5. Consider potential risks based on financial data and market position.
            6. Ensure your price predictions are realistic and based solely on quantitative data, avoiding any emotional bias.

            Your analysis must be thorough, objective, and based solely on verifiable quantitative data. Maintain a cold, analytical approach in your price predictions.""",

            expected_output=f"""Produce a detailed quantitative report with the following structure:

            1. Summary of Technical and Financial Analysis Results

            2. Quantitative 6-Month and 12-Month Price Targets:
            [Left BRain 6-month price target]: $XX.XX
            [Left BRain 12-month price target]: $XX.XX

            3. Detailed Analysis (including historical data, financial statements, valuation metrics, industry analysis)

            4. Quantitative Risk Assessment

            5. Conclusion: Summary of key quantitative findings and justification for price targets

            CRITICAL: The 6-month and 12-month price targets must be clearly tagged as shown above.""",
            agent=agent,
            context=context,
            output_file="left_brain_report.md"
        )

    def right_brain_task(self, agent, context):
        return Task(
            description=f"""Provide insightful and qualitative analysis of {context} based on news articles as research and technical analysis:
            1. Review and interpret qualitative research result.
            2. Analyze recent news, market sentiment, and potential catalysts, giving appropriate weight to positive news.
            3. Identify emerging trends, disruptive factors, and potential future scenarios.
            4. Provide intuitive 6-month and 12-month price targets based on qualitative factors and market dynamics, ensuring they reflect the overall sentiment of news and market trends.
            5. Consider broader economic, social, and geopolitical contexts in the analysis.
            6. Ensure that price predictions are grounded in reality while reflecting the positive aspects found in news articles and market sentiment.

            Analysis should be creative and focus on future potential and market sentiment, considering factors other than numbers. Pay special attention to positive news and its potential impact on future stock performance.""",

            expected_output=f"""A comprehensive qualitative report with the following structure:

            1. Summary of research findings and news analysis, highlighting positive aspects

            2. Qualitative 6-month and 12-month price targets:
            [Right Brain 6-month price target]: $XX.XX
            [Right Brain 12-month price target]: $XX.XX

            3. Detailed analysis (including market sentiment, potential catalysts, emerging trends, and macroeconomic factors)

            4. Qualitative risk assessment balanced with growth opportunities

            5. Conclusion: Summary of key qualitative findings and justification for price target, emphasizing how positive news influences the prediction

            Important: 6-month and 12-month price targets must be clearly tagged as shown above and should reflect the overall positive sentiment when appropriate.""",
            agent=agent,
            context=context,
            output_file="right_brain_report.md"
        )

    def brain_agent_task(self, agent, context):
        return Task(
            description=f"""Synthesize a comprehensive investment recommendation report for {context}:
            1. Review and summarize the Left Brain (quantitative) analysis.
            2. Review and summarize the Right Brain (qualitative) analysis.
            3. Integrate both analyses, reconciling any discrepancies.
            4. Provide a final conclusion with 6-month and 12-month price targets and an investment recommendation.
            
            Note: When calculating final price targets, give slightly more weight to the Left Brain's predictions.""",

            expected_output=f"""Produce a final investment report with the following structure:

            1. Left Brain Analysis Summary:
            - Key findings from quantitative analysis
            - Left Brain 6-month and 12-month price targets

            2. Right Brain Analysis Summary:
            - Key insights from qualitative analysis
            - Right Brain 6-month and 12-month price targets

            3. Integrated Analysis:
            - Synthesis of quantitative and qualitative factors
            - Reconciliation of any discrepancies between Left and Right Brain analyses
            - Key drivers for potential stock performance
            - Comprehensive risk assessment and potential upsides

            4. Conclusion:
            - [6MONTH_PRICE_TARGET]: $XX.XX
            - [12MONTH_PRICE_TARGET]: $XX.XX
            - [INVESTMENT_RECOMMENDATION]: Buy/Hold/Sell (Confidence: Low/Medium/High)
            - Explanation of final price targets and recommendation
            - Final thoughts on risk-reward profile

            CRITICAL: Ensure all price targets and the investment recommendation are clearly tagged as shown above. The report will be considered incomplete without these tags.""",
            agent=agent,
            context=context,
            output_file="final_recommendation_report.md",
        )