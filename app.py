import asyncio
import os
from typing import Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AgentState(Enum):
    """Enum for tracking agent states"""
    INTENT_DETECTION = "intent_detection"
    AUTHENTICATION = "authentication"
    TERMINAL = "terminal"
    SUCCESS = "success"

@dataclass
class ConversationContext:
    """Context to track conversation state"""
    current_state: AgentState = AgentState.INTENT_DETECTION
    auth_attempts: int = 0
    auth_question_stage: int = 0
    authenticated: bool = False
    intent: Optional[str] = None
    history: ChatHistory = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = ChatHistory()

class IntentDetectionAgent:
    """Agent responsible for detecting user intent"""
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.chat_service = kernel.get_service("chat")
        
    @kernel_function(
        name="detect_intent",
        description="Detects the user's intent from their message"
    )
    async def detect_intent(self, user_message: str) -> Tuple[str, str]:
        """
        Detects intent from user message
        Returns: (intent_type, response_message)
        """
        prompt = f"""
        Analyze the following user message and determine their intent.
        
        User message: "{user_message}"
        
        Classify the intent as one of the following:
        - "account_balance": If the user wants to check account balance, account details, or similar banking information
        - "other": For any other request
        
        Respond in the format:
        INTENT: [intent_type]
        RESPONSE: [appropriate response based on intent]
        
        If intent is "account_balance", respond with: "I can help you check your account balance. Let me verify your identity first."
        If intent is "other", respond with: "I'm sorry, I can only help with account balance inquiries at this time."
        """
        
        settings = AzureChatPromptExecutionSettings(
            temperature=0.1,
            max_tokens=150
        )
        
        response = await self.chat_service.get_chat_message_content(
            chat_history=ChatHistory(messages=[{"role": "user", "content": prompt}]),
            settings=settings
        )
        
        # Parse response
        response_text = str(response)
        intent = "other"
        
        if "INTENT: account_balance" in response_text:
            intent = "account_balance"
            message = "I can help you check your account balance. Let me verify your identity first."
        else:
            message = "I'm sorry, I can only help with account balance inquiries at this time."
            
        return intent, message

class AuthenticationAgent:
    """Agent responsible for user authentication"""
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.questions = [
            ("What is 20 + 20?", "40"),
            ("What is 10 + 10?", "20")
        ]
        
    @kernel_function(
        name="authenticate_user",
        description="Authenticates the user with security questions"
    )
    async def authenticate_user(self, user_answer: str, question_stage: int) -> Tuple[bool, str, bool]:
        """
        Authenticates user based on their answer
        Returns: (is_correct, response_message, authentication_complete)
        """
        if question_stage >= len(self.questions):
            return False, "Authentication process error.", True
            
        question, correct_answer = self.questions[question_stage]
        
        # Check if answer is correct
        user_answer = user_answer.strip().lower()
        is_correct = user_answer == correct_answer.lower()
        
        if not is_correct:
            return False, f"That's incorrect. {question}", False
            
        # If this was the last question
        if question_stage == len(self.questions) - 1:
            return True, "Authentication successful! You can now access your account balance. Your current balance is $1,234.56.", True
            
        # Move to next question
        next_question = self.questions[question_stage + 1][0]
        return True, f"Correct! Next question: {next_question}", False
    
    def get_current_question(self, stage: int) -> str:
        """Get the current authentication question"""
        if stage < len(self.questions):
            return self.questions[stage][0]
        return ""

class MultiAgentOrchestrator:
    """Orchestrates the flow between different agents"""
    
    def __init__(self):
        # Initialize kernel
        self.kernel = Kernel()
        
        # Add Azure OpenAI service
        self.kernel.add_service(
            AzureChatCompletion(
                service_id="chat",
                deployment_name=os.getenv("AZURE_OPENAI_GPT_4_1_DEPLOYMENT_NAME"),
                endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            )
        )
        
        # Initialize agents
        self.intent_agent = IntentDetectionAgent(self.kernel)
        self.auth_agent = AuthenticationAgent(self.kernel)
        
        # Initialize context
        self.context = ConversationContext()
        
    async def _check_topic_change(self, user_input: str) -> bool:
        """Use AI to detect if user is trying to change topic during authentication"""
        prompt = f"""
        During an authentication process where I asked a math question, the user responded with: "{user_input}"
        
        Determine if the user is:
        1. Attempting to answer the math question (even if incorrect)
        2. Trying to change the topic or avoid authentication
        
        Examples of answering: "40", "thirty", "I think it's 50", "um... 45?"
        Examples of changing topic: "I need help with something else", "can you do something different", "forget that"
        
        Respond with only: ANSWERING or CHANGING_TOPIC
        """
        
        settings = AzureChatPromptExecutionSettings(
            temperature=0.1,
            max_tokens=20
        )
        
        chat_service = self.kernel.get_service("chat")
        response = await chat_service.get_chat_message_content(
            chat_history=ChatHistory(messages=[{"role": "user", "content": prompt}]),
            settings=settings
        )
        
        return "CHANGING_TOPIC" in str(response)
        
    async def process_user_input(self, user_input: str) -> str:
        """
        Process user input based on current state
        Returns the response to the user
        """
        self.context.history.add_user_message(user_input)
        
        if self.context.current_state == AgentState.INTENT_DETECTION:
            return await self._handle_intent_detection(user_input)
            
        elif self.context.current_state == AgentState.AUTHENTICATION:
            return await self._handle_authentication(user_input)
            
        elif self.context.current_state == AgentState.TERMINAL:
            return "This conversation has ended. Please start a new session."
            
        elif self.context.current_state == AgentState.SUCCESS:
            return "You have successfully accessed your account information. Is there anything else I can help you with?"
            
    async def _handle_intent_detection(self, user_input: str) -> str:
        """Handle intent detection state"""
        intent, response = await self.intent_agent.detect_intent(user_input)
        self.context.intent = intent
        
        if intent == "account_balance":
            self.context.current_state = AgentState.AUTHENTICATION
            # Add first authentication question
            first_question = self.auth_agent.get_current_question(0)
            response += f"\n\nPlease answer the following security question: {first_question}"
        else:
            self.context.current_state = AgentState.TERMINAL
            
        self.context.history.add_assistant_message(response)
        return response
        
    async def _handle_authentication(self, user_input: str) -> str:
        """Handle authentication state"""
        # Use AI to check if user is trying to change topic
        is_changing_topic = await self._check_topic_change(user_input)
        
        if is_changing_topic:
            self.context.auth_attempts += 1
            if self.context.auth_attempts >= 3:
                self.context.current_state = AgentState.TERMINAL
                response = "Maximum authentication attempts exceeded. This session has ended for security reasons."
                self.context.history.add_assistant_message(response)
                return response
            
            current_question = self.auth_agent.get_current_question(self.context.auth_question_stage)
            response = f"Please complete the authentication process first. {current_question} (Attempt {self.context.auth_attempts + 1}/3)"
            self.context.history.add_assistant_message(response)
            return response
            
        # Process authentication
        is_correct, response, auth_complete = await self.auth_agent.authenticate_user(
            user_input, 
            self.context.auth_question_stage
        )
        
        if not is_correct:
            self.context.auth_attempts += 1
            if self.context.auth_attempts >= 3:
                self.context.current_state = AgentState.TERMINAL
                response = "Maximum authentication attempts exceeded. This session has ended for security reasons."
            else:
                response += f" (Attempt {self.context.auth_attempts + 1}/3)"
        else:
            if auth_complete:
                self.context.current_state = AgentState.SUCCESS
                self.context.authenticated = True
            else:
                self.context.auth_question_stage += 1
                # Reset attempts for next question
                self.context.auth_attempts = 0
                
        self.context.history.add_assistant_message(response)
        return response

async def main():
    """Main function to run the multi-agent system"""
    print("=== Multi-Agent Banking Assistant ===")
    print("I can help you check your account balance.")
    print("Type 'quit' to exit.\n")
    
    orchestrator = MultiAgentOrchestrator()
    
    while True:
        # Check if we're in terminal state
        if orchestrator.context.current_state == AgentState.TERMINAL:
            print("\n[Session ended]")
            break
            
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nGoodbye!")
            break
            
        response = await orchestrator.process_user_input(user_input)
        print(f"\nAssistant: {response}")
        
        # If we reached success state, end the conversation
        if orchestrator.context.current_state == AgentState.SUCCESS:
            print("\n[Account balance retrieved successfully]")
            break

if __name__ == "__main__":
    asyncio.run(main())