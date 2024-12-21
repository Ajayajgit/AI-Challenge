import io 
import re
import requests
import streamlit as st
from PyPDF2 import PdfReader
from src.AiProduct.config.configuration import Config
from src.AiProduct.components.slackclient import SlackHandler

class PdfHandler: # this is for handling the pdf, reads it, extract the text and clean any contents 
    @staticmethod
    def extract_text_from_pdf(pdf_file):
        reader = PdfReader(pdf_file)
        text = []
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text.append(PdfHandler.clean_toc(page_text, page_num))
        return "\n".join(text)

    @staticmethod
    def clean_toc(text, page_num):
        toc_start_pattern = r'\bTable of Contents\b'
        toc_pattern = r'^\d+(\.\d+)+\s+[A-Za-z\s]+\s*\.+\s*\d{1,3}$'
        link_pattern = r'https?://\S+'

        lines = text.splitlines()
        clean_lines = []
        inside_toc = False

        for line in lines:
            if re.search(toc_start_pattern, line, re.IGNORECASE):
                inside_toc = True
            if inside_toc:
                if not line.strip():
                    inside_toc = False
                continue
            if re.match(toc_pattern, line.strip()):
                continue
            line = re.sub(link_pattern, '', line)
            clean_lines.append(line)
        
        cleaned_text = "\n".join(clean_lines)
        return cleaned_text

class ApiHandler:
    @staticmethod
    def add_document(doc_text):
        config = Config()
        response = requests.post(f"{Config.get_api_url()}/add-document", json={"text": doc_text})
        return response

    @staticmethod
    def get_answer(query_text):
        config = Config()
        response = requests.post(f"{Config.get_api_url()}/get-answer", json={"query": query_text})
        return response

class SlackNotifier:
    @staticmethod
    def send_notification(message):
        try:
            SlackHandler.post_message(message)
        except Exception as e:
            raise Exception(f"Failed to send message to Slack: {e}")

class PdfApp:
    def __init__(self):
        self.pdf_handler = PdfHandler()
        self.api_handler = ApiHandler()
        self.slack_notifier = SlackNotifier()

    def display_ui(self):
        st.title("PDF Question Answering System")
        st.write("This interface allows you to upload a PDF and ask questions based on its content.")
        st.sidebar.title("Options")
        option = st.sidebar.selectbox("Choose an action", ["Add Document", "Get Answer"])
        send_to_slack = st.sidebar.checkbox("Send response to Slack")

        if option == "Add Document":
            self.add_document_ui(send_to_slack)
        elif option == "Get Answer":
            self.get_answer_ui(send_to_slack)

    def add_document_ui(self, send_to_slack):
        st.header("Upload PDF Document")
        uploaded_file = st.file_uploader("Upload a .pdf file", type=["pdf"])

        doc_text = ""
        if uploaded_file:
            pdf_data = io.BytesIO(uploaded_file.read())
            doc_text = self.pdf_handler.extract_text_from_pdf(pdf_data)
        
        if st.button("Submit Document"):
            if doc_text.strip():
                response = self.api_handler.add_document(doc_text)
                if response.status_code == 200:
                    st.success("Document added successfully!")
                    if send_to_slack:
                        try:
                            self.slack_notifier.send_notification("Document added successfully to the system.")
                            st.info("Notification sent to Slack.")
                        except Exception as e:
                            st.error(f"Failed to send message to Slack: {e}")
                else:
                    st.error("Error adding document. Please check the server.")
            else:
                st.warning("Please upload a valid PDF.")

    def get_answer_ui(self, send_to_slack):
        st.header("Ask a Question")
        query_text = st.text_input("Enter your question:")
        
        if st.button("Get Answer"):
            if query_text:
                response = self.api_handler.get_answer(query_text)
                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer found.")
                    st.write("**Answer:**")
                    st.write(answer)
                    if send_to_slack:
                        try:
                            self.slack_notifier.send_notification(f"Q: {query_text}\nA: {answer}")
                            st.info("Answer sent to Slack.")
                        except Exception as e:
                            st.error(f"Failed to send answer to Slack: {e}")
                else:
                    st.error("Error retrieving answer. Please check the server.")
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    app = PdfApp()
    app.display_ui()
