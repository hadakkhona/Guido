# config.py — All settings and constants for Guido

class Config:

    # ----------------------------
    # Robot identity
    # ----------------------------
    ROBOT_NAME      = "Guido"
    VERSION         = "0.1.0"

    # ----------------------------
    # Serial communication (Arduino Mega)
    # ----------------------------
    SERIAL_PORT     = "/dev/ttyUSB0"   # Linux — change to "COM3" etc. on Windows
    BAUDRATE        = 9600

    # ----------------------------
    # AI Model (Ollama)
    # ----------------------------
    OLLAMA_URL      = "http://localhost:11434"
    MODEL_NAME      = "gemma2:2b"

    # ----------------------------
    # Voice & Language
    # ----------------------------
    LANGUAGE        = "en-US"          # Change to "fr-FR", "ar-MA" etc. if needed
    SPEECH_RATE     = 150              # Words per minute for TTS
    SPEECH_VOLUME   = 1.0              # 0.0 to 1.0

    # ----------------------------
    # Camera
    # ----------------------------
    CAMERA_INDEX    = 0                # 0 = default camera
    FRAME_WIDTH     = 640
    FRAME_HEIGHT    = 480

    # ----------------------------
    # Timeouts & Delays
    # ----------------------------
    NLU_TIMEOUT     = 15               # Seconds to wait for Ollama response
    LOOP_DELAY      = 0.5              # Delay between main loop iterations
    ERROR_DELAY     = 1.0             # Delay after an error before retrying

    # RFID (RC522 via SPI)
    RFID_RST_PIN = 22
    RFID_SDA_PIN = 24   # also called SS/CS
    RFID_COOLDOWN = 2.0  # seconds between scans
