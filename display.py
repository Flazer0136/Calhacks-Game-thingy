import time
import random
import re
from rich.console import Console, Group
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box
from menu_system import MenuState
from rich.rule import Rule
import os


console = Console(force_terminal=True)


THEME = {
    "bg": "#1a1b26",           
    "border": "#7aa2f7",       
    "divider": "#414868",      
    "tab_active": "#f7768e",   
    "tab_inactive": "#414868",
    "primary": "#7aa2f7",      
    "secondary": "#bb9af7", 
    "text_active": "#1a1b26",  
    "text_normal": "#a9b1d6",  
    "highlight": "#bb9af7",    
    "success": "#9ece6a",      
    "warning": "#e0af68",
    "danger": "#f7768e"
}


def load_sprite_frames(filename):
    """
    Load sprite frames from a text file.
    If file has multiple frames, they're separated by blank lines.
    Returns list of frames.
    """
    try:
        path = f"pet_sprites/{filename}"
        
        # Opens with utf-8, fallback to system default if it fails
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, 'r') as f:
                content = f.read()
        
        if "===" in content:
            frames = content.split("===")
        else:
            frames = re.split(r'\n{3,}', content)

        frames = [frame.strip('\n') for frame in frames if frame.strip()]
        
        return frames if frames else ["???"]
        
    except FileNotFoundError:
        return ["???"]
    except Exception as e:
        return [f"Error: {str(e)}"]


PET_SPRITES = {
    "happy": load_sprite_frames("happy.txt"),
    "normal": load_sprite_frames("normal.txt"),
    "sadness": load_sprite_frames("sadness.txt"),
    "fear": load_sprite_frames("fear.txt"),
    "anger": load_sprite_frames("anger.txt"),
    "regular": load_sprite_frames("regular.txt"),
    "dance": load_sprite_frames("dance.txt"),
    "sit": load_sprite_frames("sit.txt"),
    "sing": load_sprite_frames("happy.txt"), 
    "feed": load_sprite_frames("happy.txt"),  
    "play": load_sprite_frames("happy.txt"),
}


def corrupt_text(text, corruption_level):
    """Corrupt text based on corruption level (0-100)"""
    if corruption_level < 20:
        return text
    
    corrupted = ""
    for char in text:
        if char == ' ' or char == '\n':
            corrupted += char
        elif random.random() < (corruption_level / 200):
            corrupted += random.choice(['?', '█', '▓', '░', '*', '#'])
        else:
            corrupted += char
    return corrupted


def get_pet_art(pet, frame_index=0, current_action=None):
    """Get sprite based on pet state or current action."""
    
    if current_action:
        action_key = current_action.lower()
        frames = PET_SPRITES.get(action_key, PET_SPRITES.get("normal"))
        if not frames: frames = ["???"]
        frame = frames[frame_index % len(frames)]
        return frame
    
    bond = pet.pet_memory["bond_level"]
    corruption = pet.player_memory["file_corruption"]
    
    try:
        bond = int(bond)
        corruption = int(corruption)
    except ValueError:
        return "ERROR: Stats are not numbers"

    if corruption > 50 and corruption < 80:
        frames = PET_SPRITES.get("fear", ["???"])
    elif corruption >= 80:
        frames = PET_SPRITES.get("anger", ["???"])
    elif bond > 70:
        frames = PET_SPRITES.get("happy", ["???"])
    elif bond > 40:
        frames = PET_SPRITES.get("normal", ["???"])
    else:
        frames = PET_SPRITES.get("sadness", ["???"])
    
    if not frames: frames = ["???"]
    frame = frames[frame_index % len(frames)]
    
    # ✨ RANDOM INTERMITTENT GLITCH
    if corruption > 50:
        # Higher corruption = higher chance of glitch
        glitch_probability = (corruption - 50) / 150  # 0% at 50, 33% at 100
        
        if random.random() < glitch_probability:
            frame = corrupt_text(frame, corruption)
    
    return frame




# Simple stat bar 
def create_stat_bar(value: int, width: int = 15, filled: str = "█", empty: str = "░") -> str:
    """Create a visual stat bar."""
    value = max(0, min(100, int(value)))
    filled_count = int(value / 100 * width)
    empty_count = width - filled_count
    return f"{filled * filled_count}{empty * empty_count}"


# Horizontal stat bars
def create_stats_panel(pet):
    """Create Happy Index panel with horizontal bars"""
    stats_grid = Table.grid(expand=True, padding=(1, 2))
    stats_grid.add_column(width=12, justify="left")  # Emoji + Label
    stats_grid.add_column(ratio=1)                    # Bar
    stats_grid.add_column(width=5, justify="right")   # Percentage
    
    def create_bar_row(emoji, label, value, color):
        value = max(0, min(100, int(value)))
        bar_str = create_stat_bar(value, width=15)
        
        label_text = Text(f"{emoji} {label}", style="bold white")
        bar_text = Text(bar_str, style=color)
        percent_text = Text(f"{value}%", style="dim white")
        
        return (label_text, bar_text, percent_text)
    
    stats_grid.add_row(*create_bar_row("😊", "Happy", pet.stats['happiness'], THEME['success']))
    stats_grid.add_row(*create_bar_row("💝", "Bond", pet.pet_memory['bond_level'], THEME['warning']))
    stats_grid.add_row(*create_bar_row("🧠", "Memory", pet.pet_memory['name_clarity'], THEME['primary']))
    stats_grid.add_row(*create_bar_row("💾", "Backup", 100 - pet.player_memory['file_corruption'], THEME['danger']))
    
    return stats_grid


def create_git_panel(git_info):
    """Create Git Index panel showing commit graph + info"""
    git_table = Table.grid(expand=True, padding=(0, 1))
    git_table.add_column(justify="left")
    
    # GRAPH FIRST (if available) - YELLOW/GOLD THEME
    if git_info.get('graph'):
        git_table.add_row(Text("📈 Commit Graph", style=f"bold {THEME['warning']}"))  # Yellow title
        git_table.add_row(Text(""))
        
        # Colorize the graph
        graph_lines = git_info['graph'].split('\n')
        for line in graph_lines:
            colored_line = Text()
            for char in line:
                if char in ['*', '|', '/', '\\']:
                    # Graph symbols in yellow
                    colored_line.append(char, style=THEME['warning'])
                elif char in ['─', '│']:
                    colored_line.append(char, style=THEME['divider'])
                else:
                    # Commit messages in white
                    colored_line.append(char, style="white")
            git_table.add_row(colored_line)
        
        git_table.add_row(Text(""))
        git_table.add_row(Text("─" * 30, style=THEME['divider']))
        git_table.add_row(Text(""))
    
    # THEN COMMIT INFO
    git_table.add_row(Text(f"📊 Last Commit", style=f"bold {THEME['highlight']}"))
    git_table.add_row(Text(f"   {git_info.get('message', 'N/A')[:40]}", style="white"))
    git_table.add_row(Text(""))
    
    git_table.add_row(Text(f"👤 {git_info.get('author', 'N/A')}", style="dim white"))
    git_table.add_row(Text(f"⏰ {git_info.get('time_ago', 'N/A')}", style=THEME['warning']))
    git_table.add_row(Text(f"📝 {git_info.get('total', 0)} commits", style=THEME['success']))
    
    return git_table



def create_git_graph_panel(graph_text):
    """Create Git Graph panel showing commit tree"""
    git_table = Table.grid(expand=True, padding=(1, 1))
    git_table.add_column(justify="left")
    
    git_table.add_row(Text("📈 Commit History", style=f"bold {THEME['secondary']}"))
    git_table.add_row(Text(""))
    
    if graph_text:
        git_table.add_row(Text(graph_text, style="white"))
    else:
        git_table.add_row(Text("No git repository found", style="dim red"))
    
    return git_table



# Helper to create dividers
def create_horizontal_divider():
    """Create a full-width horizontal divider line"""
    return Rule(style=THEME['divider'])


def create_game_layout(pet, menu, current_message="", frame_index=0, current_action=None, view_mode="stats", git_info=None):
    """✨ UPDATED: Single box layout with internal dividers"""
    
    # === TOP SECTION: Pet (left) | Stats (right) ===
    top_section = Table.grid(expand=True, padding=(1, 1))
    top_section.add_column(ratio=1)   # Pet side
    top_section.add_column(width=1)   # Vertical divider
    top_section.add_column(ratio=1)   # Stats side
    
    # Left: Pet Art + Message
    art_str = get_pet_art(pet, frame_index, current_action)
    pet_content = Group(
        Text(""),
        Align.center(Text(art_str, style="bold white", justify="center")),
        Text(""),
        Align.center(Text(current_message if current_message else "", 
                         style=f"bold {THEME['highlight']}", 
                         justify="center"))
    )
    
    # Right: Stats or Git Info
    if view_mode in ["git", "git_graph"] and git_info:
        info_content = Group(
            Align.center(Text("Git Index", style=f"bold {THEME['secondary']}")),
            Text(""),
            create_git_panel(git_info)
        )

    elif view_mode == "git_graph" and git_info:
        info_content = Group(
            Align.center(Text("Git Graph", style=f"bold {THEME['secondary']}")),
            Text(""),
            create_git_graph_panel(git_info.get('graph', 'No commits'))
        )
    else:
        info_content = Group(
            Align.center(Text("Happy Index", style=f"bold {THEME['success']}")),
            Text(""),
            create_stats_panel(pet)
    )
    
    # Vertical divider
    vertical_divider = Text("│\n" * 26, style=THEME['divider'])
    
    top_section.add_row(pet_content, vertical_divider, info_content)
    
    # === HORIZONTAL DIVIDER ===
    h_divider = create_horizontal_divider()
    
    # === BOTTOM SECTION: Menu ===
    bottom_section = Table.grid(expand=True, padding=(1, 1))
    bottom_section.add_column(width=20)  
    bottom_section.add_column(width=1)  
     
    bottom_section.add_column(ratio=1)   
    
    # Sidebar
    sidebar_content = Table.grid(padding=(1, 1))
    for i, item in enumerate(menu.main_items):
        is_selected = (menu.state == MenuState.MAIN and i == menu.selected_index)
        
        if is_selected:
            label = Text(f" {item.label.upper()} ", style=f"bold {THEME['text_active']} on {THEME['tab_active']}")
            indicator = Text("● ", style=THEME['tab_active'])
        else:
            label = Text(f" {item.label.upper()} ", style=f"{THEME['text_normal']}")
            indicator = Text("  ")
        
        sidebar_content.add_row(indicator + label)
    
    # Content Panel
    show_actions = menu.state == MenuState.ACTIONS or (
        menu.state == MenuState.MAIN and 
        menu.main_items[menu.selected_index].label == "Actions"
    )
    
    show_settings = menu.state == MenuState.SETTINGS or (
        menu.state == MenuState.MAIN and 
        menu.main_items[menu.selected_index].label == "Settings"
    )
    
    if show_actions:
        action_table = Table.grid(padding=(0, 2))
        for i, item in enumerate(menu.action_items):
            if menu.state == MenuState.ACTIONS and i == menu.selected_index:
                style = f"bold {THEME['highlight']}"
                prefix = ">"
            else:
                style = "dim white"
                prefix = " "
            action_table.add_row(Text(f"{prefix} {item.label}", style=style))
        content_panel_inner = action_table
    
    elif show_settings:
        settings_table = Table.grid(padding=(0, 2))
        for i, item in enumerate(menu.settings_items):
            if menu.state == MenuState.SETTINGS and i == menu.selected_index:
                style = f"bold {THEME['highlight']}"
                prefix = ">"
            else:
                style = "dim white"
                prefix = " "
            settings_table.add_row(Text(f"{prefix} {item.label}", style=style))
        content_panel_inner = settings_table
        
    elif menu.main_items[menu.selected_index].label == "Exit":
        content_panel_inner = Align.center(
            Text("Are you sure you want to leave?\nYour pet will miss you.", style="dim"),
            vertical="middle"
        )
    else:
        content_panel_inner = Text("")
    
    # Vertical divider for menu
    menu_vertical_divider = Text("│\n" * 12, style=THEME['divider'])
    
    bottom_section.add_row(sidebar_content, menu_vertical_divider, content_panel_inner)
    
    # === COMBINE ALL SECTIONS ===

    final_layout = Group(
        top_section,
        h_divider,
        bottom_section
    )

    return Panel(
        final_layout,
        title=f"[{THEME['primary']}] DevGotchi[/]",
        border_style=THEME["border"],
        box=box.ROUNDED,
        padding=(1, 2)
    )
