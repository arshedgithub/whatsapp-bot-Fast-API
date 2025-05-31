from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.integrations import groq_client

class ResponseType(Enum):
    TEXT = "text"
    CATALOG = "catalog"
    FORM = "form"
    BUTTONS = "buttons"
    LIST = "list"
    HUMAN = "human"
    PRODUCT_INFO = "product_info"
    ORDER_STATUS = "order_status"
    CUSTOMER_SUPPORT = "customer_support"

class QueryIntent(BaseModel):
    type: ResponseType
    confidence: float
    metadata: Dict[str, Any] = {}
    ui_type: Optional[str] = None

class ReasoningService:
    def __init__(self):
        self.intent_prompt = """Analyze the user's message and determine the most appropriate response type.
Available response types:
- TEXT: General conversation or questions
- CATALOG: Product inquiries, pricing, or browsing
- FORM: Registration, sign up, or data collection
- BUTTONS: Options that need user selection
- LIST: Multiple options with descriptions
- HUMAN: Request to speak with a human agent
- PRODUCT_INFO: Specific product details
- ORDER_STATUS: Order tracking or history
- CUSTOMER_SUPPORT: Help or support requests

Respond in JSON format with:
{
    "type": "RESPONSE_TYPE",
    "confidence": 0.0-1.0,
    "metadata": {
        "category": "specific_category",
        "reason": "explanation"
    },
    "ui_type": "specific_ui_component_if_needed"
}"""

    async def analyze_query(self, query: str) -> QueryIntent:
        """Use Groq to analyze the user query and determine the appropriate response type."""
        try:
            # Prepare the prompt with the user's query
            full_prompt = f"{self.intent_prompt}\n\nUser message: {query}\n\nAnalysis:"
            
            print("Full prompt: ", full_prompt)

            # Get response from Groq
            response = await groq_client.get_response(full_prompt)
            analysis = response.get("answer", "{}")
            
            # Parse the response (assuming it's valid JSON)
            import json
            try:
                result = json.loads(analysis)
                
                # Map the response type string to enum
                response_type = ResponseType[result.get("type", "TEXT")]
                
                return QueryIntent(
                    type=response_type,
                    confidence=float(result.get("confidence", 0.6)),
                    metadata=result.get("metadata", {}),
                    ui_type=result.get("ui_type")
                )
            except json.JSONDecodeError:
                print(f"Failed to parse Groq response as JSON: {analysis}")
                return self._fallback_intent()
                
        except Exception as e:
            print(f"Error in reasoning service: {str(e)}")
            return self._fallback_intent()

    def _fallback_intent(self) -> QueryIntent:
        """Provide a fallback intent when analysis fails."""
        return QueryIntent(
            type=ResponseType.TEXT,
            confidence=0.6,
            metadata={"category": "fallback", "reason": "Error in analysis"},
            ui_type=None
        )

reasoning_service = ReasoningService() 