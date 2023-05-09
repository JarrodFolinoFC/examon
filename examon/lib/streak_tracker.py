class StreakTracker:
    def __init__(self):
        self.__current_streak = 0
        self.__best = 0
        self.__streaks = []

    def increment(self):
        self.__current_streak += 1
        if self.__current_streak > self.__best:
            self.__best = self.__current_streak
    def reset(self):
        if self.__current_streak != 0:
            self.__streaks.append(self.__best)
        self.__current_streak = 0

    def summary(self):
        return self.__best, self.__streaks
