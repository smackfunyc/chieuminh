# LLM Chatbot Overview
+-------------+
|    User     |
+-------------+
      |
      v
+----------------+
| Chat Interface  |
| (e.g., Gradio)  |
+----------------+
      |
      v
+-------------------------+
|     LLM (ChatGPT)      |
| +---------------------+ |
| |  Tokenization      | |
| +---------------------+ |
| |  Prediction Engine  | |
| +---------------------+ |
| |  Output Generation  | |
| +---------------------+ |
+-------------------------+
      |
      v
+--------------+
|   Response   |
+--------------+
      |
      v
+----------------+
| Chat Interface  |
+----------------+

This project leverages the **LangGraph** library to create an interactive chat application that generates responses based on predefined constants and user input. It integrates several Python libraries to enhance functionality:

- **Gradio**: For building the user interface.
- **langchain_openai**: Utilized for leveraging OpenAI's language models.
- **Pydantic**: Used for data validation.

## Requirements

To run this project, you will need the following:

- **LangSmith API**: For powerful interaction and tracking of your language tasks.
- **Serper API**: For online search capabilities.
- **Python 3.7 or later**: Ensure you have Python installed on your machine.

### Required Python Libraries

You need to install the following libraries:

- `gradio`
- `langchain-openai`
- `langgraph`
- `pydantic`
- `requests`
- `python-dotenv`


### Installation Instructions

1. **Download the requirements file**:

2. **Install Dependencies**:
   Navigate to your project directory and run the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```

## Application Structure

The application is designed with a **stateful graph structure** in which nodes represent Python functions that handle user interactions and generate either random or AI-generated responses. 

### Core Functionality

- **State Representation**: Defines the structure of the application's state.
- **Response Graph**: Builds a graph of responses based on user interactions.
- **Chat Interface**: Launches an interactive chat interface that allows users to engage seamlessly with the application.

## Key Features

- **Interactive Chat**: Users can input queries and receive generated responses in real-time.
- **Integration of Language Models**: Demonstrates the power of combining Python functions with advanced language models for dynamic interaction.

This project illustrates the potential of creating smart, interactive applications by utilizing modern Python libraries to enhance user experience and functionality.
