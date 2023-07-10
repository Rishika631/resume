import streamlit as st
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
    st.title("Resume Chatbot")
    st.write("Welcome! Start a conversation with the chatbot.")

    # Load the resume text from the PDF
    pdf_path = 'path/to/your/resume.pdf'
    resume_text = load_resume_text(pdf_path)

    # Extract links from the PDF
    extracted_links = extract_links_from_pdf(pdf_path)

    # Extract certificate links from the resume text
    certificate_links = extract_certificate_links(resume_text)

    # Display image and chatbot in side-by-side columns
    col1, col2 = st.beta_columns(2)

    # Display the image
    image_path = 'path/to/your/image.jpg'
    image = Image.open(image_path)
    col1.image(image, use_column_width=True)

    # Chatbot conversation loop
    user_input = col2.text_input("You:")
    chat_history = []

    if user_input:
        chat_history.append(user_input)
        response = generate_response(user_input, resume_text)
        chat_history.append(response)

        # Display the chat history
        col2.subheader("Chat History")
        for i in range(0, len(chat_history), 2):
            col2.write("You: " + chat_history[i])
            col2.write("Chatbot: " + chat_history[i + 1])

        # Display the extracted links
        if any(keyword in user_input.lower() for keyword in ["links", "hyperlinks"]):
            col2.subheader("Extracted Links")
            for link in extracted_links:
                col2.write(link)

        # Display the certificate links
        if "certificates" in user_input.lower():
            col2.subheader("Certificate Links")
            if certificate_links:
                for certificate_link in certificate_links:
                    col2.write(certificate_link)
            else:
                col2.write("No certificate links found.")

if __name__ == "__main__":
    main()
