#!/usr/bin/env python3
"""
Roblox Profile Generator
Generates realistic usernames, passwords, and profile data for Roblox accounts.
"""

import random
import string
from typing import Tuple


class RobloxProfile:
    """Advanced profile generation for Roblox accounts."""
    
    # Username word parts for generation
    WORD_PARTS = [
        "Shadow", "Flame", "Wolf", "Tiger", "Dragon", "Phoenix", "Hunter", "Star", "Ghost",
        "Legend", "Galaxy", "Frost", "Sonic", "Crystal", "Silver", "Dark", "Power", "Magic", "Light",
        "Alpha", "King", "Queen", "Master", "Pro", "Hero", "Knight", "Beast", "Epic", "Ultra",
        "Fire", "Storm", "Blaze", "Ice", "Sky", "Thunder", "Raven", "Fox", "Lion", "Eagle",
        "Night", "Dawn", "Viper", "Blade", "Hawk", "Claw", "Venom", "Echo", "Bane", "Mystic",
        "Cyber", "Nova", "Orbit", "Pixel", "Glitch", "Byte", "Circuit", "Spark", "Neon", "Chase",
        "Rogue", "Stealth", "Fusion", "Prism", "Wraith", "Saber", "Pulse", "Zero", "Fury",
        "Builder", "Ninja", "Gamer", "Lava", "Stream", "Craft", "Miner", "Block", "Code", "Playz",
        "Panda", "Bear", "Slime", "Duck", "Bacon", "Cookie", "Rocket", "Moon", "Starry", "Turbo",
        "Lucky", "Flash", "Arrow", "Ace", "Omega", "Chaos", "Void", "Rift", "Toxic",
        "Golden", "Blizzard", "Inferno", "Vortex", "Zoom", "Aqua", "Primal", "Chill", "Hyper",
    ]
    
    HUMAN_NAMES = [
        "Liam", "Emma", "Noah", "Olivia", "Oliver", "Ava", "Elijah", "Sophia", "Lucas", "Isabella",
        "Mason", "Mia", "Ethan", "Charlotte", "Logan", "Amelia", "Aiden", "Harper", "James", "Evelyn",
        "Jayden", "Abigail", "Henry", "Ella", "Sebastian", "Aria", "Jackson", "Scarlett", "Alexander", "Grace",
        "Mateo", "Chloe", "Michael", "Victoria", "Daniel", "Zoe", "William", "Luna", "Levi", "Hannah",
        "Gabriel", "Addison", "Carter", "Willow", "Wyatt", "Nora", "Isaac", "Layla", "Eli", "Hazel",
    ]
    
    @staticmethod
    def get_username() -> str:
        """
        Generate a realistic Roblox username.
        
        Returns:
            Generated username (3-20 characters, alphanumeric + underscore)
        """
        separators = ["", "_", "."]
        
        # Choose strategy
        use_human_name = random.random() < 0.4
        
        # Select word parts
        part1 = random.choice(RobloxProfile.HUMAN_NAMES) if use_human_name else random.choice(RobloxProfile.WORD_PARTS)
        part2 = random.choice(RobloxProfile.WORD_PARTS)
        
        # Ensure parts are different
        while part2.lower() == part1.lower():
            part2 = random.choice(RobloxProfile.WORD_PARTS)
        
        # Optional elements
        birth_year = str(random.randint(2002, 2024)) if random.random() < 0.2 else ""
        short_number = str(random.randint(10, 99)) if random.random() < 0.1 else ""
        
        # Sometimes add third part
        if random.random() < 0.2:
            part3 = random.choice(RobloxProfile.WORD_PARTS)
            while part3.lower() in [part1.lower(), part2.lower()]:
                part3 = random.choice(RobloxProfile.WORD_PARTS)
            parts = [part1, part2, part3]
        else:
            parts = [part1, part2]
        
        # Join with separator
        username = "".join(random.choice(separators).join(parts).split())
        
        # Special formatting
        if random.random() < 0.15:
            username = f"Xx_{username}_xX"
        elif random.random() < 0.1:
            username = f"Xx{username}xX"
        
        # Add numbers
        if birth_year:
            username += birth_year
        if short_number:
            username += short_number
        if random.random() < 0.05:
            username += "_YT" if random.random() < 0.5 else "YT"
        
        # Leet speak substitutions
        if random.random() < 0.2:
            username = username.replace("o", "0")
        if random.random() < 0.2:
            username = username.replace("e", "3")
        
        # Random capitalization
        parts = username.split("_")
        if len(parts) > 1 and random.random() < 0.3:
            random_index = random.randint(0, len(parts) - 1)
            parts[random_index] = parts[random_index].upper()
            username = "_".join(parts)
        
        # Clean and validate
        username = ''.join(filter(lambda x: x.isalnum() or x == '_', username))
        
        # Ensure length requirements
        if len(username) < 3:
            username += str(random.randint(10, 99))
        if len(username) > 20:
            username = username[:20]
        
        return username
    
    @staticmethod
    def get_password() -> str:
        """
        Generate a secure password for Roblox.
        
        Returns:
            Generated password (12-16 characters)
        """
        # Strong password with mixed characters
        length = random.randint(12, 16)
        
        password = (
            random.choice(string.ascii_uppercase) +
            random.choice(string.ascii_lowercase) +
            random.choice(string.digits) +
            random.choice('!@#$%') +
            ''.join(random.choices(string.ascii_letters + string.digits, k=length - 4))
        )
        
        # Shuffle
        password_list = list(password)
        random.shuffle(password_list)
        
        return ''.join(password_list)
    
    @staticmethod
    def get_birthday() -> str:
        """
        Generate a random birthday (13+ years old for Roblox).
        
        Returns:
            Birthday in ISO format (YYYY-MM-DDTHH:MM:SS.000Z)
        """
        days = [str(i).zfill(2) for i in range(1, 29)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        years = [str(x) for x in range(1997, 2012)]  # 13-28 years old
        
        year = random.choice(years)
        month = random.choice(months)
        day = random.choice(days)
        
        return f"{year}-{month}-{day}T00:00:00.000Z"
    
    @staticmethod
    def get_gender() -> int:
        """
        Get random gender (1 or 2 for Roblox).
        
        Returns:
            Gender value (1 or 2)
        """
        return random.randint(1, 2)
