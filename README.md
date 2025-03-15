# Telegram-Osint

## Overview
This tool extracts OSINT (Open Source Intelligence) data from Telegram, including user details, messages, sentiment analysis, group members, and keyword-based message searches. It can also extract emails and phone numbers from messages and export the collected data.

## Features
- Fetch user details (ID, username, phone, last seen, profile photo)
- Extract recent messages from users, groups, or channels
- Perform sentiment analysis on messages
- Extract group members from a public/private group
- Search messages for specific keywords (e.g., "password", "email")
- Extract email addresses and phone numbers from messages
- Export data to JSON and CSV files

## Installation

### **Prerequisites**
- Python 3.8+
- Telegram API credentials (API ID & API Hash from [my.telegram.org](https://my.telegram.org/))

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/Telegram-OSINT-Tool.git
cd Telegram-OSINT-Tool
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Configure API Credentials**
1. Go to [my.telegram.org](https://my.telegram.org/) and log in.
2. Navigate to **API Development Tools**.
3. Create a new app and note down the **API ID** and **API Hash**.
4. Edit `telegram_osint.py` and replace the placeholders:
   ```python
   API_ID = "your_api_id"
   API_HASH = "your_api_hash"
   ```

### **Step 4: Run the Tool**
```bash
python telegram_osint.py
```

## Usage
1. Enter the Telegram username, group, or channel ID when prompted.
2. The script will fetch user details, messages, and perform keyword searches.
3. Extracted data will be saved in `osint_results.json` and `osint_results.csv`.

## Example Output
```bash
✅ Connected to Telegram!
🔍 User Information:
User ID: 123456789
Username: example_user
First Name: John
Last Name: Doe
Phone: Hidden
Last Seen: Recently
📸 Profile photo saved: example_user_profile.jpg

📩 Recent Messages:
💬 Sender: 123456789 | 📅 Date: 2025-03-15 | 📜 Message: "This is a test message." | 😊 Sentiment: Neutral
```

## Contributing
Feel free to submit issues or pull requests if you have improvements!

## License
This project is licensed under the MIT License.
