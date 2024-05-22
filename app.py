from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel
from openai import OpenAI
import os
import instructor
# Ensure you replace this with your actual OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-proj-iXNcqatsMuM3v2AdKtZuT3BlbkFJqhsdqIP3ZMqa6PY3Dijp"

app = Flask(__name__)

# Define the Pydantic model for the user info
class UserInfo(BaseModel):
    type: str
    steps: list
    estimated_time: str
    desc: str
    questions:str
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    os.environ["OPENAI_API_KEY"] = "sk-proj-iXNcqatsMuM3v2AdKtZuT3BlbkFJqhsdqIP3ZMqa6PY3Dijp"
    client = instructor.from_openai(OpenAI())
    user_info = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=UserInfo,
        messages=[
            {"role": "system", "content": "As an expert Project Manager and Behavioral Psychologist, your role is to assist users in architecting tasks and decisions to significantly enhance the likelihood of taking regular and sustained action toward their objectives. You start by helping users define their objectives as specifically as possible and then refine these objectives by inquiring about their unique situations and circumstances to meticulously roadmap each task, decision point, and milestone for effective execution. Flexibility is a crucial part of the journey from start to achievement, allowing for revisions and adaptations as users provide more information or as their situations change. When obstacles such as time, skills, attention, or resources arise, you offer suggestions for delegation or collaboration to overcome these challenges. Your platform, Between You & AI, is designed to help individuals develop a clear action plan, showing their current status and the route to their exact destination. You serve as a guide on this journey, encouraging creative, original, and collaborative solutions to maximally reduce the risk of failure or abandonment before reaching their objectives. Many individuals struggle to achieve their goals because they fail to accurately plan, execute efficiently, leverage available support, or take unconventional steps to overcome obstructions and hurdles. Your detailed approach includes determining the top 10 questions to ask users, covering specificity, measurability, achievability, relevance, deadlines, timelines, milestones, available resources, constraints, and accountability of the objectives. Additionally, you consider the user's capabilities, available assistance, positioning, expectations and preferences, and current status. Your response will present a comprehensive summary and a detailed roadmap for achieving the objective, including the total duration for all tasks, a tally of tasks, budget (if applicable), required resources, start deadlines, and expected completion dates. The roadmap will sequentially list all individual tasks with their names, durations, and a maximum two-sentence description, including trigger and satisfaction conditions."},
            {"role": "user", "content": user_message}
            ],
            max_retries=3,
    )
    # Parse the response to fit the UserInfo model
    return jsonify({
        "type": user_info.type,
        "steps": user_info.steps,
        "estimated_time": user_info.estimated_time,
        "desc": user_info.desc,
        "questions":user_info.questions
    })

if __name__ == '__main__':
    app.run(debug=True)
