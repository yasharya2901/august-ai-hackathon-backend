from crewai import Crew, Process
from agents import blood_report_analyst, researcher, blood_report_checker, specialist_finder
from tasks import report_analyze_task, research_task, blood_report_checking_task, find_specialists_task
import os

def run_crew(file_path, city, state, country):
    """
    Executes the crewAI process on the provided blood report PDF file.

    Args:
        file_path (str): The path to the blood report PDF file.

    Returns:
        dict: The result of the crewAI process, containing analysis and recommendations.
    """
    # Initialize the Crew with the defined agents and tasks
    crew = Crew(
        agents=[blood_report_checker, blood_report_analyst, researcher, specialist_finder],
        tasks=[blood_report_checking_task, report_analyze_task, research_task, find_specialists_task],
        process=Process.sequential,
        verbose=True  # Verbose mode for detailed output
    )
    
    # Ensure the file path is correct and the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at {file_path} was not found.")

    # Execute the Crew process with the blood report as input
    result = crew.kickoff(inputs={'blood_report': file_path, 'city':city, 'state': state, 'country': country})
    
    return result

run_crew("sample_blood_report.pdf", "E-city Phase 1, Bangalore", "Karnataka", "India")