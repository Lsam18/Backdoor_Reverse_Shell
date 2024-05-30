

```markdown
# Backdoor_Reverse_Shell

## Overview

This project is a comprehensive Remote Access Tool designed for ethical use in cybersecurity awareness and remote support scenarios. It allows remote control and monitoring of a target machine with features such as screen streaming, webcam snapshots, file transfer, and location retrieval.

## Features

- **Remote Screen Streaming**: View the target's screen in real-time.
- **Screenshot Capture**: Capture screenshots of the target's screen on command.
- **Webcam Snapshots & Video**: Capture images and record video from the target's webcam.
- **File Transfer**: Seamlessly download files from the target machine.
- **Location Retrieval**: Fetch the target's location based on IP address.
- **Command Execution**: Execute shell commands remotely.
- **User-Friendly Target Deployment**: The target application runs as an executable, making deployment easy and efficient.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python libraries: `socket`, `threading`, `cv2`, `numpy`, `pyautogui`, `geocoder`, `subprocess`

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Lsam18/Backdoor_Reverse_Shell.git
   cd Backdoor_Reverse_Shell
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**

   ```bash
   python3 server.py
   ```

4. **Build the Target Executable**

   To convert the client script into an executable, use a tool like PyInstaller:

   ```bash
   pyinstaller --onefile client.py
   ```

   The executable will be found in the `dist` directory.

## Usage

### Server

1. **Start the Server**

   ```bash
   python3 server.py
   ```

   The server will start listening for connections on the specified IP and port.

2. **Interact with the Target**

   Once a target connects, you can issue various commands to control and monitor the target machine.

### Target

1. **Run the Executable**

   The target user needs to run the generated executable. Upon execution, the target machine will connect to the server, and you will be able to control it using the server interface.

## Commands

- `remote_screen`: Start remote screen streaming.
- `stop_streaming`: Stop the remote screen streaming.
- `screenshot`: Capture a screenshot of the target's screen.
- `webcam_snapshot`: Capture a snapshot from the target's webcam.
- `webcam_video <duration>`: Record a video from the target's webcam for the specified duration (in seconds).
- `location`: Retrieve the target's location based on IP address.
- `cd <directory>`: Change directory on the target machine.
- `ls`: List files in the current directory on the target machine.
- `download <file>`: Download the specified file from the target machine.
- `<any shell command>`: Execute any shell command on the target machine.

## Disclaimer

This tool is intended for ethical use only. The author is not responsible for any misuse of this tool. Always ensure you have proper authorization before using it to monitor or control any device.

## Future Improvements

- Enhance security with encryption for data transmission.
- Add more features such as keylogging and audio capture.
- Improve error handling and robustness.
- Create a graphical user interface (GUI) for the server.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspiration from various open-source projects in the cybersecurity domain.
- Special thanks to the contributors and the open-source community for their valuable resources and support.

---

Feel free to explore, use, and enhance this project. Your feedback and contributions are highly appreciated!

