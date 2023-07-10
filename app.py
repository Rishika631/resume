import streamlit as st
import openai
import PyPDF2

# Set up OpenAI API
openai.api_key = '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'

def load_pdf_content():
    pdf_path = '/path/to/resume.pdf'  # Update with the path to your PDF file
    pdf_content = ""

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            pdf_content += page.extract_text()

    return pdf_content


def generate_response(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"You: {message}\nAssistant:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

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
        response = generate_response(user_input)
        chat_history.append(response)

        # Display the chat history
        st.subheader("Chat History")
        for i in range(0, len(chat_history), 2):
            st.write("You: " + chat_history[i])
            st.write("Chatbot: " + chat_history[i + 1])

if __name__ == "__main__":
    main()
