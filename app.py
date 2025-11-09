"""
StackQL Cloud Intelligence Demo
A Streamlit-based chat interface for querying cloud infrastructure using StackQL and OpenAI.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from openai_stackql_agent import OpenAIStackQLAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="StackQL Cloud Intelligence",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# System prompt for the agent
SYSTEM_PROMPT = """You are a helpful cloud infrastructure assistant powered by StackQL.

You can help users query and analyze their cloud resources across multiple cloud providers including
Google Cloud, AWS, Azure, GitHub, Okta, and many others.

Your capabilities include:
- Listing available cloud providers and their services
- Discovering resources and methods available in each service
- Executing StackQL queries to retrieve detailed information about cloud infrastructure
- Analyzing and summarizing cloud resource configurations
- Helping users understand their cloud estate

When a user asks about their cloud resources:
1. First, determine which provider and service they're asking about
2. Use the appropriate tools to explore available resources
3. Construct and execute StackQL queries to get the information
4. Present the results in a clear, organized manner
5. Provide insights and recommendations when relevant

Always be specific and accurate. If you need more information from the user (like project IDs,
region names, etc.), ask for it before constructing queries.

Example queries you can help with:
- "Show me all my Google Cloud compute instances"
- "List all AWS S3 buckets in my account"
- "What Azure resources do I have in the East US region?"
- "Show me GitHub repositories in my organization"
- "List all my Okta users and their status"
"""


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        stackql_mcp_url = os.getenv("STACKQL_MCP_URL", "http://127.0.0.1:9912")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        if not openai_api_key:
            st.error("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
            st.stop()

        try:
            st.session_state.agent = OpenAIStackQLAgent(
                openai_api_key=openai_api_key,
                stackql_mcp_url=stackql_mcp_url,
                model=model
            )
        except Exception as e:
            st.error(f"Failed to initialize agent: {str(e)}")
            st.stop()


def display_chat_history():
    """Display the chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()

    # Header
    st.markdown('<div class="main-header">☁️ StackQL Cloud Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Query and analyze your cloud infrastructure using natural language</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Display current settings
        st.info(f"""
        **Model:** {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}
        **StackQL MCP:** {os.getenv('STACKQL_MCP_URL', 'http://127.0.0.1:9912')}
        """)

        st.divider()

        st.header("💡 Example Questions")
        example_questions = [
            "What cloud providers are available?",
            "Show me Google Cloud services",
            "List compute resources in Google Cloud",
            "What instances are running in my GCP project?",
            "Show me all my AWS EC2 instances",
            "List Azure virtual machines",
            "What GitHub repositories do I have access to?",
        ]

        for question in example_questions:
            if st.button(question, key=question):
                # Add the question to the chat
                st.session_state.messages.append({"role": "user", "content": question})
                st.rerun()

        st.divider()

        # Clear conversation button
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.agent.reset_conversation()
            st.rerun()

        st.divider()

        # Info section
        st.header("ℹ️ About")
        st.markdown("""
        This demo showcases **StackQL's MCP (Model Context Protocol)** integration with OpenAI.

        **StackQL** allows you to query cloud infrastructure using SQL-like syntax across
        multiple providers.

        **Features:**
        - Natural language cloud queries
        - Multi-provider support
        - Real-time infrastructure insights
        - AI-powered analysis
        """)

        # Connection status
        st.divider()
        st.header("🔌 Connection Status")

        try:
            # Test connection to StackQL MCP
            greeting = st.session_state.agent.stackql_client.greet("Streamlit")
            st.success("✅ Connected to StackQL MCP")
        except Exception as e:
            st.error(f"❌ StackQL MCP connection failed: {str(e)}")
            st.warning("""
            Make sure StackQL MCP server is running:
            ```bash
            stackql mcp --mcp.server.type=http --mcp.config '{"server": {"transport": "http", "address": "127.0.0.1:9912"}}'
            ```
            """)

    # Main chat interface
    st.divider()

    # Display chat history
    display_chat_history()

    # Check if there's a pending user message that needs a response
    # (happens when example buttons are clicked)
    if (len(st.session_state.messages) > 0 and
        st.session_state.messages[-1]["role"] == "user" and
        (len(st.session_state.messages) == 1 or
         st.session_state.messages[-2]["role"] == "assistant")):

        # Get the last user message
        user_message = st.session_state.messages[-1]["content"]

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Count how many times system prompt has been used
                    user_messages_count = sum(1 for msg in st.session_state.messages if msg["role"] == "user")

                    # If this is the first message, include the system prompt
                    if user_messages_count == 1:
                        response = st.session_state.agent.chat(user_message, system_prompt=SYSTEM_PROMPT)
                    else:
                        response = st.session_state.agent.chat(user_message)

                    st.markdown(response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Chat input
    if prompt := st.chat_input("Ask about your cloud infrastructure..."):
        # Add user message to chat history and rerun to process it
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()


if __name__ == "__main__":
    main()
