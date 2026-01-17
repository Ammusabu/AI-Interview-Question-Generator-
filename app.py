import gradio as gr
import requests
import json
from typing import Dict, List, Tuple

# Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

# Job category mapping
JOB_CATEGORIES = {
    # Software Development
    "Software Engineer": "software_dev",
    "Software Developer": "software_dev",
    "Full Stack Developer": "software_dev",
    "Frontend Developer": "frontend",
    "Backend Developer": "backend",
    "Mobile Application Developer": "mobile",
    "Web Developer": "frontend",
    "Game Developer": "gaming",
    "Embedded Systems Engineer": "embedded",
    
    # Data, AI & ML
    "Data Scientist": "data_science",
    "Data Analyst": "data_analysis",
    "Machine Learning Engineer": "ml_engineer",
    "AI Engineer": "ai_engineer",
    "Deep Learning Engineer": "ml_engineer",
    "NLP Engineer": "nlp",
    "Computer Vision Engineer": "computer_vision",
    "Business Intelligence Analyst": "bi",
    "Big Data Engineer": "big_data",
    "Data Engineer": "data_engineering",
    
    # Cybersecurity
    "Cybersecurity Analyst": "cybersecurity",
    "Information Security Engineer": "cybersecurity",
    "Ethical Hacker": "pentesting",
    "Penetration Tester": "pentesting",
    "Network Engineer": "networking",
    "Network Security Engineer": "cybersecurity",
    "SOC Analyst": "soc",
    
    # Cloud & DevOps
    "Cloud Engineer": "cloud",
    "Cloud Solutions Architect": "cloud_arch",
    "DevOps Engineer": "devops",
    "Site Reliability Engineer (SRE)": "sre",
    "Systems Engineer": "systems",
    
    # Database & Systems
    "Database Administrator (DBA)": "database",
    "Systems Programmer": "systems",
    
    # Product & Testing
    "QA Engineer / Software Tester": "qa",
    "Automation Test Engineer": "automation",
    "Technical Product Manager": "product",
    
    # Emerging Tech
    "Blockchain Developer": "blockchain",
    "AR/VR Developer": "ar_vr",
    "IoT Engineer": "iot",
    "Robotics Software Engineer": "robotics",
}

# Level-specific question modifiers
LEVEL_MODIFIERS = {
    "Entry/Junior": {
        "focus": ["fundamentals", "basic concepts", "learning ability", "willingness to learn"],
        "depth": "basic",
        "experience": "0-2 years"
    },
    "Mid-Level": {
        "focus": ["practical application", "project experience", "problem-solving", "collaboration"],
        "depth": "intermediate",
        "experience": "2-5 years"
    },
    "Senior": {
        "focus": ["architecture", "mentoring", "system design", "technical leadership", "best practices"],
        "depth": "advanced",
        "experience": "5-8+ years"
    },
    "Lead/Principal": {
        "focus": ["strategy", "technical vision", "team leadership", "cross-functional collaboration", "innovation"],
        "depth": "expert",
        "experience": "8+ years"
    }
}

def get_level_specific_questions(role: str, skills: str, level: str, category: str) -> List[str]:
    """Generate level-specific questions for each category"""
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    level_info = LEVEL_MODIFIERS.get(level, LEVEL_MODIFIERS["Mid-Level"])
    
    # Category-specific questions with level adjustments
    if category in ["software_dev", "frontend", "backend", "mobile"]:
        if level == "Entry/Junior":
            return [
                f"1. Explain the difference between {skills_list[0] if skills_list else 'object-oriented'} and procedural programming.",
                f"2. Walk me through how you would debug a simple application issue.",
                f"3. What version control system have you used and how do you write good commit messages?",
                f"4. Explain basic data structures like arrays, lists, and when to use each.",
                f"5. How do you approach learning a new programming language or framework?"
            ]
        elif level == "Mid-Level":
            return [
                f"1. Design a REST API for a {skills_list[0] if skills_list else 'typical'} application and explain your choices.",
                f"2. How do you optimize application performance and handle scaling issues?",
                f"3. Describe your experience with testing frameworks and writing maintainable tests.",
                f"4. Explain how you would refactor legacy code while maintaining functionality.",
                f"5. What design patterns have you implemented and what problems did they solve?"
            ]
        elif level == "Senior":
            return [
                f"1. Design a scalable microservices architecture for a high-traffic application.",
                f"2. How do you establish coding standards and ensure code quality across teams?",
                f"3. Describe your approach to mentoring junior developers and code reviews.",
                f"4. How do you make technical decisions that balance business needs and technical debt?",
                f"5. What's your strategy for leading a technical migration or major refactoring?"
            ]
        else:  # Lead/Principal
            return [
                f"1. Define technical vision and architecture roadmap for a complex product suite.",
                f"2. How do you align engineering initiatives with business strategy and OKRs?",
                f"3. Describe your approach to building and scaling high-performing engineering teams.",
                f"4. How do you evaluate new technologies and make build vs. buy decisions?",
                f"5. What metrics do you track to measure engineering productivity and system health?"
            ]
    
    elif category in ["data_science", "ml_engineer", "ai_engineer"]:
        if level == "Entry/Junior":
            return [
                f"1. Explain basic ML concepts like overfitting, underfitting, and cross-validation.",
                f"2. How do you handle missing data in a dataset?",
                f"3. Describe the difference between supervised and unsupervised learning.",
                f"4. What libraries have you used for data analysis and visualization?",
                f"5. Walk me through a simple linear regression model implementation."
            ]
        elif level == "Mid-Level":
            return [
                f"1. How do you select the right algorithm for a given business problem?",
                f"2. Describe your process for feature engineering and selection.",
                f"3. How do you evaluate model performance beyond accuracy (precision, recall, F1)?",
                f"4. Explain techniques for handling imbalanced datasets.",
                f"5. What's your experience with model deployment and monitoring?"
            ]
        elif level == "Senior":
            return [
                f"1. Design an end-to-end ML pipeline for a production system.",
                f"2. How do you establish MLOps practices and model governance?",
                f"3. Describe your approach to A/B testing and model experimentation.",
                f"4. How do you mentor junior data scientists and establish best practices?",
                f"5. What strategies do you use for model explainability and fairness?"
            ]
        else:  # Lead/Principal
            return [
                f"1. Define AI/ML strategy aligned with business objectives.",
                f"2. How do you build and scale data science teams and capabilities?",
                f"3. Design a data platform that supports ML at enterprise scale.",
                f"4. How do you measure ROI and business impact of ML initiatives?",
                f"5. What's your approach to ethical AI and responsible machine learning?"
            ]
    
    elif category in ["cybersecurity", "pentesting", "soc"]:
        if level == "Entry/Junior":
            return [
                f"1. Explain basic security concepts: CIA triad, defense in depth.",
                f"2. What common vulnerabilities should every developer know about?",
                f"3. How do you stay updated with security news and threats?",
                f"4. Describe basic network security concepts (firewalls, VPNs).",
                f"5. What tools have you used for vulnerability scanning?"
            ]
        elif level == "Mid-Level":
            return [
                f"1. How do you conduct a security assessment of a web application?",
                f"2. Describe your experience with SIEM tools and log analysis.",
                f"3. How do you handle a security incident from detection to resolution?",
                f"4. Explain different types of encryption and when to use each.",
                f"5. What's your approach to security monitoring and alerting?"
            ]
        elif level == "Senior":
            return [
                f"1. Design a comprehensive security program for an organization.",
                f"2. How do you build and lead incident response teams?",
                f"3. Describe your approach to security architecture and secure SDLC.",
                f"4. How do you establish security metrics and report to executives?",
                f"5. What's your strategy for third-party risk management?"
            ]
        else:  # Lead/Principal
            return [
                f"1. Develop enterprise-wide cybersecurity strategy and roadmap.",
                f"2. How do you align security initiatives with business objectives?",
                f"3. Design a security operations center (SOC) for a global organization.",
                f"4. How do you manage security compliance across multiple regulations?",
                f"5. What's your approach to security culture and awareness programs?"
            ]
    
    elif category in ["devops", "cloud", "sre"]:
        if level == "Entry/Junior":
            return [
                f"1. Explain basic concepts: containers, VMs, and their differences.",
                f"2. What's your experience with basic Linux administration?",
                f"3. How do you write a simple Dockerfile and docker-compose file?",
                f"4. Describe basic CI/CD concepts and why they're important.",
                f"5. What monitoring tools have you used?"
            ]
        elif level == "Mid-Level":
            return [
                f"1. Design a CI/CD pipeline for a microservices application.",
                f"2. How do you implement Infrastructure as Code?",
                f"3. Describe your experience with container orchestration.",
                f"4. How do you ensure high availability and disaster recovery?",
                f"5. What's your approach to monitoring and alerting?"
            ]
        elif level == "Senior":
            return [
                f"1. Design cloud architecture for a globally distributed application.",
                f"2. How do you establish SLOs, SLIs, and error budgets?",
                f"3. Describe your approach to cost optimization in cloud environments.",
                f"4. How do you mentor junior engineers and establish DevOps practices?",
                f"5. What's your strategy for platform engineering and internal tools?"
            ]
        else:  # Lead/Principal
            return [
                f"1. Define cloud and platform strategy for an enterprise.",
                f"2. How do you build and scale platform engineering teams?",
                f"3. Design a multi-cloud strategy with cost and performance optimization.",
                f"4. How do you measure and improve developer productivity?",
                f"5. What's your approach to platform reliability and incident management?"
            ]
    
    elif category in ["database"]:
        if level == "Entry/Junior":
            return [
                f"1. Explain basic SQL concepts: joins, indexes, transactions.",
                f"2. How do you write efficient SELECT queries?",
                f"3. What's the difference between SQL and NoSQL databases?",
                f"4. How do you backup and restore a database?",
                f"5. What tools have you used for database administration?"
            ]
        elif level == "Mid-Level":
            return [
                f"1. How do you optimize slow-running queries?",
                f"2. Design a database schema for a typical e-commerce application.",
                f"3. Describe your experience with database replication.",
                f"4. How do you implement database security and access controls?",
                f"5. What's your approach to database performance monitoring?"
            ]
        elif level == "Senior":
            return [
                f"1. Design database architecture for a high-traffic application.",
                f"2. How do you plan and execute database migrations?",
                f"3. Describe your approach to database capacity planning.",
                f"4. How do you establish database standards and best practices?",
                f"5. What's your strategy for data lifecycle management?"
            ]
        else:  # Lead/Principal
            return [
                f"1. Define data architecture strategy for an enterprise.",
                f"2. How do you build and lead database engineering teams?",
                f"3. Design a data platform supporting multiple business units.",
                f"4. How do you align database strategy with business goals?",
                f"5. What's your approach to data governance and quality?"
            ]
    
    # Default questions for other categories
    if level == "Entry/Junior":
        return [
            f"1. What attracts you to this {role} position?",
            f"2. Describe your educational background and relevant coursework.",
            f"3. What projects have you completed using {skills_list[0] if skills_list else 'relevant skills'}?",
            f"4. How do you approach learning new technologies?",
            f"5. Where do you see yourself in 3 years in this field?"
        ]
    elif level == "Mid-Level":
        return [
            f"1. Describe a challenging project where you used {skills_list[0] if skills_list else 'key skills'}.",
            f"2. How do you collaborate with team members on technical projects?",
            f"3. What's your process for troubleshooting complex issues?",
            f"4. How do you stay current with industry trends?",
            f"5. Describe a time you improved an existing process or system."
        ]
    elif level == "Senior":
        return [
            f"1. How do you mentor and develop junior team members?",
            f"2. Describe a technical decision you made that significantly impacted the business.",
            f"3. How do you balance technical debt with new feature development?",
            f"4. What's your approach to architectural design and documentation?",
            f"5. How do you handle conflicting priorities in technical projects?"
        ]
    else:  # Lead/Principal
        return [
            f"1. How do you develop and communicate technical vision?",
            f"2. Describe your experience building and leading high-performing teams.",
            f"3. How do you align technical strategy with business objectives?",
            f"4. What's your approach to stakeholder management and communication?",
            f"5. How do you drive innovation while maintaining system stability?"
        ]

def generate_questions(role, skills, level, use_api=True):
    """Generate interview questions using API or fallback"""
    if not role or not skills:
        return "Please enter both job role and skills."
    
    # Get category
    category = JOB_CATEGORIES.get(role, "default")
    category_name = get_category_name(category)
    
    if use_api:
        try:
            # Build level-specific prompt
            level_info = LEVEL_MODIFIERS.get(level, {})
            prompt = f"""
            Generate 5 interview questions for a {role} position at {level} level.
            Focus areas: {', '.join(level_info.get('focus', ['technical skills', 'problem-solving']))}
            Required skills: {skills}
            Experience level: {level_info.get('experience', 'relevant experience')}
            Questions should test {level_info.get('depth', 'appropriate')} knowledge.
            
            Format each question clearly with a number.
            Make questions specific to {category_name} role.
            """
            
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 300,
                        "temperature": 0.8,
                        "do_sample": True,
                        "top_k": 50
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        questions = result[0]["generated_text"].strip()
                        return format_questions(questions, role, category)
            
            # If API fails, use enhanced fallback
            return generate_enhanced_fallback(role, skills, level, category)
            
        except Exception as e:
            print(f"API Error: {e}")
            return generate_enhanced_fallback(role, skills, level, category)
    else:
        return generate_enhanced_fallback(role, skills, level, category)

def generate_enhanced_fallback(role: str, skills: str, level: str, category: str) -> str:
    """Generate enhanced level-specific fallback questions"""
    questions = get_level_specific_questions(role, skills, level, category)
    
    category_name = get_category_name(category)
    level_display = level.replace("/", " ").title()
    
    header = f"📋 {level_display} Level Interview Questions for {role}\n"
    header += f"🏷️ Category: {category_name}\n"
    header += f"💼 Required Skills: {skills}\n"
    header += "=" * 60 + "\n\n"
    
    # Add level-specific advice
    advice = get_level_specific_advice(level)
    
    return header + "\n\n".join(questions) + "\n\n" + advice

def get_level_specific_advice(level: str) -> str:
    """Get level-specific interview advice"""
    if level == "Entry/Junior":
        return "💡 Junior Level Tips:\n• Focus on fundamentals and willingness to learn\n• Show enthusiasm and growth mindset\n• Be prepared to discuss academic projects and internships\n• Demonstrate problem-solving approach, not just answers"
    elif level == "Mid-Level":
        return "💡 Mid-Level Tips:\n• Emphasize practical experience and project contributions\n• Show ability to work independently and in teams\n• Discuss specific technical challenges and how you solved them\n• Demonstrate understanding of best practices"
    elif level == "Senior":
        return "💡 Senior Level Tips:\n• Highlight leadership and mentoring experience\n• Discuss architectural decisions and trade-offs\n• Show business impact of technical decisions\n• Demonstrate ability to establish processes and standards"
    else:  # Lead/Principal
        return "💡 Leadership Tips:\n• Emphasize strategic thinking and vision\n• Show experience building and scaling teams\n• Discuss stakeholder management and communication\n• Demonstrate business-technical alignment"

def get_category_name(category: str) -> str:
    """Get display name for category"""
    category_names = {
        "software_dev": "Software Development",
        "data_science": "Data Science",
        "ml_engineer": "Machine Learning",
        "cybersecurity": "Cybersecurity",
        "devops": "DevOps & Cloud",
        "frontend": "Frontend Development",
        "backend": "Backend Development",
        "database": "Database Administration",
        "default": "General Technology"
    }
    return category_names.get(category, "General Technology")

def format_questions(questions_text: str, role: str, category: str) -> str:
    """Format the generated questions nicely"""
    category_name = get_category_name(category)
    header = f"📋 Interview Questions for {role}\n"
    header += f"🏷️ Category: {category_name}\n"
    header += "=" * 50 + "\n\n"
    
    return header + questions_text

# Rest of the code remains the same (generate_followup_questions, interface creation, etc.)

def generate_followup_questions(role, skills, level, question_type):
    """Generate follow-up questions based on type and level"""
    level_info = LEVEL_MODIFIERS.get(level, {})
    
    type_prompts = {
        "behavioral": {
            "Entry/Junior": f"Generate 3 behavioral questions focusing on learning, adaptability, and teamwork for a {role} at {level} level",
            "Mid-Level": f"Generate 3 behavioral questions focusing on project experience, collaboration, and problem-solving for a {role} at {level} level",
            "Senior": f"Generate 3 behavioral questions focusing on leadership, mentoring, and technical guidance for a {role} at {level} level",
            "Lead/Principal": f"Generate 3 behavioral questions focusing on strategic thinking, team building, and stakeholder management for a {role} at {level} level"
        },
        "technical_depth": {
            "Entry/Junior": f"Generate 3 technical questions focusing on fundamentals and basic concepts for {role}",
            "Mid-Level": f"Generate 3 advanced technical questions diving deeper into specific skills: {skills}",
            "Senior": f"Generate 3 architectural/system design questions for {role} position",
            "Lead/Principal": f"Generate 3 strategic technical questions about technology selection and implementation for {role}"
        },
        "scenario": {
            "Entry/Junior": f"Generate 3 simple scenario-based questions testing basic problem-solving for {role}",
            "Mid-Level": f"Generate 3 realistic work scenario questions for {role} with skills: {skills}",
            "Senior": f"Generate 3 complex scenario questions involving technical leadership and decision-making",
            "Lead/Principal": f"Generate 3 strategic scenario questions involving business and technical trade-offs"
        },
        "leadership": {
            "Entry/Junior": f"Generate 3 questions about teamwork and collaboration for junior {role}",
            "Mid-Level": f"Generate 3 questions about informal leadership and mentoring for {role}",
            "Senior": f"Generate 3 leadership questions about team management and technical direction",
            "Lead/Principal": f"Generate 3 executive-level leadership questions for {role} position"
        }
    }
    
    prompt = type_prompts.get(question_type, {}).get(level, 
        f"Generate 3 {question_type} questions for a {role} at {level} level with skills: {skills}")
    
    # Fallback responses when API is not available
    fallback_responses = {
        "behavioral": get_behavioral_fallback(role, level),
        "technical_depth": get_technical_fallback(role, skills, level),
        "scenario": get_scenario_fallback(role, level),
        "leadership": get_leadership_fallback(role, level)
    }
    
    return fallback_responses.get(question_type, "Focus on practical experience and problem-solving approaches.")

def get_behavioral_fallback(role: str, level: str) -> str:
    """Fallback behavioral questions"""
    if level == "Entry/Junior":
        return "1. Describe a time you had to learn something new quickly.\n2. How do you handle feedback on your work?\n3. Tell me about a team project you worked on and your contribution."
    elif level == "Mid-Level":
        return "1. Describe a challenging project and how you overcame obstacles.\n2. How do you handle conflicting priorities?\n3. Tell me about a time you had to convince others of your technical approach."
    elif level == "Senior":
        return "1. How do you mentor junior team members?\n2. Describe a time you made a difficult technical decision.\n3. How do you handle disagreements about technical direction?"
    else:
        return "1. How do you build and maintain high-performing teams?\n2. Describe your approach to stakeholder management.\n3. How do you align technical strategy with business goals?"

def get_technical_fallback(role: str, skills: str, level: str) -> str:
    """Fallback technical questions"""
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    primary_skill = skills_list[0] if skills_list else "relevant technology"
    
    if level == "Entry/Junior":
        return f"1. Explain basic concepts of {primary_skill}.\n2. What are common use cases for {primary_skill}?\n3. How would you troubleshoot a basic issue with {primary_skill}?"
    elif level == "Mid-Level":
        return f"1. What advanced features of {primary_skill} have you used?\n2. How do you optimize performance with {primary_skill}?\n3. What are the limitations of {primary_skill} and how do you work around them?"
    elif level == "Senior":
        return f"1. Design a system architecture using {primary_skill}.\n2. How would you scale {primary_skill} for high traffic?\n3. What best practices do you enforce for {primary_skill} usage?"
    else:
        return f"1. How do you evaluate {primary_skill} against alternatives?\n2. What's the long-term strategy for {primary_skill} in an organization?\n3. How do you manage technical debt with {primary_skill}?"

def get_scenario_fallback(role: str, level: str) -> str:
    """Fallback scenario questions"""
    if level == "Entry/Junior":
        return "1. You're given a task you don't know how to do. What's your approach?\n2. You find a bug in code you didn't write. What do you do?\n3. You're stuck on a problem. How do you proceed?"
    elif level == "Mid-Level":
        return "1. A critical production issue occurs. Describe your troubleshooting process.\n2. You need to estimate a complex project. What's your approach?\n3. Requirements change mid-project. How do you handle it?"
    elif level == "Senior":
        return "1. Two teams have conflicting technical approaches. How do you resolve it?\n2. You need to migrate a critical system with zero downtime. Plan it.\n3. Technical debt is impacting velocity. What's your remediation plan?"
    else:
        return "1. Business wants to enter a new market. What's your technical strategy?\n2. You need to build a new engineering team. What's your plan?\n3. Multiple projects are competing for resources. How do you prioritize?"

def get_leadership_fallback(role: str, level: str) -> str:
    """Fallback leadership questions"""
    if level == "Entry/Junior":
        return "1. How do you contribute to team success?\n2. Describe your ideal team environment.\n3. How do you handle working with diverse team members?"
    elif level == "Mid-Level":
        return "1. How do you help junior team members grow?\n2. Describe your approach to code reviews and knowledge sharing.\n3. How do you build consensus on technical decisions?"
    elif level == "Senior":
        return "1. How do you develop technical talent in your team?\n2. Describe your approach to technical strategy and roadmap.\n3. How do you balance innovation with stability?"
    else:
        return "1. How do you build engineering culture and values?\n2. Describe your approach to executive communication.\n3. How do you measure and improve team performance?"

# Create interface (same as before)
with gr.Blocks(theme=gr.themes.Soft(), title="🤖 Advanced Interview Question Generator") as demo:
    gr.Markdown("# 🤖 Advanced Interview Question Generator")
    gr.Markdown("Generate tailored interview questions for specific tech roles")
    
    with gr.Row():
        with gr.Column(scale=1):
            role = gr.Dropdown(
                choices=list(JOB_CATEGORIES.keys()),
                value="Software Engineer",
                label="Select Job Role",
                interactive=True
            )
            
            level = gr.Radio(
                ["Entry/Junior", "Mid-Level", "Senior", "Lead/Principal"],
                value="Mid-Level",
                label="Experience Level"
            )
            
            use_api = gr.Checkbox(
                value=True,
                label="Use AI Generation (Hugging Face API)"
            )
        
        with gr.Column(scale=2):
            skills = gr.Textbox(
                label="Required Skills (comma-separated)",
                value="Python, SQL, AWS",
                lines=3,
                placeholder="Enter key skills separated by commas..."
            )
    
    with gr.Row():
        generate_btn = gr.Button("🎯 Generate Interview Questions", variant="primary", size="lg")
        clear_btn = gr.Button("🔄 Clear", variant="secondary")
    
    output = gr.Textbox(
        label="Generated Questions",
        lines=15,
        interactive=False
    )
    
    gr.Markdown("### 🔍 Additional Question Types")
    
    with gr.Row():
        behavioral_btn = gr.Button("🧠 Behavioral Questions")
        technical_btn = gr.Button("⚙️ Technical Deep Dive")
        scenario_btn = gr.Button("🎯 Scenario-Based")
        leadership_btn = gr.Button("👥 Leadership Questions")
    
    followup_output = gr.Textbox(
        label="Follow-up Questions",
        lines=8,
        interactive=False
    )
    
    # Main generation function
    def generate_wrapper(role, skills, level, use_api):
        return generate_questions(role, skills, level, use_api)
    
    # Event handlers
    generate_btn.click(
        generate_wrapper,
        inputs=[role, skills, level, use_api],
        outputs=output
    )
    
    clear_btn.click(
        lambda: ("", "", "Mid-Level", True, "", ""),
        outputs=[role, skills, level, use_api, output, followup_output]
    )
    
    # Follow-up question handlers
    def create_followup_handler(q_type):
        def handler(role, skills, level):
            return generate_followup_questions(role, skills, level, q_type)
        return handler
    
    behavioral_btn.click(
        create_followup_handler("behavioral"),
        inputs=[role, skills, level],
        outputs=followup_output
    )
    
    technical_btn.click(
        create_followup_handler("technical_depth"),
        inputs=[role, skills, level],
        outputs=followup_output
    )
    
    scenario_btn.click(
        create_followup_handler("scenario"),
        inputs=[role, skills, level],
        outputs=followup_output
    )
    
    leadership_btn.click(
        create_followup_handler("leadership"),
        inputs=[role, skills, level],
        outputs=followup_output
    )
    
    # Examples
    gr.Markdown("### 💡 Quick Examples")
    with gr.Row():
        gr.Examples(
            examples=[
                ["Machine Learning Engineer", "Python, TensorFlow, PyTorch, Scikit-learn", "Senior"],
                ["DevOps Engineer", "AWS, Docker, Kubernetes, Jenkins, Terraform", "Mid-Level"],
                ["Frontend Developer", "React, TypeScript, CSS, Redux", "Entry/Junior"],
                ["Cybersecurity Analyst", "SIEM, Splunk, IDS/IPS, Threat Hunting", "Mid-Level"]
            ],
            inputs=[role, skills, level]
        )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
