# FastAPI LangGraph Chat

This project is a simple chat application built using FastAPI and LangGraph agents. It provides a web interface for users to interact with a chat system powered by AI.

## Project Structure

```
fastapi-langgraph-chat
├── src
│   ├── main.py                # Entry point of the FastAPI application
│   ├── api
│   │   └── chat.py            # API endpoint for chat functionality
│   ├── agents
│   │   └── langgraph_agent.py  # Implementation of the LangGraph agent
│   ├── templates
│   │   └── chat.html          # HTML template for the chat window
│   ├── static
│   │   ├── css
│   │   │   └── styles.css     # CSS styles for the chat window
│   │   └── js
│   │       └── chat.js        # JavaScript for chat interactions
│   └── tests
│       └── test_chat.py       # Unit tests for the chat API
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables for configuration
├── Dockerfile                  # Instructions for building the Docker image
├── docker-compose.yml          # Multi-container Docker application configuration
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-langgraph-chat
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn src.main:app --reload
   ```

5. **Access the chat interface:**
   Open your browser and go to `http://localhost:8000`.

## Usage

- Users can send messages through the chat interface.
- The backend processes the messages using LangGraph agents and returns responses.

## Testing

To run the tests, execute the following command:
```
pytest src/tests/test_chat.py
```

## Docker

To build and run the application using Docker, use the following commands:
```
docker-compose up --build
```

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.