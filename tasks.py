from crewai import Task
from tools import search_tool, PDFSearchTool
from agents import blood_report_analyst, researcher, blood_report_checker, specialist_finder

report_analyze_task = Task(
    description=(
        "Proceed only if the provided {blood_report} is a valid blood report."
        "Thoroughly analyze the provided {blood_report}. Focus on all key parameters, biomarkers, and potential health issues. "
        "For each parameter, explain its significance, normal range, and any deviations observed. "
        "Summarize the potential health implications, making sure to explain each in an accessible manner."
    ),
    expected_output=(
        "The output should be a comprehensive and structured summary that includes:\n"
        "1. **Introduction**: Brief overview of the report.\n"
        "2. **Key Parameters**: Detailed analysis of each parameter, including normal ranges and explanations.\n"
        "3. **Abnormal Findings**: Specific sections highlighting any abnormalities with detailed descriptions.\n"
        "4. **Health Implications**: Explanation of potential health issues based on the findings.\n"
        "5. **Critical Alerts**: Identification of any critical issues that need immediate attention.\n"
        "The final report should be professional, clear, and accessible to non-experts."
    ),
    tools=[PDFSearchTool],
    agent=blood_report_analyst,
    output_file='blood_report_summary12.md'
)

research_task = Task(
    description=(
        "Proceed only if the provided {blood_report} is a valid blood report."
        "Conduct thorough research based on the {blood_report} analysis to provide targeted health recommendations and relevant resources. "
        "The research should be comprehensive, evidence-based, and directly related to the critical health issues identified in the blood report.\n"
        "Steps to follow:\n"
        "1. Carefully review the blood report summary to identify the most critical health issues and abnormalities.\n"
        "2. For each identified issue, research and compile a list of specific, actionable health recommendations that address these issues.\n"
        "3. Locate credible, peer-reviewed articles, medical guidelines, or authoritative resources that support each recommendation.\n"
        "4. Summarize each resource, explaining its content, relevance, and how it supports the recommendation based on the blood report findings.\n"
        "5. Ensure all recommendations are practical and easy for the patient to implement."
    ),
    expected_output=(
        "The final output should be a detailed, well-structured report that includes:\n"
        "1. **Critical Health Issues**: A list of key health issues identified from the blood report, with a brief explanation for each.\n"
        "2. **Health Recommendations**: Specific, evidence-based health recommendations for each issue, presented in a clear, actionable format.\n"
        "3. **Supporting Resources**: For each recommendation, provide 1-3 high-quality, credible resources, including:\n"
        "   - A direct link to the article or resource\n"
        "   - A concise summary of the article's content\n"
        "   - An explanation of the article's relevance to the patient's blood report findings and the corresponding recommendation\n"
        "4. **Conclusion**: A final summary highlighting the key actions the patient should prioritize based on the research findings."
    ),
    agent=researcher,
    tools=[PDFSearchTool, search_tool],
    output_file='blood_report_recommendations12.md'
)


# blood_report_checking_task = Task(
#     description=(
#         "Check if the provided {blood_report} is a valid blood report and contains the necessary information for analysis. "
#         ""
#         "If the file is not a valid blood report, provide feedback to the user."
#     ),
#     expected_output=(
#         "The output should be a boolean value indicating whether the file is a valid blood report or not. "
#         "If the file is valid, the output should be True; otherwise, it should be False."
#     ),
#     tools=[PDFSearchTool],
#     agent=blood_report_checker
# )


blood_report_checking_task = Task(
    description=(
        "Check if the provided {blood_report} is a valid blood report and contains the necessary information for analysis. "
        "If the file is not a valid blood report, indicate that it is invalid and request the user to upload a valid blood report."
    ),
    expected_output=(
        "The output should be a boolean value indicating whether the file is a valid blood report or not:\n"
        "1. **Valid**: Return 'True'.\n"
        "2. **Invalid**: Return 'False' with a prompt to 'Please upload a valid blood test report.'"
    ),
    tools=[PDFSearchTool],
    agent=blood_report_checker
)


find_specialists_task = Task(
        description=(
        "Based on the blood test analysis and health concerns, suggest appropriate medical specialists near the user. "
        "1. Identify key health issues from the blood test report. "
        "2. Determine the most relevant medical specialists for addressing these issues. "
        "3. Use the provided location ({city}, {state}, {country}) to find nearby specialists: "
        "- Provide 2-3 highly rated specialists for each concern. "
        "- Include name, contact info, and a brief description of their expertise. "
        "- If found, also mention the phone number and email to contact the specialists"
        "Ensure the recommendations are easy to understand and actionable."
        ),
        expected_output='A list of recommended specialists in the user\'s location with explanations of their relevance.',
        agent=specialist_finder,
        context=[research_task, report_analyze_task],
        output_file='specialists_recommendations12.md'
    )