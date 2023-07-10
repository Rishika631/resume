import streamlit as st
import PyPDF2
import re
from langchain.summarization import summarize_text
import openai

openai.api_key = "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"

def load_resume_text():
    pdf_path = 'Rishika_Agrawal_resumeofficial.pdf'  # Update with the path to your resume PDF file
    resume_text = ""

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            resume_text += page.extract_text()

    return resume_text

def extract_experience(resume_text):
    experience_section = ""
    experience_pattern = r"EXPERIENCE[\s\S]*?(?=ACHIEVEMENTS|EDUCATION|SKILLS\sSUMMARY|PROJECTS|\Z)"
    matches = re.findall(experience_pattern, resume_text, re.IGNORECASE)
    if matches:
        experience_section = matches[0].strip()
    return experience_section

def extract_achievements(resume_text):
    achievements_section = ""
    achievements_pattern = r"ACHIEVEMENTS[\s\S]*?(?=EXPERIENCE|EDUCATION|SKILLS\sSUMMARY|PROJECTS|CERTIFICATES|\Z)"
    matches = re.findall(achievements_pattern, resume_text, re.IGNORECASE)
    if matches:
        achievements_section = matches[0].strip()
    return achievements_section

def extract_education(resume_text):
    education_section = ""
    education_pattern = r"EDUCATION[\s\S]*?(?=EXPERIENCE|ACHIEVEMENTS|SKILLS\sSUMMARY|PROJECTS|\Z)"
    matches = re.findall(education_pattern, resume_text, re.IGNORECASE)
    if matches:
        education_section = matches[0].strip()
    return education_section

def extract_skills_summary(resume_text):
    skills_summary_section = ""
    skills_summary_pattern = r"SKILLS\sSUMMARY[\s\S]*?(?=EXPERIENCE|ACHIEVEMENTS|EDUCATION|PROJECTS|\Z)"
    matches = re.findall(skills_summary_pattern, resume_text, re.IGNORECASE)
    if matches:
        skills_summary_section = matches[0].strip()
    return skills_summary_section

def extract_projects(resume_text):
    projects_section = ""
    projects_pattern = r"PROJECTS[\s\S]*?(?=EXPERIENCE|ACHIEVEMENTS|EDUCATION|SKILLS\sSUMMARY|\Z)"
    matches = re.findall(projects_pattern, resume_text, re.IGNORECASE)
    if matches:
        projects_section = matches[0].strip()
    return projects_section

def extract_certificates(resume_text):
    certificates_section = ""
    certificates_pattern = r"CERTIFICATES[\s\S]*?(?=EXPERIENCE|ACHIEVEMENTS|EDUCATION|SKILLS\sSUMMARY|PROJECTS|\Z)"
    matches = re.findall(certificates_pattern, resume_text, re.IGNORECASE)
    if matches:
        certificates_section = matches[0].strip()
    return certificates_section

def generate_response(message, resume_text):
    response = ""

    if "experience" in message.lower():
        # Extract and generate response about experience
        experience_section = extract_experience(resume_text)
        response = f"Experience:\n{experience_section}"

    elif "achievements" in message.lower():
        # Extract and generate response about achievements and certificates
        achievements_section = extract_achievements(resume_text)
        certificates_section = extract_certificates(resume_text)
        response = f"Achievements:\n{achievements_section}\n\nCertificates:\n{certificates_section}"

    elif "education" in message.lower():
        # Extract and generate response about education
        education_section = extract_education(resume_text)
        response = f"Education:\n{education_section}"

    elif "skills" in message.lower() or "summary" in message.lower():
        # Extract and generate response about skills summary
        skills_summary_section = extract_skills_summary(resume_text)
        response = f"Skills Summary:\n{skills_summary_section}"

    elif "projects" in message.lower():
        # Extract and generate response about projects
        projects_section = extract_projects(resume_text)
        response = f"Projects:\n{projects_section}"

    else:
        # Summarize the resume text and generate response
        summarized_text = summarize_text(resume_text)
        response = chatbot_interaction(summarized_text, message)

    return response

def chatbot_interaction(transcript, question):
    # Use LangChain API or any other OpenAI model API for chatbot
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Transcript: {transcript}\nQuestion: {question}",
        max_tokens=75,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    answer = response.choices[0].text.strip()

    if answer:
        return answer
    else:
        return "I'm sorry, I don't have an answer for that question."

def main():
    st.title("Resume Chatbot")
    st.write("Welcome! Start a conversation with the chatbot.")

    # Load the resume text from the PDF
    resume_text = load_resume_text()

    # Chatbot conversation loop
    user_input = st.text_input("You:")
    chat_history = []

    if user_input:
        chat_history.append(user_input)
        response = generate_response(user_input, resume_text)
        chat_history.append(response)

        # Display the chat history
        st.subheader("Chat History")
        for i in range(0, len(chat_history), 2):
            st.write("You: " + chat_history[i])
            st.write("Chatbot: " + chat_history[i + 1])

if __name__ == "__main__":
    main()
