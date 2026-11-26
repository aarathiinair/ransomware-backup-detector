"""Create ~200 normal files in data/original/ (text, CSV, and a few real JPG/PDFs)."""
import csv
import random
import shutil
from pathlib import Path

random.seed(42)  # same data every run

OUT_DIR = Path("data/original")

# Real, naturally high-entropy files from your laptop. Edit this list.
REAL_FILES = [
    r"C:\Windows\Web\Wallpaper\ThemeA\img20.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeA\img21.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeA\img22.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeA\img23.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeB\img24.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeB\img25.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeB\img26.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeB\img27.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeC\img28.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeC\img29.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeC\img30.jpg",
    r"C:\Windows\Web\Wallpaper\ThemeC\img31.jpg",
]

WORDS = ["backup", "report", "invoice", "meeting", "budget", "client", "project",
         "draft", "summary", "review", "update", "schedule", "notes", "data"]

N_TEXT = 80
N_CSV = 80


def make_text_files():
    for i in range(N_TEXT):
        n_words=random.randint(500,5000)
        words=random.choices(WORDS,k=n_words)
        text=" ".join(words)
        (OUT_DIR/f"text_{i:03d}.txt").write_text(text)
    return N_TEXT
        


def make_csv_files():
    for i in range(N_CSV):
        n_rows = random.randint(100, 1000)
        with open(OUT_DIR / f"table_{i:03d}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id","value_a","value_b"])              # header: 3 column names
            for row_id in range(n_rows):        # inner loop: one pass per row
                writer.writerow([row_id,random.randint(0,1000),random.randint(0,1000)])          # row: row_id + 2 random numbers
    return N_CSV


def copy_real_files():
    count=0
    for p in REAL_FILES:
        if not Path(p).exists():
            print(f"warning: {p} not found")
            continue
        shutil.copy(p,OUT_DIR)
        count+=1
    return count


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    n_text = make_text_files()
    n_csv = make_csv_files()
    n_real = copy_real_files()
    print(f"text: {n_text}, csv: {n_csv}, real: {n_real}, total: {len(list(OUT_DIR.iterdir()))}")


if __name__ == "__main__":
    main()
