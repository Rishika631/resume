import streamlit as st
import pdfplumber
import re
import openai

openai.api_key = "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"

def load_resume_text(pdf_path):
    resume_text = ""

    with open(pdf_path, 'rb') as file:
        reader = pdfplumber.load(file)
        for page in reader.pages:
            text = page.extract_text()
            resume_text += text

    return resume_text

def extract_links_from_pdf(pdf_path):
    hyperlinks = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            matches = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            hyperlinks.extend(matches)

    return hyperlinks

def summarize_text(resume_text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=resume_text,
        max_tokens=150,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()
    return summary

def chatbot_interaction(summarized_text, question):
    # Use LangChain API or any other OpenAI model API for chatbot
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Transcript: {summarized_text}\nQuestion: {question}",
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
    pdf_path = 'Rishika_Agrawal_resumeofficial.pdf'  # Update with the path to your resume PDF file
    resume_text = load_resume_text(pdf_path)

    # Extract links from the PDF
    extracted_links = extract_links_from_pdf(pdf_path)

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

        # Display the extracted links
        if any(keyword in user_input.lower() for keyword in ["links", "hyperlinks"]):
            st.subheader("Extracted Links")
            for link in extracted_links:
                st.write(link)

if __name__ == "__main__":
    main()
