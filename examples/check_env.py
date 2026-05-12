import os
import sys

from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    print(f"Python: {sys.version.split()[0]}")

    if sys.version_info < (3, 10):
        print("Attention: utilise Python 3.10+ pour l'Agents SDK.")
    else:
        print("Version Python OK.")

    if os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY trouvee.")
    else:
        print("OPENAI_API_KEY absente. Cree un fichier .env ou exporte la variable.")


if __name__ == "__main__":
    main()
