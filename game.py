from pet_system.pet_data import Pet
from display import display_pet, display_message, console, COLORS
from git_tracker import is_git_repo, get_commit_info, hours_since_last_commit
import time
import os

class Game:
    """Main game controller"""
    
    def __init__(self):
        if is_git_repo():
            repo_name = os.path.basename(os.getcwd())
            console.print(f"[dim]Tracking commits in: {repo_name}[/]")
            
            commit_info = get_commit_info()
            if commit_info:
                console.print(f"[dim]Last commit: {commit_info['message']} ({commit_info['time_ago']})[/]\n")
        else:
            console.print(f"[{COLORS['warning']}]⚠️  Not a git repo! Pet won't decay.[/]\n")
            
        # Create or load pet
        owner_name = self.get_owner_name()
        self.pet = Pet(owner_name=owner_name, pet_name="Buddy")
        self.running = True
    
    def get_owner_name(self):
        """Get player's name at start"""
        console.clear()
        console.print(f"[bold {COLORS['primary']}]╔═══ WELCOME TO MEMORY PET ═══╗[/]")
        console.print("\n[cyan]Your pet's memory depends on your git commits![/]")
        name = console.input(f"\n[{COLORS['secondary']}]What's your name?[/] ").strip()
        return name if name else "Friend"
    
    def handle_command(self, command):
        """Process user commands and update pet state"""
        
        if command == "quit" or command == "exit":
            self.running = False
            display_message("👋 Goodbye! Don't forget to commit to keep your pet's memory alive!", COLORS['warning'])
            return
        
        elif command == "feed":
            # Feeding increases happiness and health
            self.pet.stats['happiness'] = min(100, self.pet.stats['happiness'] + 15)
            self.pet.stats['health'] = min(100, self.pet.stats['health'] + 10)
            self.pet.stats['hunger'] = max(0, self.pet.stats['hunger'] - 20)
            self.pet.pet_memory['interaction_count'] += 1
            
            # Pet remembers you slightly better when you interact
            self.pet.pet_memory['name_clarity'] = min(100, self.pet.pet_memory['name_clarity'] + 2)
            self.pet.pet_memory['bond_level'] = min(100, self.pet.pet_memory['bond_level'] + 3)
            
            display_message(f"🍖 {self.pet.pet_name} is eating... nom nom! Health restored!", COLORS['success'])
            time.sleep(1.5)
        
        elif command == "play":
            # Playing increases happiness and bond
            self.pet.stats['happiness'] = min(100, self.pet.stats['happiness'] + 20)
            self.pet.pet_memory['bond_level'] = min(100, self.pet.pet_memory['bond_level'] + 5)
            self.pet.pet_memory['interaction_count'] += 1
            
            # Small memory boost
            self.pet.pet_memory['name_clarity'] = min(100, self.pet.pet_memory['name_clarity'] + 3)
            
            display_message(f"🎾 {self.pet.pet_name} is playing! So much fun!", COLORS['success'])
            time.sleep(1.5)
        
        elif command == "dance":
            # Dance is a learned trick
            if 'dance' not in self.pet.pet_memory['learned_tricks']:
                self.pet.pet_memory['learned_tricks'].append('dance')
                display_message(f"✨ {self.pet.pet_name} learned to dance!", COLORS['info'])
            else:
                display_message(f"💃 {self.pet.pet_name} dances gracefully!", COLORS['success'])
            
            self.pet.stats['happiness'] = min(100, self.pet.stats['happiness'] + 10)
            self.pet.pet_memory['bond_level'] = min(100, self.pet.pet_memory['bond_level'] + 4)
            self.pet.pet_memory['interaction_count'] += 1
            time.sleep(1.5)
        
        elif command == "sit":
            if 'sit' not in self.pet.pet_memory['learned_tricks']:
                self.pet.pet_memory['learned_tricks'].append('sit')
                display_message(f"✨ {self.pet.pet_name} learned to sit!", COLORS['info'])
            else:
                display_message(f"🪑 {self.pet.pet_name} sits down obediently!", COLORS['success'])
            
            self.pet.pet_memory['interaction_count'] += 1
            time.sleep(1.5)
        
        elif command == "sing":
            if 'sing' not in self.pet.pet_memory['learned_tricks']:
                self.pet.pet_memory['learned_tricks'].append('sing')
                display_message(f"✨ {self.pet.pet_name} learned to sing!", COLORS['info'])
            else:
                display_message(f"🎵 {self.pet.pet_name} sings a beautiful song! ♪♫", COLORS['success'])
            
            self.pet.stats['happiness'] = min(100, self.pet.stats['happiness'] + 15)
            self.pet.pet_memory['interaction_count'] += 1
            time.sleep(1.5)
        
        elif command == "status":
            # Show detailed status
            tricks = ", ".join(self.pet.pet_memory['learned_tricks']) if self.pet.pet_memory['learned_tricks'] else "None yet"
            display_message(
                f"📊 Interactions: {self.pet.pet_memory['interaction_count']} | Tricks known: {tricks}",
                COLORS['info']
            )
            time.sleep(2)
        
        elif command == "decay":
            # Manual decay for testing (remove in final version)
            display_message("⏱️  Simulating 10 hours of memory decay...", COLORS['warning'])
            self.pet.decay_memory(hours_passed=10)
            time.sleep(1)
        
        else:
            display_message("❓ Unknown command! Try: feed, play, dance, sit, sing, status, quit", COLORS['danger'])
            time.sleep(1)
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Display current state
            display_pet(self.pet)
            
            # Show available commands
            console.print(f"\n[bold {COLORS['primary']}]━━━ Actions ━━━[/]")
            console.print(f"[{COLORS['secondary']}]feed[/] | [{COLORS['secondary']}]play[/] | [{COLORS['secondary']}]dance[/] | [{COLORS['secondary']}]sit[/] | [{COLORS['secondary']}]sing[/] | [{COLORS['info']}]status[/] | [{COLORS['danger']}]quit[/]")
            
            # Get user input
            command = console.input(f"\n[bold {COLORS['secondary']}]>[/] ").strip().lower()
            
            # Handle the command
            self.handle_command(command)

# Main entry point
if __name__ == "__main__":
    game = Game()
    game.run()
