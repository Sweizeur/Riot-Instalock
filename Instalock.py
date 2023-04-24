import json
import keyboard
import os
import pyautogui
import time


class Agent:
    def __init__(self, name, position, shortcut=None):
        self.name = name
        self.position = position
        self.shortcut = shortcut


class AgentManager:
    def __init__(self):
        self.agents = []
        self.lock_position = None
        self.file = "config.json"
        self.lock_shortcut = "ctrl+maj+l"
        self.blocked_keys = ["ctrl+maj+q", "ctrl+maj+m", self.lock_shortcut]

    def create_agent(self):
        print(f'\n{"Create_Agent":-^70}')
        name = input("Enter the name of the agent: ")
        print(f'Please press {self.lock_shortcut} to create the lock (or press enter to cancel)')
        position = self.get_mouse_position()
        if not position:
            return
        shortcut = self.get_agent_shortcut()
        self.agents.append(Agent(name, position, shortcut))
        self.save_agents()
        print("Agent created successfully")
        print(f'{"Create_Agent":-^70}\n')

    def get_mouse_position(self):
        while True:
            if keyboard.is_pressed(self.lock_shortcut):
                return pyautogui.position()
            if keyboard.is_pressed("esc"):
                return None

    def get_agent_shortcut(self, name="the agent"):
        time.sleep(0.5)
        while True:
            shortcut = input(f"Enter the shortcut for {name} (or press enter to skip) >> ")
            if not shortcut:
                return None
            elif shortcut.lower() in self.blocked_keys:
                print("This shortcut is not allowed")
            else:
                return shortcut.lower()

    def create_lock(self):
        print(f'\n{"Create_Lock":-^70}')
        print(f"Please press {self.lock_shortcut} to create the lock (or press enter to cancel)")
        lock_position = self.get_mouse_position()
        if not lock_position:
            return
        self.lock_position = lock_position
        self.save_agents()
        print("Lock created successfully")
        print(f'{"Create_Lock":-^70}\n')

    def delete_agent(self):
        print(f'\n{"Delete_Agent":-^70}')
        self.print_agents()
        name = input("Enter the name of the agent you want to delete (or enter 'all' to delete all agents or press enter to cancel) >> ")
        if not name:
            return
        for agent in self.agents:
            if name == "all":
                self.agents = []
                self.save_agents()
                print("All agents deleted successfully")
                print(f'{"Delete_Agent":-^70}\n')
                return
            if agent.name == name:
                self.agents.remove(agent)
                self.save_agents()
                print(f"Agent {name} deleted successfully")
                print(f'{"Delete_Agent":-^70}\n')
                return
        print(f"Could not find agent {name}")
        print(f'{"Delete_Agent":-^70}\n')

    def modify_agent(self):
        print(f'\n{"Modify_Agent":-^70}')
        self.print_agents()
        name = input("Enter the name of the agent you want to modify >> ")
        for agent in self.agents:
            if agent.name == name:
                new_name = input(f"Enter the new name for {name} (or press enter to keep the same name) >> ")
                shortcut = self.get_agent_shortcut(name)
                if new_name:
                    agent.name = new_name
                if shortcut is not None:
                    agent.shortcut = shortcut
                print(f"Please press {self.lock_shortcut} to modify the location (or press enter to keep the same location)")
                position = self.get_mouse_position()
                if position:
                    agent.position = position
                self.save_agents()
                print("Agent modified successfully")
                print(f'{"Modify_Agent":-^70}\n')
                return
        print(f"Could not find agent {name}")
        print(f'{"Modify_Agent":-^70}\n')

    def print_agents(self):
        print(f'\n{"List Agents":-^70}')
        print("Agents:\n")
        for agent in self.agents:
            print(f"- {agent.name}")
        print(f'{"List Agents":-^70}\n')

    def load_agents(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
                self.agents = [Agent(**agent) for agent in data.get("agents", [])]
                self.lock_position = tuple(data.get("lock", None) or ())
        else:
            self.save_agents()

    def save_agents(self):
        data = {
            "agents": [{"name": agent.name, "position": agent.position, "shortcut": agent.shortcut} for agent in self.agents],
            "lock": self.lock_position
        }
        with open(self.file, "w") as f:
            json.dump(data, f)

    def run(self):
        time.sleep(0.5)
        self.load_agents()
        while True:
            print(f'\n{"Menu":-^70}')
            print("1. Create agent")
            print("2. Create lock")
            print("3. List agents")
            print("4. Delete agent")
            print("5. Modify agent")
            print("Enter. Exit")
            print(f'{"Menu":-^70}\n')
            choice = input("\nEnter your choice >> ")
            if choice == "1":
                self.create_agent()
            elif choice == "2":
                self.create_lock()
            elif choice == "3":
                self.print_agents()
            elif choice == "4":
                self.delete_agent()
            elif choice == "5":
                self.modify_agent()
            elif choice == "":
                print(f'\n{"Instalock":-^70}')
                print("Instalock started (press Ctrl+Maj+Q to stop)")
                print(f'{"Instalock":-^70}\n')
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    agent_manager = AgentManager()
    agent_manager.run()

    while True:
        for agent in agent_manager.agents:
            if agent.shortcut and keyboard.is_pressed(agent.shortcut):
                pyautogui.click(agent.position)
                pyautogui.click(agent_manager.lock_position)
                break
        if keyboard.is_pressed("ctrl+maj+q"):
            break