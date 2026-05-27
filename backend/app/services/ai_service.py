"""AI Service for interacting with AI models."""

import time
from typing import Optional, List, Dict, Any, Tuple

from app.core.config import settings


class AIService:
    """Service for AI model interactions."""

    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.anthropic_api_key = settings.anthropic_api_key
        self.default_model = "gpt-4-turbo-preview"

    async def chat(
        self,
        message: str,
        history: List[Any] = None,
        context: Optional[Dict] = None,
        model: Optional[str] = None
    ) -> Tuple[str, int, str]:
        """
        Send a chat message and get response.
        Returns (response_text, tokens_used, model_name).
        """
        # Build messages array with history
        messages = []
        
        # Add system prompt
        system_prompt = self._build_system_prompt(context)
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        if history:
            for msg in history:
                role = "user" if msg.role.value == "user" else "assistant"
                messages.append({"role": role, "content": msg.content})
        
        # Add current message
        messages.append({"role": "user", "content": message})

        # In production, call actual AI API
        # For demo, return a simulated response
        return self._simulate_response(message), 100, model or self.default_model

    async def generate_embeddings(
        self,
        texts: List[str],
        model: str = "text-embedding-ada-002"
    ) -> List[List[float]]:
        """Generate embeddings for texts."""
        # In production, call OpenAI embeddings API
        # Return simulated embeddings
        return [[0.1] * 1536 for _ in texts]

    async def moderate_content(
        self,
        text: str
    ) -> Dict[str, Any]:
        """Check content for policy violations."""
        # Check for common inappropriate content
        blocked_words = ["violence", "hate", "explicit"]
        
        flagged = any(word in text.lower() for word in blocked_words)
        
        return {
            "flagged": flagged,
            "categories": {
                "violence": flagged,
                "hate": flagged,
                "sexual": False,
                "self_harm": False
            },
            "category_scores": {
                "violence": 0.1 if flagged else 0.0,
                "hate": 0.1 if flagged else 0.0,
                "sexual": 0.0,
                "self_harm": 0.0
            }
        }

    async def stream_chat(
        self,
        message: str,
        history: List[Any] = None,
        context: Optional[Dict] = None,
        model: Optional[str] = None
    ):
        """
        Stream chat response.
        Yields chunks of response text.
        """
        # Generate response
        response, _, _ = await self.chat(message, history, context, model)
        
        # Stream response in chunks
        words = response.split()
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            await self._sleep(0.05)  # Simulate streaming delay

    def _build_system_prompt(self, context: Optional[Dict]) -> str:
        """Build system prompt with context."""
        base_prompt = """You are AI Nexus Assistant, a helpful AI assistant. 

Guidelines:
- Be helpful, informative, and concise
- Follow safety guidelines
- Admit when you don't know something
- Provide accurate information
- Be respectful and professional
"""
        if context and context.get("user_name"):
            base_prompt += f"\n- The user's name is {context['user_name']}"

        return base_prompt

    def _simulate_response(self, message: str) -> str:
        """Simulate AI response for demo purposes."""
        message_lower = message.lower()
        
        if "help" in message_lower or "what can you do" in message_lower:
            return """I can help you with a variety of tasks:

1. **Answer Questions** - I can explain concepts, provide information, and help with research.

2. **Write & Edit** - I can help write emails, reports, code, and other content.

3. **Analysis** - I can analyze data, documents, and provide insights.

4. **Automation** - I can help set up automated workflows and processes.

5. **Problem Solving** - I can help break down problems and find solutions.

How can I assist you today?"""

        elif "analyze" in message_lower or "analysis" in message_lower:
            return """I'd be happy to help with analysis! To provide the most accurate insights, please share:

- What specific data or topic you'd like analyzed
- Any context or background information
- The format you'd prefer for the output (report, summary, etc.)

You can also connect your data sources or upload documents directly for me to analyze."""

        elif "automate" in message_lower or "automation" in message_lower:
            return """I can help you build automation workflows! Here's how:

1. **Describe your workflow** - Tell me what repetitive task you want to automate
2. **Define triggers** - What should start the automation (schedule, event, etc.)
3. **Set actions** - What should happen when triggered
4. **Add conditions** - Any filters or conditions for specific cases

You can use our visual workflow builder or describe your needs in natural language. What would you like to automate?"""

        elif any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
            return "Hello! I'm your AI assistant. How can I help you today?"

        elif "thanks" in message_lower or "thank you" in message_lower:
            return "You're welcome! Is there anything else I can help you with?"

        else:
            return f"""I understand you're asking about: "{message[:50]}..."

I can help with that! Could you provide more details so I can give you a more specific and helpful response?

Here are some things I can help with:
- Answering questions and explaining concepts
- Writing and editing content
- Analyzing data and documents
- Setting up automations
- Problem solving and brainstorming"""

    async def _sleep(self, seconds: float):
        """Async sleep helper."""
        import asyncio
        await asyncio.sleep(seconds)