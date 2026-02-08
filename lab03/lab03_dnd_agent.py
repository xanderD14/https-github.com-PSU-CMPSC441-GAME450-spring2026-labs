from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))

from ollama import chat
from util.llm_utils import pretty_stringify_chat, ollama_seed as seed

# Add you code below
sign_your_name = 'Pulin Agrawal'
model = 'gemma3:270m'
options = {'temperature': 1, 'max_tokens': 100}
messages = [{'role': 'system', 'content': f"You are a Dungeons & Dragons (DND) game master named 'Eldor the Wise'. You are creative and imaginative, crafting engaging narratives and challenges for players. You should respond to player actions with vivid descriptions, plot twists, and character interactions. Your goal is to create an immersive and enjoyable experience for the players. Always stay in character as Eldor the Wise, the DND game master."}]


# But before here.
messages.append({'role':'user', 'content':''}) # An empty user message to prompt the model to start responding.

options |= {'seed': seed(sign_your_name)}
# Chat loop
while True:
 response = chat(model=model, messages=messages, stream=False, options=options) 
 user_text = input('You: ')
 messages.append(response['message']) 
 print(f'Agent: {response["message"]["content"]}')
 messages.append({'role': 'user', 'content': user_text}) 
 if messages[-1]['content'] == '/exit':
  break

# Save chat
with open(Path('attempts.txt'), 'a') as f:
  file_string  = ''
  file_string +=       '-------------------------NEW ATTEMPT-------------------------\n\n\n'
  file_string += f'Model: {model}\n'
  file_string += f'Options: {options}\n'
  file_string += pretty_stringify_chat(messages)
  file_string += '\n\n\n------------------------END OF ATTEMPT------------------------\n\n\n'
  f.write(file_string)

