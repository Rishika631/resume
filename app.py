import streamlit as st
import PyPDF2
import re
import requests

def load_resume_text():
    pdf_url = 'https://github.com/Rishika631/resume/blob/main/Rishika_Agrawal_resumeofficial.pdf'  # Update with the URL to your resume PDF file
    resume_text = ""

    response = requests.get(pdf_url)
    with open('temp_resume.pdf', 'wb') as file:
        file.write(response.content)

    with open('temp_resume.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            resume_text += page.extract_text()

    return resume_text

def extract_links(resume_text):
    # Find all URLs or hyperlinks in the resume text
    pattern = r"(?P<url>https?://[^\s]+)"
    matches = re.findall(pattern, resume_text)
    links = list(set(matches))  # Remove duplicates if any
    return links


def generate_response(message):
    # Extract the links from the resume text
    links = extract_links(resume_text)

    # Process user input and generate response
    response = ""

    if "experience" in message.lower():
        # Generate response about experience
        response = "Here is my experience: ..."

    elif "projects" in message.lower():
        # Generate response about projects
        response = "Here are my projects: ..."

    elif "skills" in message.lower():
        # Generate response about skills
        response = "Here are my skills: ..."

    elif "education" in message.lower():
        # Generate response about education
        response = "Here is my education: ..."

    elif any(keyword in message.lower() for keyword in ["github", "code", "repository"]):
        # Check if user is asking for GitHub repository
        github_links = [link for link in links if "github" in link]
        if github_links:
            response = f"Here is my GitHub repository: {github_links[0]}"
        else:
            response = "I don't have a GitHub repository available."

    elif "linkedin" in message.lower():
        # Check if user is asking for LinkedIn profile
        linkedin_links = [link for link in links if "linkedin" in link]
        if linkedin_links:
            response = f"Here is my LinkedIn profile: {linkedin_links[0]}"
        else:
            response = "I don't have a LinkedIn profile available."

    else:
        response = "I'm sorry, I couldn't understand your question."

    return response

def main():
    st.title("Resume Chatbot")
    st.write("Welcome! Start a conversation with the chatbot.")

    # Load the resume text from the PDF
    resume_text = load_resume_text()

    # Display the resume text
    st.subheader("Resume Details")
    st.write(resume_text)

    # Chatbot conversation loop
    user_input = st.text_input("You:")
    chat_history = []

    if user_input:
        chat_history.append(user_input)
        response = generate_response(user_input)
        chat_history.append(response)

        # Display the chat history
        st.subheader("Chat History")
        for i in range(0, len(chat_history), 2):
            st.write("You: " + chat_history[i])
            st.write("Chatbot: " + chat_history[i + 1])

if __name__ == "__main__":
    main()
