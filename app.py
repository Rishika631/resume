import re
import os
import pandas as pd
import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from transformers import pipeline
import plotly.express as px
import openai

# Set OpenAI API credentials
openai.api_key = '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'

# Set Streamlit page configuration
st.set_page_config(page_title="YouTube Video Summarizer and Insights")

# Function to extract transcript from YouTube video
def extract_transcript(youtube_video):
    video_id = parse_qs(urlparse(youtube_video).query)['v'][0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([segment['text'] for segment in transcript])
    return transcript_text

# Function to summarize transcript using OpenAI's text-davinci-003 model
def summarize_transcript(transcript):
    prompt = "Extract summary from the following transcript in 100 words:\n\n" + transcript
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    summary = response.choices[0].text.strip()

    persons = re.findall(r"\b[A-Z][a-zA-Z]+\b", transcript)  # Extract persons mentioned in the transcript
    persons = list(set(persons))  # Remove duplicates

    return summary, persons

# Function to calculate contribution based on assigned tasks
def calculate_contribution(tasks_with_persons):
    tasks_df = pd.DataFrame(tasks_with_persons)
    contribution_df = tasks_df["person"].value_counts().reset_index()
    contribution_df.columns = ["Person", "Tasks Assigned"]
    total_tasks = contribution_df["Tasks Assigned"].sum()
    contribution_df["Contribution"] = contribution_df["Tasks Assigned"] / total_tasks * 100
    return contribution_df

# Function to extract transcript from video
def extract_transcript_from_video(video_path):
    transcript = ""
    
    # Convert video to audio
    audio_path = "temp_audio.wav"
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Use Google Speech Recognition to extract transcript
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    try:
        transcript = r.recognize_google(audio)
    except sr.UnknownValueError:
        st.error("Speech recognition could not understand audio")
    except sr.RequestError as e:
        st.error("Could not request results from Google Speech Recognition service: {0}".format(e))

    # Remove temporary audio file
    os.remove(audio_path)

    return transcript

# Function to extract image summary from the video using moviepy
def extract_image_summary(video_path):
    clip = mp.VideoFileClip(video_path)
    duration = clip.duration
    key_frames = []
    image_summary = []

    # Extract key frames at desired intervals
    for i in range(10):
        time = duration * i / 10
        frame = clip.get_frame(time)
        key_frames.append(frame)
        image_summary.append(f"Key Point {i+1}")

    return key_frames, image_summary

# Function to extract action insights & key points from transcript 
def extract_action_insights(transcript):
    prompt = "Extract action insights and key points both from the following transcript:\n\n" + transcript
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    insights = response.choices[0].text.strip().split("\n")
    return insights

# Function to analyze sentiment of the transcript
def analyze_sentiment(transcript):
    sentiment_analyzer = pipeline("sentiment-analysis")
    results = sentiment_analyzer(transcript)

    sentiments = [result["label"] for result in results]
    return sentiments

# Function to extract given task from transcript
def extract_task_from_transcript(transcript, task):
    prompt = f"{task} from the following transcript and mention to whom the task is given:\n\n{transcript}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.3,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    tasks = response.choices[0].text.strip().split("\n")
    tasks_with_persons = []

    for task in tasks:
        task_info = task.split(" - ")
        if len(task_info) == 2:
            tasks_with_persons.append({"task": task_info[0], "person": task_info[1]})

    return tasks_with_persons

# Function to perform chatbot interaction
def chatbot_interaction(transcript, question):
    # Use OpenAI model API for chatbot interaction
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

# Streamlit app
def main():
    st.header("YouTube Video Summarizer and Insights")

    # Option to upload local file or enter YouTube video URL
    option = st.selectbox("Choose an option:", ["YouTube Video", "Local File"])

    if option == "YouTube Video":
        # Get YouTube video URL from user
        youtube_video = st.text_input("Enter the YouTube video URL:")

        if youtube_video:
            # Extract transcript from YouTube video
            transcript = extract_transcript(youtube_video)

            # Summarize transcript
            summary, persons = summarize_transcript(transcript)

            st.info("Meeting processed successfully!")

            # Display options
            options = st.sidebar.multiselect("Select Options:", ["Meeting Summary", "Image Summary", "Action Insights & Key Points", "Sentiment Analysis", "Given Task", "Contribution Chart", "Chatbot"])

            # Meeting Summary
            if "Meeting Summary" in options:
                st.subheader("Meeting Summary")
                st.text(summary)

            # Image Summary
            if "Image Summary" in options:
                st.subheader("Image Summary")
                key_frames, image_summary = extract_image_summary(youtube_video)
                for idx, key_frame in enumerate(key_frames):
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(image_summary[idx])

            # Action Insights & Key Points
            if "Action Insights & Key Points" in options:
                st.subheader("Action Insights & Key Points")
                insights = extract_action_insights(transcript)
                for insight in insights:
                    st.write(insight)

            # Sentiment Analysis
            if "Sentiment Analysis" in options:
                st.subheader("Sentiment Analysis")
                sentiment_results = analyze_sentiment(transcript)
                for idx, sentiment in enumerate(sentiment_results):
                    st.write(f"Sentiment {idx+1}: {sentiment}")

            # Given Task
            if "Given Task" in options:
                st.subheader("Given Task")
                tasks_with_persons = extract_task_from_transcript(transcript, "Extract task")
                tasks_df = pd.DataFrame(tasks_with_persons)
                st.dataframe(tasks_df)

            # Contribution Chart
            if "Contribution Chart" in options:
                st.subheader("Contribution Chart")
                contribution_df = calculate_contribution(tasks_with_persons)
                fig = px.pie(contribution_df, values='Contribution', names='Person')
                st.plotly_chart(fig)

            # Chatbot
            if "Chatbot" in options:
                st.subheader("Chatbot")
                user_question = st.text_input("Ask a question:")
                if user_question:
                    response = chatbot_interaction(transcript, user_question)
                    st.write(response)

    elif option == "Local File":
        # File upload feature
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4"])

        if uploaded_file:
            # Save the uploaded file
            video_path = "uploaded_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract transcript from video
            transcript = extract_transcript_from_video(video_path)

            # Summarize transcript
            summary, persons = summarize_transcript(transcript)

            st.info("Transcript processed successfully!")

            # Display options
            options = st.sidebar.multiselect("Select Options:", ["Meeting Summary", "Image Summary", "Action Insights & Key Points", "Sentiment Analysis", "Given Task", "Chatbot"])

            # Meeting Summary
            if "Meeting Summary" in options:
                st.subheader("Meeting Summary")
                st.text(summary)

            # Image Summary
            if "Image Summary" in options:
                st.subheader("Image Summary")
                key_frames, image_summary = extract_image_summary(video_path)
                for idx, key_frame in enumerate(key_frames):
                    st.image(key_frame, caption=f"Key Frame {idx+1}")
                    st.write(image_summary[idx])

            # Action Insights & Key Points
            if "Action Insights & Key Points" in options:
                st.subheader("Action Insights & Key Points")
                insights = extract_action_insights(transcript)
                for insight in insights:
                    st.write(insight)

            # Sentiment Analysis
            if "Sentiment Analysis" in options:
                st.subheader("Sentiment Analysis")
                sentiment_results = analyze_sentiment(transcript)
                for idx, sentiment in enumerate(sentiment_results):
                    st.write(f"Sentiment {idx+1}: {sentiment}")

            # Given Task
            if "Given Task" in options:
                st.subheader("Given Task")
                tasks_with_persons = extract_task_from_transcript(transcript, "Extract task")
                tasks_df = pd.DataFrame(tasks_with_persons)
                st.dataframe(tasks_df)

            # Chatbot
            if "Chatbot" in options:
                st.subheader("Chatbot")
                user_question = st.text_input("Ask a question:")
                if user_question:
                    response = chatbot_interaction(transcript, user_question)
                    st.write(response)

            # Delete the uploaded video file
            os.remove(video_path)

if __name__ == "__main__":
    main()
