# 👗 Fashion Outfit Advisor 🌟

Welcome to the **Fashion Outfit Advisor**! This application provides personalized fashion advice based on user inputs, and live weather. Whether you're looking for outfit recommendations or want to explore similar products, we've got you covered! 👗👖

## 🚀 Features

- **Chat Interface**: Interact with our fashion advisor through a user-friendly chat interface. 💬
- **Image Upload**: Upload images of clothing items to get detailed analysis and recommendations (feature built, integration in progress). 📸
- **Weather Integration**: Get outfit suggestions based on the current weather in your location. ☀️🌧️
- **Similar Products Search**: Find similar products available for purchase based on uploaded images (feature built, integration in progress). 🛍️

## 🛠️ Tech Stack

### Backend
🚀 **FastAPI**

🧠 **Langchain**

🌤️ **OpenWeatherMap**

🔍 **SerpAPI - Google Lens** (in production)

🤖 **LLM Vendor: OpenAI** (moving to Anthropic)

⚡ **Uvicorn**

### Frontend 
💻 **Streamlit**

### Database
🗄️ **SQLite**

### Containerization
🐳 **Docker**

## 📦 Installation

To get started with the Fashion Outfit Advisor, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/fatima-cyber/fashion-outfit-advisor.git
   cd fashion-outfit-advisor
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
   SERPAPI_API_KEY=your_serpapi_key #currently not used
   ```

3. Run the application using Docker:
   ```bash
   make all
   ```

## 🎨 Usage

- Open your browser and navigate to `http://localhost:8501` for the frontend.

## 🤝 Contributing

We welcome contributions! If you'd like to contribute, please fork the repository and submit a pull request. Let's make fashion advice accessible to everyone! 💖

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Happy styling! 🎉👗✨

