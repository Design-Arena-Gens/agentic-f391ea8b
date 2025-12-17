from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import numpy as np

class LearningEngine:
    def __init__(self, storage_path: str = "./data/learning"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.patterns_file = os.path.join(storage_path, "patterns.json")
        self.skills_file = os.path.join(storage_path, "skills.json")
        self.patterns = self._load_patterns()
        self.skills = self._load_skills()

    def _load_patterns(self) -> List[Dict]:
        if os.path.exists(self.patterns_file):
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        return []

    def _load_skills(self) -> Dict:
        if os.path.exists(self.skills_file):
            with open(self.skills_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_patterns(self):
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)

    def _save_skills(self):
        with open(self.skills_file, 'w') as f:
            json.dump(self.skills, f, indent=2)

    def detect_pattern(self, interaction: Dict) -> Optional[str]:
        """Detect patterns in user interactions"""
        user_msg = interaction.get('user_message', '').lower()

        # Check existing patterns
        for pattern in self.patterns:
            if any(keyword in user_msg for keyword in pattern['keywords']):
                pattern['frequency'] += 1
                pattern['last_seen'] = datetime.utcnow().isoformat()
                self._save_patterns()
                return pattern['id']

        # Create new pattern if certain keywords appear
        keywords = self._extract_keywords(user_msg)
        if len(keywords) >= 2:
            pattern = {
                'id': f"pattern_{len(self.patterns)}",
                'keywords': keywords,
                'frequency': 1,
                'first_seen': datetime.utcnow().isoformat(),
                'last_seen': datetime.utcnow().isoformat()
            }
            self.patterns.append(pattern)
            self._save_patterns()
            return pattern['id']

        return None

    def _extract_keywords(self, text: str) -> List[str]:
        # Simple keyword extraction
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = text.lower().split()
        keywords = [w for w in words if len(w) > 3 and w not in common_words]
        return keywords[:5]

    def learn_skill(self, skill_name: str, skill_data: Dict):
        """Learn or improve a skill"""
        if skill_name not in self.skills:
            self.skills[skill_name] = {
                'level': 1,
                'uses': 0,
                'success_rate': 0.0,
                'created': datetime.utcnow().isoformat(),
                'data': skill_data
            }
        else:
            self.skills[skill_name]['uses'] += 1
            self.skills[skill_name]['level'] = min(10, self.skills[skill_name]['uses'] // 10 + 1)

        self._save_skills()

    def update_skill_success(self, skill_name: str, success: bool):
        """Update skill success rate"""
        if skill_name in self.skills:
            current_rate = self.skills[skill_name]['success_rate']
            uses = self.skills[skill_name]['uses']
            new_rate = (current_rate * uses + (1.0 if success else 0.0)) / (uses + 1)
            self.skills[skill_name]['success_rate'] = new_rate
            self._save_skills()

    def get_patterns(self) -> List[Dict]:
        return sorted(self.patterns, key=lambda x: x['frequency'], reverse=True)

    def get_skills(self) -> Dict:
        return self.skills

    def get_learning_stats(self) -> Dict:
        return {
            'total_patterns': len(self.patterns),
            'total_skills': len(self.skills),
            'avg_skill_level': np.mean([s['level'] for s in self.skills.values()]) if self.skills else 0,
            'patterns': self.get_patterns()[:5],
            'top_skills': sorted(self.skills.items(), key=lambda x: x[1]['level'], reverse=True)[:5]
        }
