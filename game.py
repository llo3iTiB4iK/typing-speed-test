from random import shuffle


class Game:
    def __init__(self):
        self.words_to_enter = []
        self.words_entered = []
        with open("google-10000-english-usa-no-swears-medium.txt") as file:
            self.words = [word.strip() for word in file.readlines()]

    def reset(self):
        self.words_to_enter.clear()
        self.words_entered.clear()

    def shuffle_words(self):
        shuffle(self.words)

    def enter_word(self, entered_word):
        self.words_to_enter.append(self.words.pop(0))
        self.words_entered.append(entered_word)

    def get_stats(self):
        cpm = len(" ".join(self.words_entered))
        wpm = cpm / 5
        correct_symbols = len(self.words_entered) - 1
        for expected, entered in zip(self.words_to_enter, self.words_entered):
            for index in range(len(expected)):
                try:
                    if expected[index] == entered[index]:
                        correct_symbols += 1
                except IndexError:
                    break
        acc = round(correct_symbols / cpm * 100, 1)
        return cpm, wpm, acc
