# workers/ai_workers.py
from workers.base import BaseWorker
from core.ai.client import LlmClient
from core.analysis.text_splitter import split_text
from utils.logging_config import setup_logger

logger = setup_logger(__name__)

class LlmQueryWorker(BaseWorker):
    """Worker thread for querying LLM server with text chunks."""
    def __init__(self, file_path, question, server_url="http://127.0.0.1:1234/v1", 
                 api_key="lm-studio", chunk_size=4000, overlap=200):
        super().__init__()
        self.file_path = file_path
        self.question = question
        self.server_url = server_url
        self.api_key = api_key
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.client = LlmClient(server_url=server_url, api_key=api_key)
        logger.debug(f"LlmQueryWorker initialized for file: {file_path}")

    def run(self):
        try:
            if not self.client.is_server_available():
                logger.error("LLM server is not available")
                self.signals.finished.emit(False, "LLM server is not available. Make sure LM Studio is running.")
                return

            logger.info(f"Reading file: {self.file_path}")
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            logger.info(f"Splitting text into chunks (size: {self.chunk_size}, overlap: {self.overlap})")
            chunks = split_text(text, self.chunk_size, self.overlap)
            logger.info(f"Split text into {len(chunks)} chunks")

            all_responses = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")

                result = self.client.query(chunk, self.question)

                if "error" in result:
                    response = f"Error processing chunk {i+1}: {result['error']}"
                    logger.warning(f"Error in chunk {i+1}: {result['error']}")
                else:
                    response = result.get('response', f"No response for chunk {i+1}")

                all_responses.append(response)

            if len(all_responses) == 1:
                final_response = all_responses[0]
            else:
                final_response = "# Aggregated Responses\n\n"
                for i, response in enumerate(all_responses):
                    final_response += f"## Chunk {i+1} Response\n\n{response}\n\n"
                final_response += f"\n## Summary\nThe above responses were generated from {len(chunks)} different sections of the document in response to your question: '{self.question}'"

            logger.info(f"LLM processing complete, aggregated {len(all_responses)} responses")
            self.signals.finished.emit(True, final_response)

        except Exception as e:
            logger.error(f"Error in LLM query: {str(e)}", exc_info=True)
            self.signals.finished.emit(False, f"Error querying LLM: {str(e)}")
