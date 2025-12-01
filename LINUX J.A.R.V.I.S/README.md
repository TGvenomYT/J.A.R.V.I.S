# JARVIS Assistant

JARVIS is a personal assistant application designed to help users with various tasks through voice commands. It integrates with multiple services and provides a user-friendly interface for managing tasks and accessing information.

## Features

- **Voice Recognition**: Accepts commands through voice input.
- **Date and Time**: Provides the current date and time.
- **Application Launcher**: Launches applications like Chrome.
- **Website Opener**: Opens websites based on user input.
- **Weather Information**: Fetches weather details for a specified city.
- **Wikipedia Search**: Provides summaries of topics using Wikipedia.
- **News Updates**: Fetches top headlines from The Times of India.
- **Google Search**: Searches Google for user queries.
- **YouTube Integration**: Plays videos on YouTube.
- **Email Sending**: Sends emails to predefined recipients.
- **Music Player**: Plays music from a local directory.
- **Note Taking**: Creates and opens notes using Notepad or Notepad++.
- **System Information**: Displays CPU, RAM, and battery usage.
- **Location Services**: Provides current location and distance to a specified place.
- **IP Address Retrieval**: Fetches the user's public IP address.
- **Window Switching**: Switches between open windows.
- **Screenshot Functionality**: Captures and saves screenshots.
- **File Visibility**: Hides or makes files visible in a folder.
- **Chat History**: Displays and manages past conversations.
- **Google Calendar Integration**: Fetches events from the user's Google Calendar.
- **Jokes**: Tells jokes using the `pyjokes` library.
- **DeepSeek Integration**: Answers complex queries using the DeepSeek AI model.
- **Voice Control**: Stops speech output when the Ctrl key is pressed.

## Requirements

To run this project, ensure you have the following:

1. **Python**: Version 3.7 or higher.
2. **Operating System**: Linux.
3. **Libraries and Dependencies**: Install the required Python libraries using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
4. **Microphone**: For voice input.
5. **Speaker or Headphones**: For audio output.
6. **Google Chrome**: Required for certain features like Google Search.
7. **API Keys**: Add your own API credentials for services like:
   - Weather (OpenWeatherMap API)
   - Google OAuth (for Calendar and other integrations)
   - News API (for fetching news headlines)
8. **Notepad++ (Optional)**: For enhanced note-taking functionality.

## Linux Dependencies

For the application to run correctly on Linux, you may need to install some system-level packages.

For Debian/Ubuntu-based distributions, you can install them using `apt-get`:

```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev python3-xlib
```

For other Linux distributions, please use your package manager to install the equivalent packages.

## DeepSeek Model Configuration

The application uses the `deepseek-r1:1.5b` parameter model by default, as it is optimized for basic-level laptops. If you have a more powerful computer or laptop, you can change the model to a higher parameter version for better performance and accuracy. Update the model configuration in the `deepseek_integration.py` file as per your requirements.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NIGASH333/J.A.R.V.I.S.git
   ```
2. Navigate to the project directory:
   ```bash
   cd JARVIS-master
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application:
   ```bash
   python main.py
   ```
2. Follow the voice prompts to interact with JARVIS.

## Configuration

- Update the `Jarvis/config.py` file with your API keys and other configuration settings as needed.
- Add your own API credentials for services like weather, Google OAuth, and others to ensure proper functionality.

## Screenshots

Below are some screenshots of the JARVIS Assistant in action:

1. **Main Interface**  
  ![image1](https://github.com/user-attachments/assets/5834ebf6-a790-4513-8fd9-e1f9bf57a2c2)

2. **Voice Commands**  
![image2](https://github.com/user-attachments/assets/9555f6c6-a493-45a0-9f5f-30e039233984)

3. **Chat History**  
![image3](https://github.com/user-attachments/assets/5b9c172e-bf67-409b-a49c-b7cdf949d0d9)

4. **Closing Chat Updates**  
![image4](https://github.com/user-attachments/assets/0f47cbae-4948-4c0b-9ad2-8811632a0e41)

5. **Deepseek-r1 Query**  
![image5](https://github.com/user-attachments/assets/2b1acd7f-b307-4865-8fcf-2fea2497982b)

6. **Voice Commands**  
![image6](https://github.com/user-attachments/assets/60b2073f-828d-4e7d-bc56-693d52c759b9)

7. **Weather Functionality**  
![image7](https://github.com/user-attachments/assets/67e15c00-ba83-4b60-9b9b-691b8ec3141f)



## Database

The application uses an SQL database to store chat history. Ensure that the database is set up correctly in `Jarvis/database.py`.

## Future Enhancements

Here are some ideas for improving the JARVIS Assistant in the future:

1. **Cross-Platform Support**: Done! The project is now compatible with Linux.
2. **Improved Voice Recognition**: Integrate advanced NLP models for better command understanding.
3. **Customizable Commands**: Allow users to define their own commands and actions.
4. **Multi-Language Support**: Add support for multiple languages for a broader audience.
5. **Mobile Integration**: Develop a mobile app to control JARVIS remotely.
6. **Enhanced Security**: Add user authentication and encryption for sensitive data.
7. **AI Model Upgrades**: Integrate more powerful AI models for better performance.
8. **Task Scheduling**: Enable users to schedule tasks and reminders.

## Contact

For any queries or support, feel free to contact:

- **Mobile**: 9345306576
- **Email**: [nigashnigash0845@gmail.com](mailto:nigashnigash0845@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the [GPL-3.0 License](LICENSE). 📝
