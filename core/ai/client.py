# core/ai/client.py
from typing import Dict, Any, Optional, List, Generator
from openai import OpenAI
import requests
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class LlmClient:
    """Client for interacting with LLM server."""
    def __init__(self, server_url: str = "http://127.0.0.1:1234/v1", api_key: str = "lm-studio"):
        """
        Initialize LLM client.

        Args:
            server_url: Base URL of the LLM server (default is LM Studio's default address)
            api_key: API key for authentication (default is LM Studio's default key)
        """
        self.server_url = server_url
        self.api_key = api_key
        self.client = OpenAI(base_url=server_url, api_key=api_key)
        logger.info(f"LlmClient initialized with server: {server_url}")

    def is_server_available(self) -> bool:
        """
        Check if the LLM server is available.
        
        Returns:
            Boolean indicating if server is accessible
        """
        try:
            response = requests.get(f"{self.server_url}/models", timeout=3)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking LLM server availability: {str(e)}")
            return False

    def query(self, text: str, prompt: str) -> Dict[str, Any]:
        """
        Send a query to the LLM server.
        
        Args:
            text: Text to analyze
            prompt: Prompt to send to the LLM
            
        Returns:
            Dictionary with LLM response
        """
        try:
            if not self.is_server_available():
                logger.error("LLM server is not available")
                return {"error": "LLM server is not available", "response": "Failed to connect to LLM server"}

            full_prompt = f"{prompt}\n\n{text}"

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ]

            logger.debug(f"Sending request to LLM server at {self.server_url}")

            response = self.client.chat.completions.create(
                model="local-model",
                messages=messages,
                temperature=0.7,
            )

            result = {
                "response": response.choices[0].message.content,
                "model": response.model
            }

            logger.info("LLM query successful")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying LLM: {str(e)}")
            return {"error": str(e), "response": "Failed to connect to LLM server"}
        except Exception as e:
            logger.error(f"Unexpected error in LLM query: {str(e)}")
            return {"error": str(e), "response": "Unexpected error in LLM query"}

    def query_stream(self, text: str, prompt: str) -> Generator[str, None, None]:
        """
        Send a query to the LLM server and stream the response.
        
        Args:
            text: Text to analyze
            prompt: Prompt to send to the LLM
            
        Yields:
            Chunks of the response as they become available
        """
        try:
            if not self.is_server_available():
                logger.error("LLM server is not available")
                yield "Error: LLM server is not available"
                return

            full_prompt = f"{prompt}\n\n{text}"

            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ]

            logger.debug(f"Sending streaming request to LLM server at {self.server_url}")

            stream = self.client.chat.completions.create(
                model="local-model",  # LM Studio uses this model name
                messages=messages,
                stream=True,
                temperature=0.7,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield content

            logger.info("LLM streaming query completed")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error in streaming LLM query: {str(e)}")
            yield f"Error: Failed to connect to LLM server - {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error in streaming LLM query: {str(e)}")
            yield f"Error: Unexpected error in LLM query - {str(e)}"
