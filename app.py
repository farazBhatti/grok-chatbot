from swarmauri.standard.llms.concrete.GroqModel import GroqModel
from swarmauri.standard.messages.concrete.SystemMessage import SystemMessage
from swarmauri.standard.agents.concrete.SimpleConversationAgent import SimpleConversationAgent
from swarmauri.standard.conversations.concrete.MaxSystemContextConversation import MaxSystemContextConversation
import gradio as gr
import os
from dotenv import load_dotenv
# Fetch the API key from environment variables

load_dotenv()

# Fetch the API key from environment variables
API_KEY = os.getenv("GROQ_API_KEY")


# Initialize the GroqModel with the API key to access allowed models
llm = GroqModel(api_key=API_KEY)

# Get the available models from the llm instance
allowed_models = llm.allowed_models

# Initialize a MaxSystemContextConversation instance
conversation = MaxSystemContextConversation()

# Define a function to dynamically change the model based on dropdown input
def load_model(selected_model):
    return GroqModel(api_key=API_KEY, name=selected_model)

# Define the function to interact with the agent
def converse(input_text, history, system_context, model_name):
    print(f"System context: {system_context}")
    print(f"Selected model: {model_name}")

    # Initialize the model dynamically based on user selection
    llm = load_model(model_name)

    # Initialize the agent with the new model
    agent = SimpleConversationAgent(llm=llm, conversation=conversation)

    # Set the system context for the agent
    agent.conversation.system_context = SystemMessage(content=system_context)
        # Ensure input text is a string
    input_text = str(input_text)

    print(conversation.history)

    # Execute the input command with the agent
    result = agent.exec(input_text)

    print(result, type(result))

    # Return the result as a string
    return str(result)

# Set up the Gradio ChatInterface with a dropdown for model selection
interface = gr.ChatInterface(
    fn=converse,
    additional_inputs=[
        gr.Textbox(label="System Context"),
        gr.Dropdown(label="Model Name", choices=allowed_models, value=allowed_models[0])
    ],
    title="A system context conversation",
    description="Interact with the agent using a selected model and system context."
)

# Start the Gradio interface
interface.launch()