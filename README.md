# AI-Challenge

This project creates an AI-powered agent that extracts text from uploaded PDF documents, allows users to query the content using natural language, and posts the answers to a specified Slack channel. The app is built with Streamlit for the frontend, OpenAI's GPT model for natural language understanding, and the Slack API for communication.


**Table of Contents**
    
    workflows
    Features
    Directory Structure
    Dataset description
    Installation
    License

**Workflows**

Update the configuration manager in src config
Update the components
Update the embedding in utils
Update the constants
Update the main.py
update the app.py

**Features**

PDF Extraction: Extracts and preprocesses text from large PDF documents.
Question-Answering: Allows users to ask questions based on the content of uploaded PDFs.
Slack Integration: Posts answers to a Slack channel.


**Directory Structure**

AI-CHALLENGE(Project directory)
    app.py
    src/
        AiChallenge/
            components/
                -llm_handler.py
                -document_handler.py
                -faiss_index.py
                -slackclient.py
            
            config/
                -configuration.py

            constants/
                -cvariables.py

            pipeline/
                -api_routes.py
            
            utils/
                -embedding.py

    README.md
    requirements.txt
    setup.py
    main.py

**Dataset Description** 
It is a pdf document which has different contents about a company named Zania.ai


**Installation**
Clone the repository
https://github.com/Ajayajgit/AI-Challenge

**Create a virtual environment after opening the repository**
python3 -m venv .\.venv
*activate the venv*
source .venv\Scripts\activate

**install the requirements**
pip install -r requirements.txt

**License**

This project is licensed under the MIT License.


