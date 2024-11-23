# **TravelMate - Chatbot integrating RAG (Retrieval Augmented Generation) and Function calling for Travel**

## **Project Description**
TravelMate is an intelligent chatbot that uses the **RAG (Retrieval Augmented Generation)** architecture combined with **Vector Database** to answer travel questions based on PDF data. The project uses **Langchain** to create and manage the Vector Database, providing the ability to search and process questions from users. In addition, TravelMate also supports API calls through **function calling**, although the feature related to image and video processing is currently not fully developed.

## **Key Features**
- **Retrieval Augmented Generation (RAG)**: Chatbot uses the RAG model to search for information in the Vector Database and combines it with the response generation ability of the LLM (Language Model) model to answer questions.
- **Vector Database**: Travel data is stored in Vector Database, which helps chatbots quickly search for information from imported PDF documents.

- **Function Calling to Call API**: The project uses Langchain and other APIs to support calling external APIs to get more information for user questions.

- **Support photos, videos and voice** (Not yet developed): Features related to photos and videos can be developed in the future so that chatbots can process and answer questions related to images or videos.

- **User interface using Streamlit**: The project runs on the Streamlit platform, allowing users to easily interact with the chatbot through the web interface.

## **Directory Structure**
```plaintext
LLM-RAG
└── src
├── app
├── data_src
├── domain
├── infra
└── vector_index
├── entry.py
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirement.txt
```
```markdown
## System Requirements

* **Python:** 3.7+
* **Streamlit:** 1.0+
* **Other Python Libraries:**
* `langchain`
* `openai`
* `Pillow (PIL)` (image processing support - no image/video features yet)
* `requests`
* `streamlit-chat-message-history`
* `python-dotenv`
* `numpy`
* `faiss-cpu` or `faiss-gpu` (depending on your computer configuration)
* **Other required tools:**
* `Docker` (if you want to deploy via Docker)
```
## Installation and Deployment

**1. Setting up a virtual environment:**

To manage libraries and environments more easily, you should create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Linux/Mac
venv\Scripts\activate # On Windows
```
**2. Installation requirements:**

Install the required libraries for the project via `requirements.txt`:

```bash
pip install -r requirements.txt
```
**3. Launch the application locally:**

To run the application locally via Streamlit, use the following command:

```bash
streamlit run streamlit_app/app.py
```
**4. Deploy with Docker:**

To deploy the application on Docker, you need to build a Docker image and run the container.

* **Step 1: Build the Docker image:**

```bash
docker build -t ravelmate .

```

* **Step 2: Run the Docker container:**

```bash
docker run -p 8501:8501 ravelmate
```

The application will be run on `http://localhost:8501`.

## Important Note

* This project uses Vector Database to store travel PDF documents, you need to prepare PDF files and upload them to the system so that the chatbot can search for information from them.

* Image, video, voice processing features are not currently implemented but may be added in the future.

* Just install Docker and use the mentioned commands to deploy and run the application without having to install any additional tools other than Docker.

## Future

* Support image/video processing features so that the chatbot can answer questions related to image or video content.

* Improve and expand the API function calling capabilities to integrate more external API services into the chatbot.

## Thanks

Thank you for using TravelMate! We look forward to receiving your feedback and contributions to improve this product!

```
