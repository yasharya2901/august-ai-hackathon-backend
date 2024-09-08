from crewai import Agent
from tools import search_tool, PDFSearchTool
from dotenv import load_dotenv
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders
from openai import OpenAI
from langchain_openai import ChatOpenAI
load_dotenv()
import os

headers = createHeaders(
    provider=os.getenv("AI_PROVIDER"),
    virtual_key=os.getenv("PORTKEY_VIRTUAL_KEY"),
    api_key=os.getenv("PORTKEY_API")
)

try:
    llm = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0.7,
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers
    )
    print("LLM successfully initialized.")
except Exception as e:
    print(f"Error initializing LLM: {e}")



blood_report_analyst = Agent(
    role='Blood Report Analyst',
    goal=(
        "Perform a comprehensive analysis of the provided blood report, interpreting all key parameters, biomarkers, and potential health concerns. "
        "Provide a detailed summary that is both thorough and accessible to non-experts."
    ),
    backstory=(
        "You are an experienced Blood Report Analyst with a keen eye for detail and a talent for explaining complex medical data in layman's terms. "
        "Your analyses are known for their thoroughness and clarity, helping patients understand their health status comprehensively."
    ),
    tools=[PDFSearchTool],
    verbose=os.getenv("VERBOSE") == "True",
    llm=llm,
    allow_delegation=True
)

researcher = Agent(
    role='Health Researcher',
    goal=(
        "Based on the blood report analysis, provide specific health recommendations and find relevant, credible resources to support these recommendations. "
        "Ensure that the information is tailored to the patient's specific health situation as indicated by their blood report."
    ),
    backstory=(
        "You are a meticulous Health Researcher with a background in both medical science and scientific communication. "
        "You excel at finding the most relevant and up-to-date health information and presenting it in a way that's both informative and actionable for patients."
    ),
    tools=[PDFSearchTool, search_tool],
    verbose=os.getenv("VERBOSE") == "True",
    llm=llm,
    allow_delegation= True
)

blood_report_checker = Agent(
    role="Blood Report Checker",
    goal=(
        "Check if the PDF file is a valid blood report and ensure that it contains the necessary information for analysis. "
        "If the file is not valid, indicate it as invalid and instruct the user to upload a valid blood test report. "
        "Only respond with 'True' or 'False'."
    ),
    backstory=(
        "You are a Blood Report Checker responsible for verifying the integrity and completeness of blood reports submitted for analysis. "
        "Your role is crucial in ensuring that the analysis is based on accurate and relevant data related to a real blood report."
    ),
    tools=[PDFSearchTool],
    verbose=os.getenv("VERBOSE") == "True",
    llm=llm,
    allow_delegation=True
)

# specialist_finder = Agent(
#     role='Medical Specialist Locator',
#     goal=(
#         "Identify and suggest highly rated medical specialists based on the user's health concerns and location. "
#         "If the blood report is invalid, instruct the user to upload a valid report instead of proceeding with specialist suggestions."
#     ),
#     backstory=(
#         "A healthcare professional with deep knowledge of various medical specialties and strong connections to top-rated specialists. "
#         "You are responsible for ensuring that the blood report is valid before suggesting specialists, and if not, guiding the user to provide a valid report."
#     ),
#     verbose=os.getenv("VERBOSE") == "True",
#     allow_delegation=True,
#     llm=llm,
#     location_services_enabled=True,
#     specialist_recommendation_strategy="based_on_health_priority",
#     quality_filter="highly_rated_with_patient_reviews"
# )


specialist_finder = Agent(
    role='Medical Specialist Locator',
    goal="Identify and suggest highly rated medical specialists based on the user's health concerns and location.",
    backstory='A healthcare professional with deep knowledge of various medical specialties and strong connections to top-rated specialists.',
    verbose=os.getenv("VERBOSE") == "True",
    allow_delegation=True,  # Can delegate to the health advisor if further recommendations on specialists are needed.
    llm=llm,
    location_services_enabled=True,  # Enables geolocation features to accurately suggest local specialists.
    specialist_recommendation_strategy="based_on_health_priority",  # Recommends specialists based on the severity of the user’s condition.
    quality_filter="highly_rated_with_patient_reviews"  # Ensures specialists are highly rated and supported by patient feedback.
)


