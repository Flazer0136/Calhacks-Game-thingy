from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.markup import escape
import random

console = Console()

# Color scheme (inspired by Lip Gloss style)
COLORS = {
    "primary": "bright_magenta",
    "secondary": "bright_cyan", 
    "success": "bright_green",
    "warning": "bright_yellow",
    "danger": "bright_red",
    "info": "bright_blue"
}

# Base ASCII art (your teammate will improve these)
PET_ART = {
    "happy": """
   /\\_/\\  
  ( ^.^ ) 
   > ^ <
   """,
    "neutral": """
   /\\_/\\  
  ( -.- ) 
   > ~ <
   """,
    "sad": """
   /\\_/\\  
  ( ;_; ) 
   > . <
   """,
    "forgotten": """
   / _ \\  
  (  ?  ) 
   >   <
   """
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

def create_progress_bar(value, max_value=100, color="bright_cyan"):
    """Create a visual progress bar"""
    filled = int((value / max_value) * 10)
    empty = 10 - filled
    bar = "█" * filled + "░" * empty
    return f"[{color}]{bar}[/{color}] {int(value)}%"

def get_pet_art(pet):
    """Get ASCII art based on pet's bond level"""
    bond = pet.pet_memory["bond_level"]
    art_quality = pet.player_memory.get("art_quality", 100)
    
    # Choose art based on bond
    if bond > 70:
        art = PET_ART["happy"]
    elif bond > 40:
        art = PET_ART["neutral"]
    elif bond > 10:
        art = PET_ART["sad"]
    else:
        art = PET_ART["forgotten"]
    
    # Corrupt the art based on YOUR memory loss
    corruption = pet.player_memory["file_corruption"]
    if corruption > 30:
        art = corrupt_text(art, corruption)
    
    return art

def display_pet(pet):
    """Enhanced colorful display"""
    console.clear()
    
    # Create layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )
    
    # Split main into pet area and stats
    layout["main"].split_row(
        Layout(name="pet", ratio=2),
        Layout(name="stats", ratio=1)
    )
    
    # Colorful header
    corruption = pet.player_memory["file_corruption"]
    if corruption > 50:
        title = corrupt_text("╔═══ MEMORY PET ═══╗", corruption)
        title_color = COLORS["danger"]
    else:
        title = "╔═══ MEMORY PET ═══╗"
        title_color = COLORS["primary"]
    
    layout["header"].update(
        Panel(
            Text(title, style=f"bold {title_color}", justify="center"),
            style=f"bold {title_color}"
        )
    )
    
    # Pet display with greeting
    art = escape(get_pet_art(pet))
    safe_pet_name = escape(pet.pet_name)
    safe_display_name = escape(pet.get_display_name())
    greeting = f"\n[{COLORS['info']}]🦆 {safe_pet_name} greets:[/] [{COLORS['secondary']}]'{safe_display_name}'[/]"
    
    layout["pet"].update(
        Panel(
            art + greeting,
            title=f"[{COLORS['primary']}]Your Pet[/]",
            border_style=COLORS["primary"]
        )
    )
    
    # Stats with progress bars
    health_color = COLORS["success"] if pet.stats['health'] > 50 else COLORS["danger"]
    bond_color = COLORS["success"] if pet.pet_memory['bond_level'] > 50 else COLORS["warning"]
    memory_color = COLORS["success"] if pet.pet_memory['name_clarity'] > 50 else COLORS["danger"]
    
    stats_text = f"""
😊 [bold]Happiness[/]
{create_progress_bar(pet.stats['happiness'], color=health_color)}

💝 [bold]Bond Level[/]
{create_progress_bar(pet.pet_memory['bond_level'], color=bond_color)}

🧠 [bold]Memory Clarity[/]
{create_progress_bar(pet.pet_memory['name_clarity'], color=memory_color)}

📁 [bold]File Integrity[/]
{create_progress_bar(100 - pet.player_memory['file_corruption'], color="bright_blue")}
    """
    
    # if corruption > 60:
    #     stats_text = corrupt_text(stats_text, corruption)
    
    layout["stats"].update(
        Panel(
            stats_text,
            title=f"[{COLORS['secondary']}]Status[/]",
            border_style=COLORS["secondary"]
        )
    )
    
    console.print(layout)

def display_message(message, style="white"):
    """Show a message to the player"""
    console.print(f"\n[{style}]{message}[/{style}]")

def get_command():
    """Get user input with nice formatting"""
    console.print(f"\n[bold {COLORS['primary']}]Commands:[/] feed | play | status | quit")
    return console.input(f"[bold {COLORS['secondary']}]>[/] ").strip().lower()
