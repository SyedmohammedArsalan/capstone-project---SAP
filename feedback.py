import json
import os
from datetime import datetime

class UserPreferences:
    def __init__(self):
        self.file_path = "user_prefs.json"
        self.load_prefs()
    
    def load_prefs(self):
        if os.path.exists(self.file_path):
            with open(self.file_path) as f:
                data = json.load(f)
                self.styles = data.get('styles', [])
                self.colors = data.get('colors', [])
                self.budget = data.get('budget', 200)
                self.history = data.get('history', [])
        else:
            self.styles = []
            self.colors = []
            self.budget = 200
            self.history = []
    
    def update(self, styles, colors, budget):
        self.styles = styles
        self.colors = colors
        self.budget = budget
        self.save()
    
    def add_history(self, item):
        self.history.append({
            "item": item,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def save(self):
        data = {
            "styles": self.styles,
            "colors": self.colors,
            "budget": self.budget,
            "history": self.history
        }
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def get_styles(self):
        return ["Casual", "Formal", "Bohemian", "Streetwear"]
    
    def get_history(self):
        return [h['item'] for h in self.history[-10:]]