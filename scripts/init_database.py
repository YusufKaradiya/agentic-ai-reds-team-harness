from pathlib import Path
import sys


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from database.database import Database


def main():
    db = Database()

    print("Database initialized successfully.")
    print("Location: data/redteam.db")


if __name__ == "__main__":
    main()