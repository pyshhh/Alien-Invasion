

class GameStats:

    def __init__(self,ai_game) -> None:

        self.setting = ai_game.setting
        self.reset_stats()

        #highscore should never be resetted
        self.high_score = 0

    def reset_stats(self):
        """initializing stats that can change during the game"""
        self.ships_left = self.setting.ships_limit
        self.game_active = False
        self.score = 0
        self.level = 1




        