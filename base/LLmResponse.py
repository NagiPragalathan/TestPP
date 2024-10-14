import json
from langchain.prompts import PromptTemplate
from g4f import models, Provider
from LLM.MyLLM import G4FLLM
from langchain.llms.base import LLM

# LLM setup
def llm() -> LLM:
    return G4FLLM(
        model=models.gpt_4o,
        provider=Provider.Chatgpt4o
    )

# Direct function to rank colleges based on a given goal
def rank_colleges(college_data, user_goal):
    connector = llm()
    
    # Define the prompt template
    prompt_template = """
    Below is a list of colleges with their details in JSON format:
    {college_data}
    
    The user has the following goal: "{user_goal}"
    
    Please analyze these colleges based on factors such as infrastructure, placements, faculty quality, student satisfaction, and research output. Additionally, provide a percentage estimation of how well the user's goal can be achieved by choosing each college. Suggest suitable courses and colleges based on the user's goal description. Provide the output in JSON format, including the rankings, reasons for each ranking, goal achievement percentages, and course suggestions.
    Note: the output should be in JSON not readme and dont need the summary dont use ```json this quotes too.  Please use the following format: 
    [
        [
            "college": "",
            "ranking": number,
            "reasons": [
                "infrastructure": "",
                "placements": "",
                "faculty_quality": "",
                "student_satisfaction": ",
                "research_output": ""
            ],
            "goal_achievement_percentage": number,
            "course_suggestions": ["", "", ""]
        ],
    ]

    """
    
    # Create a formatted prompt using the data
    prompt = PromptTemplate(
        input_variables=["college_data", "user_goal"],
        template=prompt_template
    ).format(college_data=json.dumps(college_data, indent=2), user_goal=user_goal)
    
    # Run the LLM with the prompt
    response = connector.invoke(input=prompt)
    
    print(response)
    
    # Assuming the LLM returns a string that can be parsed into a JSON object
    try:
        json_response = json.loads(response)
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON response"}
    
    return json_response

# Example usage
if __name__ == "__main__":
    # Sample JSON data representing colleges
    college_data = [
        {
            "name": "Jaya Engineering College",
            "location": "Chennai"
        },
        {
            "name": "IIT Chennai",
            "location": "Chennai"
        }
    ]

    # User goal description
    user_goal = "To pursue a career in computer science with a focus on research opportunities"

    # Get the ranking result
    ranking_result = rank_colleges(college_data, user_goal)

    # Print the resulting JSON ranking
    print(json.dumps(ranking_result, indent=2))
