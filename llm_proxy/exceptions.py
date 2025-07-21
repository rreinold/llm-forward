class LLMForwardError(Exception):
    """Base exception for LLM proxy forwarding errors."""
    pass

class LLMForwardConfigError(LLMForwardError):
    """Raised when there is a configuration error in LLM proxy forwarding."""
    pass 