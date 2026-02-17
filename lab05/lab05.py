from pathlib import Path
from pdb import run
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import AgentTemplate
encounters = ['npc', 'trader', 'recruit']
def run_console_chat(template_file, agent_name='Agent', **kwargs):
    chat = AgentTemplate.from_file(**kwargs)
    response = chat.start_chat()
    while True:
        print(f'{agent_name}: {response}')
        # if one of the encounrters in message then start that chat
        this_encounter = list(filter(lambda encounter: encounter in response.lower(), encounters))
        if this_encounter:
            encounter = this_encounter[0]
            print(f'Starting {encounter} chat...')
            run_console_chat(template_file=f'lab04/lab04_{encounter}_chat.json', 
                            agent_name=encounter.capitalize(),
                             **kwargs)

        response = chat.send(input('You: '))

lab04_params = {}

if __name__ ==  '__main__':
    # run lab04.py to test your template interactively
    pass