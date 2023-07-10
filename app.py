import re
import streamlit as st
import openai
import PyPDF2

# Set up OpenAI API
openai.api_key = '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'

def load_pdf_content():
    pdf_path = 'Rishika_Agrawal_resumeofficial.pdf'  # Update with the path to your PDF file
    pdf_content = ""

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_content += page.extract_text()

    return pdf_content


def extract_experience(resume_content):
    experience_section = ""
    # Find the experience section based on a specific pattern in the resume content
    pattern = r"EXPERIENCE(.*?)EDUCATION"
    match = re.search(pattern, resume_content, re.IGNORECASE | re.DOTALL)
    if match:
        experience_section = match.group(1).strip()
    return experience_section

def extract_achievements(resume_content):
    achievements_section = ""
    # Find the achievements section based on a specific pattern in the resume content
    pattern = r"ACHIEVEMENTS & CERTIFICATES(.*?)EXPERIENCE"
    match = re.search(pattern, resume_content, re.IGNORECASE | re.DOTALL)
    if match:
        achievements_section = match.group(1).strip()
    return achievements_section

def extract_links(resume_content):
    links = []
    # Find all the hyperlinks in the resume content using regular expression pattern matching
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, resume_content)
    for match in matches:
        link_text, link_url = match
        links.append((link_text, link_url))
    return links

def generate_response(message, resume_content):
    response = ""
    
    # Check if the message is related to the resume content
    if "experience" in message.lower():
        # Extract the experience section from the resume content
        experience_section = extract_experience(resume_content)
        response = "Here is Rishika's experience:\n" + experience_section
        
    elif "achievements" in message.lower():
        # Extract the achievements section from the resume content
        achievements_section = extract_achievements(resume_content)
        response = "Here are Rishika's achievements:\n" + achievements_section
        
    elif "linkedin" in message.lower():
        # Extract the LinkedIn profile link from the resume content
        links = extract_links(resume_content)
        linkedin_links = [(text, url) for (text, url) in links if "linkedin" in url]
        if linkedin_links:
            response = "Here is Rishika's LinkedIn profile:\n"
            for text, url in linkedin_links:
                response += f"- [{text}]({url})\n"
        else:
            response = "Rishika's LinkedIn profile link is not available."
    
    else:
        response = generate_chatbot_response(message)  # Replace with your chatbot's logic
        
    return response


def main():
    st.title("Conversational Form Chatbot")
    st.write("Welcome! Start a conversation with the chatbot.")

    # Load PDF content
    pdf_content = load_pdf_content()

    # Display the PDF content
    st.subheader("Resume PDF Content")
    st.write(pdf_content)

    # Chatbot conversation loop
    user_input = st.text_input("You:")
    chat_history = []

    if user_input:
        chat_history.append(user_input)
        response = generate_response(user_input, pdf_content)
        chat_history.append(response)

        # Display the chat history
        st.subheader("Chat History")
        for i in range(0, len(chat_history), 2):
            st.write("You: " + chat_history[i])
            st.write("Chatbot: " + chat_history[i + 1])

if __name__ == "__main__":
    main()
