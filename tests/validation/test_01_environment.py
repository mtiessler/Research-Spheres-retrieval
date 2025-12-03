import pytest
import sys
import os
from pathlib import Path
from dotenv import load_dotenv


def test_python_version():
    version = sys.version_info
    assert version.major == 3, "Python 3 required"
    assert version.minor >= 9, f"Python 3.9+ required, found {version.major}.{version.minor}"
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")


def test_virtual_environment():
    in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    assert in_venv, "Not running in virtual environment. Activate venv first."
    print(f"Virtual environment: {sys.prefix}")


def test_dependencies_installed():
    required_packages = [
        'neo4j',
        'chromadb',
        'sentence_transformers',
        'torch',
        'transformers',
        'pytest',
        'yaml'
    ]

    for package in required_packages:
        try:
            __import__(package)
            print(f"Package '{package}' installed")
        except ImportError:
            pytest.fail(f"Required package '{package}' not installed")


def test_env_file_exists():
    env_path = Path('.env')
    assert env_path.exists(), ".env file not found. Copy from .env.example"
    print(f".env file found at: {env_path.absolute()}")


def test_env_variables_loaded():
    load_dotenv()

    neo4j_password = os.getenv('NEO4J_PASSWORD')
    assert neo4j_password is not None, "NEO4J_PASSWORD not set in .env"
    assert len(neo4j_password) > 0, "NEO4J_PASSWORD is empty"
    print("Environment variables loaded successfully")


def test_config_file_exists():
    config_path = Path('config/config.yaml')
    assert config_path.exists(), "config/config.yaml not found"
    print(f"Config file found at: {config_path.absolute()}")


def test_config_loads():
    from config.settings import get_settings

    settings = get_settings()
    assert settings is not None

    # Check key settings
    neo4j_uri = settings.get('neo4j', 'uri')
    embedding_model = settings.get('embeddings', 'model_name')

    assert neo4j_uri is not None, "neo4j.uri not in config"
    assert embedding_model is not None, "embeddings.model_name not in config"

    print(f"Neo4j URI: {neo4j_uri}")
    print(f"Embedding model: {embedding_model}")


def test_directory_structure():
    required_dirs = [
        'embeddings',
        'vector_store',
        'hybrid_search',
        'subgraph_extraction',
        'rag',
        'config',
        'tests',
        'scripts'
    ]

    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        assert dir_path.exists(), f"Directory '{dir_name}' not found"
        assert dir_path.is_dir(), f"'{dir_name}' is not a directory"

    print("All required directories exist")