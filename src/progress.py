import os

class Progress:
    def __init__(self, save_file="progress.dat", generated_progress_file="generated_progress.dat"):
        self.save_file = save_file
        self.generated_progress_file = generated_progress_file
        self.completed_levels = self.load_progress()
        self.completed_generated = self.load_generated_progress()

    def load_progress(self):
        if not os.path.exists(self.save_file):
            return set()
        with open(self.save_file, "r") as f:
            return set(int(line.strip()) for line in f.readlines())

    def load_generated_progress(self):
        if not os.path.exists(self.generated_progress_file):
            return 0
        with open(self.generated_progress_file, "r") as f:
            return int(f.read().strip())

    def save_progress(self):
        with open(self.save_file, "w") as f:
            for level in self.completed_levels:
                f.write(f"{level}\n")

    def save_generated_progress(self):
        with open(self.generated_progress_file, "w") as f:
            f.write(str(self.completed_generated))

    def add_completed_level(self, level_index):
        self.completed_levels.add(level_index)
        self.save_progress()

    def add_completed_generated(self):
        self.completed_generated += 1
        self.save_generated_progress()

    def get_total_completed(self):
        return len(self.completed_levels) + self.completed_generated 