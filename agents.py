## Importing libraries and files
import os

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise ImportError(
        "python-dotenv is required for loading .env files. "
        "Install it with `pip install python-dotenv`."
    ) from e

load_dotenv()

try:
    from crewai import Agent
except ImportError as e:
    raise ImportError(
        "crewai is required for the agents. "
        "Install it with `pip install crewai`."
    ) from e

from langchain_openai import ChatOpenAI

from tools import search_tool, FinancialDocumentTool

### Loading LLM - Fixed: Properly initialize LLM with OpenAI
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate, data-driven financial analysis based on the query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a highly experienced financial analyst with 15+ years in investment banking and equity research. "
        "You specialize in analyzing corporate financial statements, identifying key financial metrics, and providing "
        "objective investment insights. You follow strict analytical frameworks and always base your recommendations "
        "on concrete data from financial documents. You understand financial ratios, cash flow analysis, and market trends. "
        "You provide balanced, well-researched investment advice that considers both opportunities and risks. "
        "You adhere to all regulatory compliance standards and never make recommendations without proper data support."
    ),
    tools=[FinancialDocumentTool],
    llm=llm,
    max_iter=15,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Accurately verify and validate financial documents to ensure they contain legitimate financial data and meet analysis requirements.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous document verification specialist with expertise in financial compliance and data validation. "
        "You have worked in regulatory compliance for major financial institutions and understand document standards. "
        "You carefully examine documents to verify they are legitimate financial reports with proper data structure. "
        "You check for required financial metrics, proper formatting, and data integrity. "
        "You flag any inconsistencies or missing critical information needed for proper financial analysis."
    ),
    tools=[FinancialDocumentTool],
    llm=llm,
    max_iter=10,
    max_rpm=10,
    allow_delegation=True
)

# Creating investment advisor agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide evidence-based investment recommendations based on thorough financial document analysis.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified investment advisor (CFA) with deep expertise in portfolio management and investment strategy. "
        "You analyze financial documents to identify genuine investment opportunities based on fundamental analysis. "
        "You consider risk-adjusted returns, market conditions, and investor profiles when making recommendations. "
        "You follow SEC regulations and fiduciary standards, always prioritizing client interests. "
        "You provide balanced recommendations that consider both growth potential and risk management. "
        "You never recommend investments without proper due diligence and always disclose relevant risks."
    ),
    tools=[FinancialDocumentTool, search_tool],
    llm=llm,
    max_iter=15,
    max_rpm=10,
    allow_delegation=False
)

# Creating risk assessor agent
risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Conduct comprehensive risk analysis using established financial risk frameworks and methodologies.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with expertise in financial risk assessment and portfolio analysis. "
        "You use established frameworks like Value at Risk (VaR), stress testing, and scenario analysis. "
        "You identify both systematic and unsystematic risks in investment opportunities. "
        "You understand market risk, credit risk, liquidity risk, and operational risk factors. "
        "You provide balanced risk assessments that help investors make informed decisions. "
        "You follow industry best practices and regulatory guidelines for risk disclosure."
    ),
    tools=[FinancialDocumentTool, search_tool],
    llm=llm,
    max_iter=15,
    max_rpm=10,
    allow_delegation=False
)
