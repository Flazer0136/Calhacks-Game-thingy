# DevGotchi 

DevGotchi is a virtual pet that tracks your git logs to see how consistent you have been. If it notices you slacking off, it'll take damage and slowly start to forget about you.

# Installation and getting started

1. Make sure your device has uv set up for the best experience with the virtual environment.

- [UV Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

2. Clone the repository to the directory where you have a repository that you want to track:

```bash
git clone https://github.com/Flazer0136/DevGotchi.git
```

3. Navigate to the project folder and run the following commands:


- First to install dependencies
```bash
uv sync
```

- to run the app (this also automatically initializes the project)

```bash
uv run game.py
```

# Usage
- Your app should be running in your terminal now, the pet will automatically check the git logs using the sub process that runs along side it. 

- Play and interact with the pet to gain extra health and happiness points.

# Contributers
- Avi pancholi [Github](https://github.com/RobomrFox)
- Sikanderdeep Kingra [Github](https://github.com/Flazer0136)