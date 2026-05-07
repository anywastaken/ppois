import json
import os

class HighScoreManager:
    def __init__(self, filename="configs/highscores.json"):
        """Инициализация менеджера таблицы рекордов"""
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        """Загрузка и сортировка сохраненных рекордов"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                return sorted(json.load(f), key=lambda x: x['score'], reverse=True)
        except:
            return []

    def check_new_record(self, current_score):
        """Проверка попадания результата в таблицу рекордов"""
        if not self.scores or len(self.scores) < 10:
            return True
        return current_score > self.scores[-1]['score']

    def add_score(self, name, score):
        """Добавление нового результата в таблицу рекордов"""
        self.scores.append({"name": name, "score": score})
        self.scores = sorted(self.scores, key=lambda x: x['score'], reverse=True)[:10]
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f, indent=4)
