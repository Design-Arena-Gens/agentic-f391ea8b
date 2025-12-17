from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class EpisodicMemory:
    def __init__(self, storage_path: str = "./data/episodic"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.episodes_file = os.path.join(storage_path, "episodes.json")
        self.episodes = self._load_episodes()

    def _load_episodes(self) -> List[Dict]:
        if os.path.exists(self.episodes_file):
            with open(self.episodes_file, 'r') as f:
                return json.load(f)
        return []

    def _save_episodes(self):
        with open(self.episodes_file, 'w') as f:
            json.dump(self.episodes, f, indent=2)

    def add_episode(self, interaction: Dict) -> str:
        episode = {
            'id': str(len(self.episodes)),
            'timestamp': datetime.utcnow().isoformat(),
            'user_message': interaction.get('user_message', ''),
            'agent_response': interaction.get('agent_response', ''),
            'tools_used': interaction.get('tools_used', []),
            'context': interaction.get('context', {})
        }
        self.episodes.append(episode)
        self._save_episodes()
        return episode['id']

    def get_recent_episodes(self, n: int = 10) -> List[Dict]:
        return self.episodes[-n:]

    def get_episode(self, episode_id: str) -> Optional[Dict]:
        for episode in self.episodes:
            if episode['id'] == episode_id:
                return episode
        return None

    def search_episodes(self, query: str) -> List[Dict]:
        results = []
        query_lower = query.lower()
        for episode in self.episodes:
            if (query_lower in episode['user_message'].lower() or
                query_lower in episode['agent_response'].lower()):
                results.append(episode)
        return results

    def clear_all(self):
        self.episodes = []
        self._save_episodes()
