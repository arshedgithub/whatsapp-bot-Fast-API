from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel

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
        # Define keywords and patterns for different types of queries
        self.patterns = {
            ResponseType.HUMAN: [
                "speak to human",
                "talk to agent",
                "connect to support",
                "customer service"
            ],
            ResponseType.PRODUCT_INFO: [
                "product",
                "price",
                "cost",
                "available",
                "stock",
                "catalog",
                "show me products"
            ],
            ResponseType.ORDER_STATUS: [
                "order",
                "tracking",
                "delivery",
                "shipping"
            ],
            ResponseType.CUSTOMER_SUPPORT: [
                "help",
                "support",
                "issue",
                "problem",
                "complaint"
            ],
            ResponseType.FORM: [
                "register",
                "sign up",
                "create account",
                "place order",
                "book appointment"
            ]
        }

    async def analyze_query(self, query: str) -> QueryIntent:
        """Analyze the user query and determine the appropriate response type."""
        query = query.lower()
        
        # Check for human connection request first
        if any(pattern in query for pattern in self.patterns[ResponseType.HUMAN]):
            return QueryIntent(
                type=ResponseType.HUMAN,
                confidence=0.9,
                metadata={"reason": "Explicit request for human connection"}
            )

        # Check for product-related queries
        if any(pattern in query for pattern in self.patterns[ResponseType.PRODUCT_INFO]):
            return QueryIntent(
                type=ResponseType.PRODUCT_INFO,
                confidence=0.8,
                metadata={"category": "product_inquiry"},
                ui_type="catalog"  # Specify UI type for product queries
            )

        # Check for form-related queries
        if any(pattern in query for pattern in self.patterns[ResponseType.FORM]):
            return QueryIntent(
                type=ResponseType.FORM,
                confidence=0.8,
                metadata={"category": "form_request"},
                ui_type="form"  # Specify UI type for form requests
            )

        # Check for order-related queries
        if any(pattern in query for pattern in self.patterns[ResponseType.ORDER_STATUS]):
            return QueryIntent(
                type=ResponseType.ORDER_STATUS,
                confidence=0.8,
                metadata={"category": "order_inquiry"},
                ui_type="buttons"  # Specify UI type for order status
            )

        # Check for support-related queries
        if any(pattern in query for pattern in self.patterns[ResponseType.CUSTOMER_SUPPORT]):
            return QueryIntent(
                type=ResponseType.CUSTOMER_SUPPORT,
                confidence=0.7,
                metadata={"category": "support_request"},
                ui_type="list"  # Specify UI type for support options
            )

        # Default to text response if no specific intent is detected
        return QueryIntent(
            type=ResponseType.TEXT,
            confidence=0.6,
            metadata={"category": "general_query"}
        )

reasoning_service = ReasoningService() 