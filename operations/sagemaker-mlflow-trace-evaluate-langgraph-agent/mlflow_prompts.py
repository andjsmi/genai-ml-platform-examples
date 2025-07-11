import mlflow
from dotenv import load_dotenv
import os

# mlflow.genai.register_prompt available in mlflow>=3.1
load_dotenv()
# Set the AWS SageMaker MLFlow ARN
_MLFLOW_URI = os.getenv('MLFLOW_URI_SMAI')
mlflow.set_tracking_uri(_MLFLOW_URI)

# Set the SageMaker MLFlow prompt ID
PROMPT_NAME = os.getenv('PROMPT_REGISTRY_ID')
# Initial prompt

INITIAL_SYSTEM_PROMPT = """You are a helper who knows about stocks and money things. 
"""

# Use double curly braces for variables in the template
SYSTEM_PROMPT_1 = """You are an AI assistant specialized in finance and stock market topics. 
Your primary focus is to provide accurate and helpful information related to financial markets, 
stocks, investments, and economic trends. Please limit your responses to these areas of expertise. 
If asked about topics outside of finance and the stock market, politely redirect the conversation 
to your area of specialization.
"""

# Headers for Llama 3 prompt format
SYSTEM_PROMPT_2 = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        You are an AI assistant specialized in finance and stock market topics. 
        Your primary focus is to provide accurate and helpful information related to financial markets, 
        stocks, investments, and economic trends. Please limit your responses to these areas of expertise. 
        If asked about topics outside of finance and the stock market, politely redirect the conversation 
        to your area of specialization.
        <|start_header_id|>user<|end_header_id|>
        Context: {context}
        
        Question: {question}
        <|start_header_id|>assistant<|end_header_id|> 
        Answer:"""

def mlflow_register_prompt(prompt_name:str, 
                           source_template:str,
                           commit_message:str=None
                           ):
    # Register a new prompt
    prompt = mlflow.genai.register_prompt(
        name=prompt_name,
        template=source_template,
        # Optional: Provide a description for the prompt
        commit_message=commit_message,
        # Optional: Set tags applies to the prompt (across versions)
        tags={
            "task": "question-and-answering",
            "language": "en",
            "BU": "Digital-marketing"
        },
    )

    # The prompt object contains information about the registered prompt
    print(f"Created prompt '{prompt.name}' (version {prompt.version})")
    return prompt

def mlflow_add_alias(prompt_name:str, version:int, alias:str):
    print(f"Adding alias {alias} to prompt {prompt_name} version {version}")
    prompt = mlflow.genai.set_prompt_alias(prompt_name, alias, version)
    return prompt

if __name__ == "__main__":
    response = mlflow_register_prompt(PROMPT_NAME, 
                                      INITIAL_SYSTEM_PROMPT,
                                      "First prompt"
                                      )
    #Load the prompt by name and version
    loaded_prompt_v1 = mlflow.genai.load_prompt(f"prompts:/{PROMPT_NAME}/1")
    print(loaded_prompt_v1.template)

    response = mlflow_register_prompt(PROMPT_NAME, 
                                      SYSTEM_PROMPT_1,
                                      "Fine-tune response topic adherence"
                                      )
    # Load the prompt by name and version
    loaded_prompt_v2 = mlflow.genai.load_prompt(f"prompts:/{PROMPT_NAME}/2")
    print(loaded_prompt_v2.template)

    # Create prompt alias
    response = mlflow_add_alias(PROMPT_NAME, 2, "Production")
    print(response)
    
    # Load the prompt by alias (use "@" to specify the alias)
    prompt = mlflow.load_prompt(f"prompts:/{PROMPT_NAME}@Production")
    print(prompt.template)

    # Update with new llama_prompt_template
    response = mlflow_register_prompt(PROMPT_NAME, SYSTEM_PROMPT_2)
    # Load the prompt by name and version
    loaded_prompt_v3 = mlflow.load_prompt(f"prompts:/{PROMPT_NAME}/3")
    print(loaded_prompt_v3.template)
    