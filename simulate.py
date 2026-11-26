"""Simulate 33 daily backups: 30 normal days, then a gradual ransomware attack."""
import base64
import random
import shutil
from pathlib import Path

from cryptography.fernet import Fernet

from make_data import WORDS

random.seed(42)  # same edits every run

ROOT = Path(__file__).resolve().parent  # the project folder
ORIGINAL_DIR = ROOT / "data" / "original"
SNAP_DIR = ROOT / "snapshots"

NORMAL_DAYS = 30
ATTACKS = {31: 0.05, 32: 0.25, 33: 0.60}  # day -> share of files to encrypt


def normal_day(prev_dir, new_dir):
    # TODO 1: copy yesterday's folder (prev_dir) to make today's folder (new_dir).
    # TODO 2: pick a few text files in new_dir and add a line to the end of each.
    # TODO 3: add one or two new files to new_dir.
    
    shutil.copytree(prev_dir,new_dir)
    
    text_files = sorted(new_dir.glob("*.txt"))
    chosen = random.sample(text_files, k=3)
    for path in chosen:
        line = " ".join(random.choices(WORDS, k=random.randint(10,20)))
        with open(path,"a") as f:
            f.write("\n"+line)

    how_many=random.randint(1,2)
    for i in range(how_many):
        line=" ".join(random.choices(WORDS,k=random.randint(10,20)))
        (new_dir/f"{new_dir.name}_new_{i}.txt").write_text(line)
    

    


def attack_day(prev_dir, new_dir, fraction):
    # We write this after normal_day works.
    shutil.copytree(prev_dir,new_dir)
    files=sorted(new_dir.glob("*"))

    how_many=round(len(files)*(fraction))
    chosen = random.sample(files, k=how_many)

    fernet = Fernet(Fernet.generate_key())

    for path in chosen:
        data = path.read_bytes()
        locked = fernet.encrypt(data)
        encrypted = base64.urlsafe_b64decode(locked)
        path.write_bytes(encrypted)


def main():
    if SNAP_DIR.exists():
        shutil.rmtree(SNAP_DIR)  # delete the old history so every run starts fresh
    SNAP_DIR.mkdir()

    prev_dir = ORIGINAL_DIR
    for day in range(1, NORMAL_DAYS + 1):
        new_dir = SNAP_DIR / f"day_{day:02d}"
        normal_day(prev_dir, new_dir)
        prev_dir = new_dir  # today becomes tomorrow's "yesterday"

    for day, fraction in ATTACKS.items():
        new_dir = SNAP_DIR / f"day_{day:02d}"
        attack_day(prev_dir, new_dir, fraction)
        prev_dir = new_dir

    print(f"snapshots created: {len(list(SNAP_DIR.iterdir()))}")


if __name__ == "__main__":
    main()
