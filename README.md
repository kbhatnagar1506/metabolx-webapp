# Blood Report Analyzer

A web application that uses AI to analyze blood reports and provide medical insights, diagnoses, and medicine recommendations.

## Features

- Text-based blood report analysis
- Image-based blood report analysis
- Medicine recommendations with efficacy percentages
- Modern and responsive UI
- Drag-and-drop image upload

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd blood_report_analyzer
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. You can either:
   - Paste your blood report text in the text area
   - Upload an image of your blood report
   - Or both

4. Click "Analyze Report" to get the AI-powered analysis

## Security Note

This application is for demonstration purposes only. In a production environment, you should:
- Implement proper user authentication
- Use HTTPS
- Validate and sanitize all inputs
- Implement rate limiting
- Store sensitive data securely
- Add proper error handling and logging

## License

MIT License 