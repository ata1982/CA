import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    SRC_DIR = PROJECT_ROOT / "src"
    TASKS_DIR = PROJECT_ROOT / "tasks"
    LOGS_DIR = PROJECT_ROOT / "logs"
    WORKSPACE_DIR = PROJECT_ROOT / "workspace"
    
    DATABASE_PATH = PROJECT_ROOT / "tasks.db"
    
    CLAUDE_CODE_COMMAND = os.getenv("CLAUDE_CODE_COMMAND", "claude")
    CLAUDE_CODE_TIMEOUT = int(os.getenv("CLAUDE_CODE_TIMEOUT", "300"))
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def setup_logging(cls):
        cls.LOGS_DIR.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format=cls.LOG_FORMAT,
            handlers=[
                logging.FileHandler(cls.LOGS_DIR / "agent.log"),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)

config = Config()
logger = config.setup_logging()