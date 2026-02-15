import time
import random
from rich.console import Console, Group  # <--- Added Group import
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box
from menu_system import MenuState

console = Console()

# --- THEME: "LIP GLOSS" (Deep Purple/Pink) ---
THEME = {
    "bg": "#1a1b26",           
    "border": "#7aa2f7",       
    "tab_active": "#f7768e",   
    "tab_inactive": "#414868", 
    "text_active": "#1a1b26",  
    "text_normal": "#a9b1d6",  
    "highlight": "#bb9af7",    
    "success": "#9ece6a",      
    "warning": "#e0af68",
    "danger": "#f7768e"
}

# --- YOUR ORIGINAL ART ---
PET_ART = {
    "happy": [
        """
   /\\_/\\  
  ( ^.^ ) 
   > ^ <
        """,
        """
   /\\_/\\  
  ( ^ω^ ) 
   > ^ <
        """
    ],
    "neutral": [
        """
   /\\_/\\  
  ( -.- ) 
   > ~ <
        """,
        """
   /\\_/\\  
  ( o.o ) 
   > ~ <
        """
    ],
    "sad": [
        """
   /\\_/\\  
  ( ;_; ) 
   > . <
        """,
        """
   /\\_/\\  
  ( T_T ) 
   > . <
        """
    ],
    "forgotten": [
        """
   / _ \\  
  (  ?  ) 
   >   <
        """
    ]
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

def get_pet_art(pet, frame_index=0):
    """Get ASCII art based on pet's bond level + Animation Frame"""
    bond = pet.pet_memory["bond_level"]
    corruption = pet.player_memory["file_corruption"]

    # Choose state
    if corruption > 80:
        frames = PET_ART["forgotten"]
    elif bond > 70:
        frames = PET_ART["happy"]
    elif bond > 40:
        frames = PET_ART["neutral"]
    else:
        frames = PET_ART["sad"]
    
    # Cycle frames
    art = frames[frame_index % len(frames)]
    
    # Apply corruption
    if corruption > 30:
        art = corrupt_text(art, corruption)
    
    return art

def create_game_layout(pet, menu, current_message="", frame_index=0):
    """
    Creates the 'Lip Gloss' style interface
    """
    layout = Layout()
    layout.split_column(
        Layout(name="top", ratio=2),
        Layout(name="bottom", size=10)
    )

    # --- TOP AREA: PET & STATS ---
    # 1. Create the stats table
    stats_table = Table.grid(expand=True, padding=(1, 2))
    stats_table.add_column(justify="center", ratio=1)
    stats_table.add_column(justify="center", ratio=1)
    
    def make_bar(val, color):
        blocks = int(val / 10)
        return f"[{color}]{'█' * blocks}[/][#24283b]{'█' * (10 - blocks)}[/]"

    stats_table.add_row(
        f"HAPPY {make_bar(pet.stats['happiness'], THEME['success'])}",
        f"BOND {make_bar(pet.pet_memory['bond_level'], THEME['warning'])}"
    )

    # 2. Get Art
    art_str = get_pet_art(pet, frame_index)
    
    # 3. Combine Art and Stats into a Group
    # This renders them stacked vertically inside the panel
    art_content = Align.center(
        Text(f"\n{art_str}\n", style="bold white") + 
        Text(f"\n{current_message}\n", style=f"bold {THEME['highlight']}")
    )
    
    # Use Group to stack Art (top) and Stats (bottom)
    main_content = Group(
        art_content,
        Align.center(stats_table)
    )
    
    layout["top"].update(
        Panel(
            main_content,
            border_style=THEME["border"],
            box=box.ROUNDED,
            padding=(1, 2)
        )
    )

    # --- BOTTOM AREA: VERTICAL TABS ---
    bottom_grid = Table.grid(expand=True)
    bottom_grid.add_column(width=20) 
    bottom_grid.add_column(ratio=1)  
    
    # Sidebar
    sidebar_content = Table.grid(padding=(1, 1), expand=True)
    
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
    content_panel = None
    
    show_actions = False
    if menu.state == MenuState.ACTIONS:
        show_actions = True
    elif menu.state == MenuState.MAIN and menu.main_items[menu.selected_index].label == "Actions":
        show_actions = True

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
        content_panel = Panel(action_table, border_style=THEME["tab_inactive"], box=box.MINIMAL)
        
    elif menu.main_items[menu.selected_index].label == "Exit":
        content_panel = Panel(
            Align.center("[dim]Are you sure you want to leave?\nYour pet will miss you.[/]", vertical="middle"),
            border_style=THEME["tab_inactive"],
            box=box.MINIMAL
        )

    bottom_grid.add_row(
        Panel(sidebar_content, border_style=THEME["border"], box=box.ROUNDED),
        content_panel if content_panel else Panel("", box=box.MINIMAL)
    )

    layout["bottom"].update(bottom_grid)
    return layout