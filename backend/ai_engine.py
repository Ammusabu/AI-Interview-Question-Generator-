import openai

openai.api_key = "YOUR_API_KEY"

def generate_questions(role, skills, level):
    prompt = f"""
    Generate 5 {level} interview questions for a {role}
    focusing on the following skills: {', '.join(skills)}.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
