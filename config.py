"""
ACDSYN Configuration Management
Centralized configuration with environment-aware settings and validation
"""
import os
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DomainType(str, Enum):
    """Supported domain types for cross-domain synthesis"""
    DATA_SCIENCE = "data_science"
    SOFTWARE_ENGINEERING = "software_engineering"
    RESEARCH = "research"
    AUTOMATION = "automation"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    
class SynthesisStrategy(str, Enum):
    """Available synthesis strategies"""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    HYBRID = "hybrid"
    EMERGENT = "emergent"

class LogLevel(str, Enum):
    """Logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ACDSYNConfig(BaseSettings):
    """Main configuration class with validation"""
    
    # Firebase Configuration
    firebase_project_id: str = Field(..., env="FIREBASE_PROJECT_ID")
    firebase_credentials_path: Path = Field(..., env="FIREBASE_CREDENTIALS_PATH")
    firestore_collection_prefix: str = "acdsyn_"
    
    # Network Configuration
    max_domain_connections: int = 100
    synthesis_timeout_seconds: int = 300
    retry_attempts: int = 3
    retry_delay_seconds: int = 5
    
    # Performance Configuration
    metrics_collection_interval: int = 60  # seconds
    optimization_cycle_hours: int = 24
    performance_threshold: float = 0.8
    
    # Logging Configuration
    log_level: LogLevel = LogLevel.INFO
    log_format: str = "json"
    enable_structured_logging: bool = True
    
    # Synthesis Configuration
    default_strategy: SynthesisStrategy = SynthesisStrategy.HYBRID
    enable_emergent_behavior: bool = True
    max_synthesis_depth: int = 5
    compatibility_threshold: float = 0.7
    
    # Domain-Specific Configuration
    domain_configs: Dict[DomainType, Dict[str, Any]] = {
        DomainType.DATA_SCIENCE: {
            "max_components": 50,
            "allowed_libraries": ["pandas", "numpy", "scikit-learn"],
            "data_requirements": ["clean", "structured"]
        },
        DomainType.SOFTWARE_ENGINEERING: {
            "max_components": 100,
            "allowed_languages": ["python", "javascript"],
            "code_standards": ["pep8", "eslint"]
        }
    }
    
    @validator("firebase_credentials_path")
    def validate_credentials_path(cls, v):
        """Ensure Firebase credentials file exists"""
        if not v.exists():
            raise FileNotFoundError(f"Firebase credentials not found at {v}")
        return v
    
    @validator("compatibility_threshold")
    def validate_threshold(cls, v):
        """Ensure threshold is between 0 and 1"""
        if not 0 <= v <= 1:
            raise ValueError("compatibility_threshold must be between 0 and 1")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Singleton configuration instance
_config: Optional[ACDSYNConfig] = None

def get_config() -> ACDSYNConfig:
    """Get or create configuration singleton"""
    global _config
    if _config is None:
        try:
            _config = ACDSYNConfig()
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration: {e}")
    return _config

def load_yaml_config(path: Path) -> Dict[str, Any]:
    """Load additional configuration from YAML file"""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, 'r') as f:
        return yaml.safe_load(f)