from enum import Enum
import sys
import tty
import termios

class MenuState(Enum):
    MAIN = "main"
    ACTIONS = "actions"

class MenuItem:
    def __init__(self, label, action=None, submenu=None):
        self.label = label
        self.action = action
        self.submenu = submenu

class Menu:
    def __init__(self):
        self.state = MenuState.MAIN
        self.selected_index = 0
        
        # Main Menu
        self.main_items = [
            MenuItem("Actions", submenu="actions"),
            MenuItem("Exit", action="quit")
        ]
        
        # Actions Tab
        self.action_items = [
            MenuItem("Dance", action="dance"),
            MenuItem("Sit", action="sit"),
            MenuItem("Sing", action="sing"),
            MenuItem("Feed", action="feed"),
            MenuItem("Play", action="play"),
            # We don't need "Back" anymore if we have Left Arrow support!
        ]
    
    def get_current_items(self):
        if self.state == MenuState.MAIN:
            return self.main_items
        elif self.state == MenuState.ACTIONS:
            return self.action_items
        return []
    
    def navigate_up(self):
        items = self.get_current_items()
        self.selected_index = (self.selected_index - 1) % len(items)
    
    def navigate_down(self):
        items = self.get_current_items()
        self.selected_index = (self.selected_index + 1) % len(items)

    # --- NEW: TAB NAVIGATION ---
    def navigate_right(self):
        """Enter the tab if the selected item has a submenu"""
        items = self.get_current_items()
        selected = items[self.selected_index]
        
        if selected.submenu == "actions":
            self.state = MenuState.ACTIONS
            self.selected_index = 0 # Start at top of action list

    def navigate_left(self):
        """Go back to the sidebar"""
        if self.state == MenuState.ACTIONS:
            self.state = MenuState.MAIN
            self.selected_index = 0 # Highlight 'Actions' again

    def select(self):
        """Handle Enter key"""
        items = self.get_current_items()
        selected = items[self.selected_index]
        
        # Also allow Enter to open tabs (just like Right Arrow)
        if selected.submenu == "actions":
            self.state = MenuState.ACTIONS
            self.selected_index = 0
            return None
        elif selected.action == "back":
            self.state = MenuState.MAIN
            self.selected_index = 0
            return None
        else:
            return selected.action

    # ... (Keep get_key function and is_actions_open unchanged) ...
    def is_actions_open(self):
        return self.state == MenuState.ACTIONS

# (Keep your existing get_key function down here)
def get_key():
    # ... paste your existing get_key code here ...
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A': return 'UP'
                elif ch3 == 'B': return 'DOWN'
                elif ch3 == 'C': return 'RIGHT'
                elif ch3 == 'D': return 'LEFT'
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)