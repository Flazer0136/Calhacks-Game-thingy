import os

SPRITE_CACHE = {}

def load_sprites(sprite_folder="pet_sprites"):
    """Loads all .txt files from the folder and splits them by '==='"""
    global SPRITE_CACHE
    
    # Ensure the folder exists
    if not os.path.exists(sprite_folder):
        os.makedirs(sprite_folder)
        print(f"Created {sprite_folder}. Please put your .txt files there!")
        return

    # List of expected files
    anim_names = ["dance", "fear", "happy", "regular", "sadness", "sit", "anger"]

    for name in anim_names:
        filepath = os.path.join(sprite_folder, f"{name}.txt")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Split by the separator
                frames = content.split("===")
                # cleans lines for new frame
                SPRITE_CACHE[name] = [f.strip("\n") for f in frames]
        except FileNotFoundError:
            # Fallback if file is missing
            SPRITE_CACHE[name] = [f"(Missing {name}.txt)"]