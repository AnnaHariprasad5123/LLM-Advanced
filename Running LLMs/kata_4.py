import requests
from bs4 import BeautifulSoup
import json
import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
hugging_face_key = os.getenv("HUGGING_FACE_KEY")


def get_article_text(url):
    """Fetch article text from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = soup.get_text()
        return article_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL {url}: {e}")
        return None

headers = {"Authorization": f"Bearer ${hugging_face_key}"}

def query(payload, API_URL):
    """Send a query to the API and return the response."""
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error querying the API: {e}")
        return None

def get_summary(article):
    """Generate a summary, date, and category for the article."""
    try:
        article_text1 = article[800:]
        summary_output = query({"inputs": article_text1}, "https://api-inference.huggingface.co/models/google/pegasus-large")
        date_output = query({
            "inputs": {
                "question": "What is the date the article was written",
                "context": article_text1
            }
        }, "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2")
        category_output = query({
            "inputs": {
                "question": "What are the most likely category of articles that this content could belong to? Here are some examples of article categories: news, sports, business, entertainment, science, technology, lifestyle, health, opinion, travel, arts, and food.",
                "context": article
            }
        }, "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2")
        return {"summary": summary_output[0]['summary_text'], "date": date_output['answer'], 'article_type': category_output['answer']}
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

def main():
    st.title("Article Summarizer and Chat Query Tool")

    # Initialize session states
    if "urls" not in st.session_state:
        st.session_state.urls = []
    if "url_count" not in st.session_state:
        st.session_state.url_count = 0 
    if "json_created" not in st.session_state:
        st.session_state.json_created = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display dynamic input fields for URLs
    if st.button("Add More URL"):
        st.session_state.url_count += 1

    # Display URL inputs and process them when entered
    for i in range(st.session_state.url_count):
        current_url = st.text_input(f"Enter URL {i + 1}:", key=f"current_url_{i}", value=st.session_state.get(f'current_url_{i}', ''))
        
        if st.button(f"Enter URL {i + 1}"):
            if current_url:
                st.session_state.urls.append(current_url)
                st.success(f"URL {i + 1} added!")
            else:
                st.warning(f"Please enter a URL {i + 1}.")

    # Show all added URLs
    if st.session_state.urls:
        st.write("Added URLs:")
        for idx, url in enumerate(st.session_state.urls, start=1):
            st.write(f"{idx}. {url}")

    # Process URLs when "Process URLs" button is clicked
    if st.button("Process URLs") and st.session_state.urls:
        with st.spinner("Summarizing articles and creating JSON file..."):
            try:
                existing_data = []
                for url in st.session_state.urls:
                    article_text = get_article_text(url)
                    if article_text:
                        summary_data = get_summary(article_text)
                        if summary_data:
                            summary_data["url"] = url
                            existing_data.append(summary_data)

                with open("summary_data1.json", "w") as file:
                    json.dump(existing_data, file, indent=4)

                st.session_state.json_created = True
                st.success("JSON file created successfully!")
            except Exception as e:
                st.error(f"Error during summarization: {e}")

    # Show JSON file if created
    if st.session_state.json_created:
        with st.expander("View Summary JSON File"):
            try:
                with open("summary_data1.json", "r") as file:
                    json_data = json.load(file)
                    st.json(json_data)
            except FileNotFoundError:
                st.error("JSON file not found.")

        st.subheader("Query on Summarized Data")
        question = st.text_input("Ask a question about the summarized data:")
        if st.button("Submit Query") and question:
            try:
                with open("summary_data1.json", "r") as file:
                    read_data = json.load(file)
                read_data_str = json.dumps(read_data)
                client = Groq(
                    api_key=groq_api_key
                )
                def query_on_json(question):
                    chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content":f"{read_data_str}\n\n{question}"
                        }
                    ],
                    model="llama-3.1-8b-instant",
                    )

                    return chat_completion.choices[0].message.content

                with st.spinner("Fetching answer..."):
                    answer = query_on_json(question)
                    st.session_state.chat_history.append((question, answer))

            except FileNotFoundError:
                st.error("JSON file not found. Please process URLs first.")

        # Display chat history
        if st.session_state.chat_history:
            st.write("Chat History:")
            for idx, (q, a) in enumerate(st.session_state.chat_history, start=1):
                st.markdown(f"**Q{idx}:** {q}")
                st.markdown(f"**A{idx}:** {a}")

if __name__ == "__main__":
    main()
