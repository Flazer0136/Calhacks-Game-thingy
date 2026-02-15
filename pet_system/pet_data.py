import time

class Pet:
    """Pet's Brain 🥹"""
    
    def __init__(self, owner_name="Friend", pet_name="Buddy"):
        self.pet_name = pet_name
        self.creation_time = time.time()

        self.pet_memory = {
            "owner_name": owner_name,
            "name_clarity": 100,            
            "bond_level": 100,              
            "learned_tricks": [],           
            "interaction_count": 0          
        }
        
        # Pet's health stats
        self.stats = {
            "health": 100,
            "happiness": 100,
            "hunger": 0,
            "age_hours": 0
        }
        
        # Time tracking for decay
        self.last_interaction = time.time()
        self.last_commit = time.time()
        
        # YOUR memory of pet (file integrity)
        self.player_memory = {
            "file_corruption": 0,    # 0-100
            "history_intact": True,  # Command history
            "art_quality": 100       # ASCII art clarity
        }
    
    def get_display_name(self):
        """What the pet calls you (degrades with memory loss)"""
        clarity = self.pet_memory["name_clarity"]
        owner = self.pet_memory["owner_name"]
        
        if clarity > 70:
            return owner
        elif clarity > 40:
            # Partial corruption
            corrupted = ""
            for i, char in enumerate(owner):
                if i % 2 == 0:
                    corrupted += "?"
                else:
                    corrupted += char
            return corrupted
        elif clarity > 10:
            return "stranger"
        else:
            return "???"
    
    def decay_memory(self, hours_passed):
        """Memory loss over time :/ sad person"""
        # Pet forgets you
        self.pet_memory["name_clarity"] -= hours_passed * 5
        self.pet_memory["bond_level"] -= hours_passed * 3
        
        # Your files corrupt
        self.player_memory["file_corruption"] += hours_passed * 4
        
        # Clamp values
        self.pet_memory["name_clarity"] = max(0, self.pet_memory["name_clarity"])
        self.pet_memory["bond_level"] = max(0, self.pet_memory["bond_level"])
        self.player_memory["file_corruption"] = min(100, self.player_memory["file_corruption"])
