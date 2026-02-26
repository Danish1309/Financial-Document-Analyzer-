## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a task to analyze financial document - Fixed: Proper description and expected output
analyze_financial_document = Task(
    description="""Analyze the financial document to address the user's query: {query}
    
    Your analysis should:
    1. Read and thoroughly understand the financial document provided
    2. Extract key financial metrics, ratios, and performance indicators
    3. Identify trends, strengths, and weaknesses in the financial data
    4. Provide objective, data-driven insights based on the document
    5. Address the specific aspects mentioned in the user's query
    6. Use reliable sources and cite any external market data when relevant
    
    Base all recommendations on concrete evidence from the financial document.""",

    expected_output="""A comprehensive financial analysis report that includes:
    
    1. Executive Summary
       - Brief overview of the financial document analyzed
       - Key findings and main insights
    
    2. Financial Metrics Analysis
       - Revenue and profitability trends
       - Key financial ratios (liquidity, solvency, profitability)
       - Balance sheet strength
       - Cash flow analysis
    
    3. Market Position & Competitive Analysis
       - Company's market position
       - Competitive advantages or challenges
       - Industry context and comparisons
    
    4. Risk Factors
       - Identified financial risks
       - Market and operational risks
       - Risk mitigation strategies
    
    5. Investment Insights
       - Data-driven investment perspective
       - Key considerations for investors
       - Relevant market research and sources (with valid URLs)
    
    Format: Clear, structured analysis with proper headings and bullet points where appropriate.
    All claims must be supported by data from the financial document or reliable external sources.""",

    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating a document verification task - Fixed: Proper verification process
verification_task = Task(
    description="""Verify the financial document to ensure it contains legitimate financial data.
    
    Your verification should:
    1. Confirm the document is a valid financial report (quarterly/annual report, financial statement, etc.)
    2. Check for presence of key financial sections (balance sheet, income statement, cash flow)
    3. Validate data completeness and format
    4. Identify any missing critical financial information
    5. Flag any inconsistencies or data quality issues
    
    Provide a clear verification status and any concerns.""",

    expected_output="""A verification report containing:
    
    1. Document Type Identification
       - Type of financial document (10-K, 10-Q, earnings report, etc.)
       - Reporting period covered
    
    2. Completeness Check
       - Presence of key financial statements
       - Availability of required metrics
       - Data quality assessment
    
    3. Verification Status
       - VERIFIED or REQUIRES ATTENTION
       - List of any missing or incomplete sections
       - Recommendations for additional data if needed
    
    Format: Structured verification report with clear status indicators.""",

    agent=verifier,  # Fixed: Correct agent assignment
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Creating an investment analysis task - Fixed: Professional investment analysis
investment_analysis_task = Task(
    description="""Provide evidence-based investment recommendations based on the financial document analysis.
    
    Your analysis should:
    1. Review key financial metrics and performance indicators
    2. Assess the company's financial health and growth potential
    3. Consider current market conditions and industry trends
    4. Evaluate risk-adjusted return potential
    5. Provide balanced recommendations with clear reasoning
    6. Consider different investor profiles (conservative, moderate, aggressive)
    
    User query context: {query}""",

    expected_output="""An investment recommendation report including:
    
    1. Investment Thesis
       - Core investment argument based on financial analysis
       - Key strengths supporting the investment case
       - Main concerns or weaknesses
    
    2. Valuation Assessment
       - Key valuation metrics (P/E, P/B, EV/EBITDA, etc.)
       - Comparison to industry peers
       - Fair value assessment
    
    3. Growth Prospects
       - Revenue and earnings growth potential
       - Market expansion opportunities
       - Competitive positioning
    
    4. Investment Recommendation
       - Clear recommendation (Strong Buy, Buy, Hold, Sell, Strong Sell)
       - Target price or valuation range (if applicable)
       - Investment timeframe
       - Suitable investor profile
    
    5. Key Risks and Considerations
       - Main investment risks
       - Factors that could change the recommendation
    
    6. Supporting Research
       - Relevant market data and industry reports
       - Valid URLs to reputable financial sources
    
    Format: Professional investment report with clear structure and data-backed recommendations.""",

    agent=investment_advisor,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task - Fixed: Comprehensive risk analysis
risk_assessment_task = Task(
    description="""Conduct a thorough risk assessment of the investment opportunity based on the financial document.
    
    Your assessment should:
    1. Identify and categorize all material risks (financial, operational, market, regulatory)
    2. Assess the severity and likelihood of each risk
    3. Evaluate risk management strategies in place
    4. Consider macroeconomic and industry-specific risk factors
    5. Provide risk mitigation recommendations
    6. Use established risk assessment frameworks
    
    User query context: {query}""",

    expected_output="""A comprehensive risk assessment report containing:
    
    1. Risk Overview
       - Overall risk rating (Low, Moderate, High, Very High)
       - Summary of key risk factors
    
    2. Financial Risks
       - Liquidity risk assessment
       - Leverage and solvency concerns
       - Earnings volatility and sustainability
       - Cash flow risks
    
    3. Operational Risks
       - Business model risks
       - Management and governance concerns
       - Operational efficiency issues
    
    4. Market Risks
       - Market volatility exposure
       - Competition and market share risks
       - Industry disruption potential
       - Macroeconomic sensitivities
    
    5. Regulatory and Legal Risks
       - Compliance and regulatory concerns
       - Legal exposure
       - ESG (Environmental, Social, Governance) risks
    
    6. Risk Mitigation Strategies
       - Recommended risk management approaches
       - Hedging strategies (if applicable)
       - Portfolio diversification considerations
       - Monitoring metrics and warning signs
    
    7. Risk-Adjusted Return Analysis
       - Risk vs. return tradeoff assessment
       - Comparison to risk-free and benchmark returns
    
    Format: Detailed risk report with clear categorization and actionable insights.""",

    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)
