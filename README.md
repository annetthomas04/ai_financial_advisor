# Ruya - AI Financial Advisor

Ruya is an AI-powered financial advisor web application that provides personalized financial insights, budgeting suggestions, and money management tips.

## Features

- 💬 Interactive chat interface
- 💰 Financial advice on budgeting, saving, investments, and lifestyle
- 🤖 Powered by advanced AI models through OpenRouter API
- 🌐 Web-based interface accessible from any device

## Setup Instructions

### Prerequisites

- Python 3.6+
- OpenRouter API key

### Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenRouter API key:

```
DEEPSEEK_API_KEY=your_openrouter_api_key_here
```

### Running the Application

1. Start the Flask server:

```bash
python app.py
```

2. Open `index.html` in your web browser or serve it using a local web server

## Usage

1. Type your financial question in the input box
2. Click the send button or press Enter
3. Receive AI-generated financial advice tailored to your query

## Troubleshooting

### API Rate Limits

The application uses multiple AI models with automatic fallback and retry mechanisms to handle rate limits. If you encounter persistent API issues:

- Wait a few minutes before trying again
- Check your OpenRouter API key and usage limits
- Consider upgrading to a paid tier for higher rate limits

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- AI: OpenRouter API (DeepSeek, Mistral, Palm models)

## License

This project is for educational purposes only.