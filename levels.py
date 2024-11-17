class Levels:
    levels = [
        {"max_score": 11, "name": "Level 0 – No Proficiency"},
        {"max_score": 13, "name": "Level 0+ – Memorized Proficiency"},
        {"max_score": 16, "name": "Level 1 – Elementary Proficiency"},
        {"max_score": 18, "name": "Level 1+ – Elementary Proficiency, Plus"},
        {"max_score": 21, "name": "Level 2 – Limited Working Proficiency"},
        {"max_score": 23, "name": "Level 2+ – Limited Working Proficiency, Plus"},
        {"max_score": 26, "name": "Level 3 – Professional Working Proficiency"},
        {"max_score": 28, "name": "Level 3+ – Professional Working Proficiency, Plus"},
        {"max_score": 31, "name": "Level 4 – Full Professional Proficiency"},
        {"max_score": 33, "name": "Level 4+ – Full Professional Proficiency, Plus"},
        {"max_score": float('inf'), "name": "Level 5 – Native or Bilingual Proficiency"}
    ]

    @staticmethod
    def determine_level(score):
        """Determine the ILR level based on the score."""
        for level in Levels.levels:
            if score <= level['max_score']:
                return level['name']
        return "Error: Score out of range"