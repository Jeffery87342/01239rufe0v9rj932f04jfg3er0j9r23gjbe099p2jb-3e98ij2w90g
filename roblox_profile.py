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
        Generate a completely randomized Roblox username with mixed capitalization.
        
        Returns:
            Generated username (3-20 characters, alphanumeric + underscore)
        """
        # Strategy 1: Fully random alphanumeric (40% chance)
        if random.random() < 0.4:
            length = random.randint(8, 15)
            username = ''.join(
                random.choice(string.ascii_letters + string.digits) 
                for _ in range(length)
            )
            # Apply random capitalization to each character
            username = ''.join(
                c.upper() if random.random() < 0.5 else c.lower() 
                for c in username
            )
            # Add random numbers at the end (30% chance)
            if random.random() < 0.3:
                username += str(random.randint(100, 9999))
        
        # Strategy 2: Word-based with heavy randomization (60% chance)
        else:
            separators = ["", "_", ""]
            
            # Select word parts
            use_human_name = random.random() < 0.3
            part1 = random.choice(RobloxProfile.HUMAN_NAMES) if use_human_name else random.choice(RobloxProfile.WORD_PARTS)
            part2 = random.choice(RobloxProfile.WORD_PARTS)
            
            # Ensure parts are different
            while part2.lower() == part1.lower():
                part2 = random.choice(RobloxProfile.WORD_PARTS)
            
            # Sometimes add third part (30% chance)
            if random.random() < 0.3:
                part3 = random.choice(RobloxProfile.WORD_PARTS)
                while part3.lower() in [part1.lower(), part2.lower()]:
                    part3 = random.choice(RobloxProfile.WORD_PARTS)
                parts = [part1, part2, part3]
            else:
                parts = [part1, part2]
            
            # Apply COMPLETELY random capitalization to each part
            randomized_parts = []
            for part in parts:
                randomized_part = ''.join(
                    c.upper() if random.random() < 0.5 else c.lower() 
                    for c in part
                )
                randomized_parts.append(randomized_part)
            
            # Join with separator
            username = random.choice(separators).join(randomized_parts)
            
            # Add random numbers (80% chance for more uniqueness)
            if random.random() < 0.8:
                num_length = random.randint(2, 4)
                username += ''.join(str(random.randint(0, 9)) for _ in range(num_length))
            
            # Leet speak substitutions (more aggressive, 40% chance)
            if random.random() < 0.4:
                username = username.replace("o", "0").replace("O", "0")
            if random.random() < 0.4:
                username = username.replace("e", "3").replace("E", "3")
            if random.random() < 0.3:
                username = username.replace("a", "4").replace("A", "4")
            if random.random() < 0.3:
                username = username.replace("i", "1").replace("I", "1")
        
        # Clean and validate
        username = ''.join(filter(lambda x: x.isalnum() or x == '_', username))
        
        # Ensure length requirements
        if len(username) < 3:
            username += ''.join(str(random.randint(0, 9)) for _ in range(3))
        if len(username) > 20:
            username = username[:20]
        
        # Final pass: ensure at least some variation in capitalization
        if username.islower() or username.isupper():
            # Make it mixed case
            username = ''.join(
                c.upper() if random.random() < 0.5 else c.lower() 
                for c in username
            )
        
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
