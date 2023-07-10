import streamlit as st
import requests
from PIL import Image
import PyPDF2
import re
import openai

openai.api_key = "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"

def load_resume_text(pdf_path):
    resume_text = ""

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            resume_text += page.extract_text()

    return resume_text

def extract_links_from_pdf(pdf_path):
    hyperlinks = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()

            # Find regular hyperlinks
            matches = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            hyperlinks.extend(matches)

            # Find Google Drive links
            google_drive_matches = re.findall(r'https?:\/\/drive.google.com\/[^\s/$.?#].[^\s]*', text)
            hyperlinks.extend(google_drive_matches)

    return hyperlinks

def extract_certificate_links(resume_text):
    certificate_links = []

    pattern = r"https:\/\/drive\.google\.com\/[^\s\/$?#].[^\s]*"
    matches = re.finditer(pattern, resume_text, re.IGNORECASE)
    for match in matches:
        certificate_links.append(match.group())

    return certificate_links

def summarize_text(resume_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=resume_text,
        max_tokens=250,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()
    return summary

def chatbot_interaction(summarized_text, question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Transcript: {summarized_text}\nQuestion: {question}",
        max_tokens=300,
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

def generate_response(message, resume_text):
    response = ""

    # Summarize the resume text and generate response
    summarized_text = summarize_text(resume_text)
    response = chatbot_interaction(resume_text, message)

    return response

def main():
    st.sidebar.title("Resume Chatbot")
    option = st.sidebar.radio("Select Option", ["Chatbot", "Resume"])

    if option == "Chatbot":
        st.title("Chatbot")
        st.write("Welcome! Start a conversation with the chatbot.")

        # Load the resume text from the PDF
        pdf_path = 'Rishika_Agrawal_resumeofficial.pdf'  # Update with the path to your resume PDF file
        resume_text = load_resume_text(pdf_path)

        # Extract links from the PDF
        extracted_links = extract_links_from_pdf(pdf_path)

        # Extract certificate links from the resume text
        certificate_links = extract_certificate_links(resume_text)

        # Autoprompt buttons
        row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
        education_button = row1_col1.button("Education")
        projects_button = row1_col2.button("Projects and Links")
        achievements_button = row1_col3.button("Achievements")
        experience_button = row1_col4.button("Experience")

        row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
        github_button = row2_col1.button("GitHub Profile")
        linkedin_button = row2_col2.button("LinkedIn Profile")
        email_button = row2_col3.button("Email")
        mobile_button = row2_col4.button("Mobile Number")

        # Chatbot conversation loop
        user_input = st.text_input("You:")
        chat_history = []

        if user_input:
            chat_history.append("You: " + user_input)
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)

            # Display the chat history
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)

            # Display the extracted links
            if any(keyword in user_input.lower() for keyword in ["links", "hyperlinks"]):
                st.subheader("Extracted Links")
                for link in extracted_links:
                    st.write(link)

            # Display the certificate links
            if "certificates" in user_input.lower():
                st.subheader("Certificate Links")
                if certificate_links:
                    for certificate_link in certificate_links:
                        st.write(certificate_link)

        # Handle autoprompt button clicks
        if education_button:
            user_input = "Education"
            chat_history.append("You: " + user_input+" give in points with each point in new line")
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif projects_button:
            user_input = "Projects and Links"
            chat_history.append("You: " + user_input+" List")
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif achievements_button:
            user_input = "Achievements"
            chat_history.append("You: " + user_input+" give in points with each point in new line")
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif experience_button:
            user_input = "Experience"
            chat_history.append("You: " + "EXPERIENCE")
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif github_button:
            user_input = "GitHub Profile"
            chat_history.append("You: " + user_input)
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif linkedin_button:
            user_input = "LinkedIn Profile"
            chat_history.append("You: " + user_input)
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif email_button:
            user_input = "Email"
            chat_history.append("You: " + user_input)
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)
        elif mobile_button:
            user_input = "Mobile Number"
            chat_history.append("You: " + user_input)
            response = generate_response(user_input, resume_text)
            chat_history.append("Chatbot: " + response)
            st.subheader("Chat History")
            for message in chat_history:
                st.write(message)

    elif option == "Resume":
        st.title("Resume")
        # Load and display the resume image
        image_path = 'resumeimage.jpg'  # Update with the path to your resume image file
        image = Image.open(image_path)
        st.image(image, caption='Resume', use_column_width=True)

if __name__ == "__main__":
    main()

