# Bakalauras 2024
 "Discord"
## Setting Up the Project

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

Edit .env file:
DISCORD_BOT_TOKEN=your-token-here

Run the bot:
python bot.py

To just launch on docker:
docker build -t discord-bot .
docker run --env-file .env discord-bot