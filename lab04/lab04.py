from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parents[1]))

from util.llm_utils import AgentTemplate

# Add code here
NPC_TEMPLATE = 'lab04/npc.json'
ENEMY_TEMPLATE = 'lab04/enemy.json'
DM_TEMPLATE = 'lab04/dm.json'

encounter_templates = {
    'npc': ('lab04/npc.json', 'Jimmy (NPC)'),
    'enemy': ('lab04/enemy.json', 'Ryan (Enemy)'),
}

def start_npc_chat():
    '''Start a chat with an NPC agent.'''
    run_console_chat(NPC_TEMPLATE, agent_name='Jimmy (NPC)')

def start_enemy_chat():
    '''Start a chat with an enemy agent.'''
    run_console_chat(ENEMY_TEMPLATE, agent_name='Ryan (Enemy)')
# But before here.

def run_console_chat(template_file, agent_name='Agent', **kwargs):
    '''
    Run a console chat with the given template file and agent name.
    Args:
        template_file: The path to the template file.
        agent_name: The name of the agent to display in the console.
        **kwargs: Additional arguments to pass to the AgentTemplate.from_file method.
    '''
    chat = AgentTemplate.from_file(template_file, **kwargs)
    response = chat.start_chat()
    while True:
        print(f'{agent_name}: {response}')
        try:
            user_input = input('You: ')
            response = chat.send(user_input)
            # Add code here to check which agent chat should be started
            for key, (template, name) in encounter_templates.items():
                if key in response.lower():
                    print(f'\n--- Entering {name} encounter ---\n')
                    run_console_chat(template_file=template, agent_name=name)
                    print(f'\n--- {name} encounter ended ---\n')
                    break
            # But before here.
        except StopIteration as e:
            break

if __name__ == '__main__':
    # Add code here to start DM chat
    encounters = ', '.join(name for _, (_, name) in encounter_templates.items())
    run_console_chat(template_file=DM_TEMPLATE, agent_name='Dungeon Master', encounters=encounters)
    # But before here.
    pass