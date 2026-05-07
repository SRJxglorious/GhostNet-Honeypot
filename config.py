import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "verbosity": int(os.getenv("VERBOSITY", 0)),
    "print_colorized": os.getenv("PRINT_COLORIZED", "true").lower() == "true",

    "ssh_config": {
        "hostname": os.getenv("SSH_HOSTNAME", "0.0.0.0"),
        "port": int(os.getenv("SSH_PORT", 2222)),
        "version": os.getenv("SSH_VERSION", "SSH-2.0-OpenSSH_7.4"),
    },
    "enable_api_server": os.getenv("ENABLE_API_SERVER", "true").lower() == "true",
    "api_server": {
        "listen_ip_address": os.getenv("API_SERVER_HOSTNAME", "0.0.0.0"),
        "listen_port": int(os.getenv("API_SERVER_PORT", 8000)),
        "CORS_origins": os.getenv("API_SERVER_CORS_ORIGINS", "").split(",") if os.getenv("API_SERVER_CORS_ORIGINS") else [],
    },
}