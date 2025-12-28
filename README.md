<div align="center">
<h1>Personal AI Assistant</h1>

> *An AI-powered OOP-driven Streamlit assistant powered by Google Gemini that acts as a tutor, coding assistant, and career helper, providing clear explanations, coding support, and practical guidance for learning, development, and career growth*
</div>

![Python Version](https://img.shields.io/badge/python-3.13.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![AI Powered](https://img.shields.io/badge/AI-Gemini-orange.svg)
![Language](https://img.shields.io/badge/language-bilingual-brightgreen.svg)
![Made with Love](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)

<!-- Custom JARVIS Badges -->
![Personal AI](https://img.shields.io/badge/Personal-AI%20Assistant-gold.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgMThjLTQuNDEgMC04LTMuNTktOC04czMuNTktOCA4LTggOCAzLjU5IDggOC0zLjU5IDgtOCA4eiIvPjwvc3ZnPg==)
![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4.svg?logo=google&logoColor=white)
![Multi](https://img.shields.io/badge/lang-Multi-blue.svg)
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellowgreen.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
![Code Style](https://img.shields.io/badge/code%20style-PEP8-blue.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Stars](https://img.shields.io/github/stars/aatansen/Personal-AI-Assistant?style=social)
![Forks](https://img.shields.io/github/forks/aatansen/Personal-AI-Assistant?style=social)
![Issues](https://img.shields.io/github/issues/aatansen/Personal-AI-Assistant)
![Last Commit](https://img.shields.io/github/last-commit/aatansen/Personal-AI-Assistant)

# **Context**
- [**Context**](#context)
  - [Features](#features)
    - [Core Functionality](#core-functionality)
  - [Requirements](#requirements)
    - [System Requirements](#system-requirements)
    - [Python Dependencies](#python-dependencies)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Install Dependencies](#2-install-dependencies)
    - [3. Configure Environment Variables](#3-configure-environment-variables)
  - [Usage](#usage)
    - [Starting Application](#starting-application)
    - [Role Selection](#role-selection)
  - [Project Structure](#project-structure)
  - [Logging](#logging)
  - [Troubleshooting](#troubleshooting)
    - [API Errors](#api-errors)
  - [Credits](#credits)
    - [Technologies Used](#technologies-used)
    - [Libraries \& Frameworks](#libraries--frameworks)
  - [Author](#author)
  - [License](#license)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)

## Features

- Lightweight Streamlit app implementing an Chatbot AI Assistant
- Designed with OOP principles (classes, encapsulation, inheritance, modularity).
- Gemini handles LLM responses; a JSON-backed memory file preserves conversation context.

### Core Functionality

- Greet user and behave like a personal assistant.
- Answer general questions using Gemini.
- Act in selectable roles:
  - Tutor
  - Coding assistant
  - Career helper
- Maintain conversation memory stored in a JSON file.
- Respect system-level instructions / assistant personality via `PromptController`.
- Robust error handling and graceful fallback when API or system errors occur.
- Chat history
  - Control Chat (delete/rename)
  - Export chat history as txt or json

[⬆️ Go to Context](#context)

## Requirements

### System Requirements

- **Python Version**: 3.13.11

[⬆️ Go to Context](#context)

### [Python Dependencies](./requirements.txt)

  ```sh
  google-genai== 1.56.0
  python-dotenv==1.2.1
  streamlit==1.52.2
  ```

[⬆️ Go to Context](#context)

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/aatansen/Personal-AI-Assistant.git
cd Personal-AI-Assistant
```

[⬆️ Go to Context](#context)

### 2. Install Dependencies

  ```sh
  pip install -r requirements.txt
  ```

[⬆️ Go to Context](#context)

### 3. Configure Environment Variables

- Create a `.env` file in the project root directory:

  ```env
  GEMINI_API_KEY="your_gemini_api_key_here"
  ```

**Note**: Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/api-keys)

[⬆️ Go to Context](#context)

## Usage

### Starting Application

- Run the main script

  ```sh
  streamlit run app.py
  ```

[⬆️ Go to Context](#context)

### Role Selection

- Select any of the three roles
  - Tutor
  - Coding assistant
  - Career helper
- Start chatting after selection

[⬆️ Go to Context](#context)

## Project Structure

  ```txt
  Personal-AI-Assistant
  ├── 📁 config
  │   ├── 🐍 __init__.py
  │   └── 🐍 settings.py
  ├── 📁 core
  │   ├── 🐍 __init__.py
  │   ├── 🐍 assistant.py
  │   ├── 🐍 gemini_engine.py
  │   ├── 🐍 memory.py
  │   └── 🐍 prompt_controller.py
  ├── ⚙️ .env.example
  ├── ⚙️ .gitattributes
  ├── ⚙️ .gitignore
  ├── 📄 LICENSE
  ├── 📝 README.md
  ├── 🐍 app.py
  ├── 📄 pixi.lock
  ├── ⚙️ pixi.toml
  └── 📄 requirements.txt
  ```

[⬆️ Go to Context](#context)

## Logging

- All interactions are logged in `logs/application.log` with timestamps for debugging and monitoring purposes. The log includes:
  - System actions performed
  - Errors and exceptions

[⬆️ Go to Context](#context)

## Troubleshooting

### API Errors

- Verify your Gemini API key is correct in the `.env` file
- Check your internet connection
- Ensure you haven't exceeded API rate limits

[⬆️ Go to Context](#context)

## Credits

### Technologies Used

- **Python** - Core programming language
- **Streamlit** - A faster way to build and share data apps
- **Google Gemini AI** - Intelligent response generation

[⬆️ Go to Context](#context)

### Libraries & Frameworks

- `python-dotenv` - Environment variable management
- `streamlit` - User interface
- `google-genai` - Gemini AI integration

[⬆️ Go to Context](#context)

## Author

[**Md. Alahi Almin Tansen**](https://github.com/aatansen/)

---

[⬆️ Go to Context](#context)

## License

This project is available for personal and educational use. Please provide appropriate credit when using or modifying this code.

[⬆️ Go to Context](#context)

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

[⬆️ Go to Context](#context)

## Acknowledgments

Inspired by OpenAI ChatGPT, Google Gemini. Special thanks to the open-source community for the amazing tools and libraries that made this project possible.

---
[⬆️ Go to Context](#context)
