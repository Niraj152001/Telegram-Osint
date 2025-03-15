import os
import re
import csv
import json
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, MessageMediaPhoto, MessageMediaDocument, MessageMediaGeo
from textblob import TextBlob

# Telegram API Credentials (Replace with your details)
API_ID = ""
API_HASH = ""

# Initialize Telegram Client
client = TelegramClient("session_name", API_ID, API_HASH)

async def get_user_info(username):
    """Fetch user details including profile photo and last seen."""
    try:
        user = await client.get_entity(username)
        print("\nðŸ” User Information:")
        user_data = {
            "User ID": user.id,
            "Username": user.username,
            "First Name": user.first_name,
            "Last Name": user.last_name if user.last_name else "None",
            "Phone": user.phone if user.phone else "Hidden",
            "Last Seen": user.status.__class__.__name__ if hasattr(user, 'status') else "Unknown"
        }
        for key, value in user_data.items():
            print(f"{key}: {value}")

        # Download Profile Photo
        if user.photo:
            profile_pic_path = f"{user.username}_profile.jpg"
            await client.download_profile_photo(user, file=profile_pic_path)
            print(f"ðŸ“¸ Profile photo saved: {profile_pic_path}")
        else:
            print("âŒ No profile photo found.")

        return user_data

    except Exception as e:
        print(f"âŒ Error fetching user details: {e}")
        return {}

async def fetch_messages(username):
    """Fetch recent messages from a user, group, or channel."""
    try:
        entity = await client.get_entity(username)
        messages = await client(GetHistoryRequest(
            peer=entity,
            limit=20,  
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        extracted_messages = []
        print("\nðŸ“© Recent Messages:")
        for message in messages.messages:
            sender = message.from_id.user_id if message.from_id else "Unknown"
            text = message.message if message.message else "Media/Non-text message"
            date = message.date.strftime("%Y-%m-%d %H:%M:%S")
            sentiment = TextBlob(text).sentiment.polarity  # Sentiment Analysis

            extracted_messages.append({
                "Sender": sender,
                "Date": date,
                "Message": text,
                "Sentiment": "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
            })

            print(f"ðŸ†” Sender: {sender} | ðŸ“… Date: {date} | ðŸ“œ Message: {text} | ðŸ˜Š Sentiment: {extracted_messages[-1]['Sentiment']}")

            # Download Media if present
            if message.media:
                if isinstance(message.media, MessageMediaPhoto) or isinstance(message.media, MessageMediaDocument):
                    file_path = await client.download_media(message)
                    print(f"ðŸ“¥ Media downloaded: {file_path}")
                elif isinstance(message.media, MessageMediaGeo):
                    print(f"ðŸ“ Location Shared: {message.media.geo}")

        return extracted_messages

    except Exception as e:
        print(f"âŒ Error fetching messages: {e}")
        return []

async def extract_group_members(group_name):
    """Extracts and lists members of a group or channel."""
    try:
        group = await client.get_entity(group_name)
        members = await client(GetParticipantsRequest(
            channel=group,
            filter=ChannelParticipantsSearch(""),
            offset=0,
            limit=50,
            hash=0
        ))

        print("\nðŸ‘¥ Group Members:")
        member_list = [{"ID": member.id, "Username": member.username} for member in members.users]
        for member in member_list:
            print(f"ðŸ†” ID: {member['ID']} | ðŸ‘¤ Username: {member['Username']}")

        return member_list

    except Exception as e:
        print(f"âŒ Error fetching group members: {e}")
        return []

async def search_keywords(username, keywords):
    """Search for messages containing specific keywords or hashtags."""
    messages = await fetch_messages(username)
    keyword_results = [msg for msg in messages if any(kw.lower() in msg["Message"].lower() for kw in keywords)]

    print("\nðŸ”Ž Keyword Search Results:")
    for result in keyword_results:
        print(f"ðŸ†” Sender: {result['Sender']} | ðŸ“… Date: {result['Date']} | ðŸ“œ Message: {result['Message']}")

    return keyword_results

async def extract_emails_and_phones(username):
    """Extract emails and phone numbers from messages."""
    messages = await fetch_messages(username)
    emails = set()
    phones = set()

    for msg in messages:
        emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", msg["Message"]))
        phones.update(re.findall(r"\+?\d[\d -]{8,}\d", msg["Message"]))

    print("\nðŸ“§ Extracted Emails & Phones:")
    print(f"Emails: {emails if emails else 'None'}")
    print(f"Phones: {phones if phones else 'None'}")

    return {"emails": list(emails), "phones": list(phones)}

async def export_data_to_file(filename, data):
    """Exports collected OSINT data to JSON & CSV files."""
    with open(f"{filename}.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    with open(f"{filename}.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"âœ… Data exported to {filename}.json and {filename}.csv")

async def main():
    await client.start()
    print("âœ… Connected to Telegram!\n")

    username = input("Enter the username, group, or channel ID: ")

    user_data = await get_user_info(username)
    messages = await fetch_messages(username)
    group_members = await extract_group_members(username)
    keyword_search = await search_keywords(username, ["password", "email", "phone"])
    extracted_contacts = await extract_emails_and_phones(username)

    # Save all collected data
    all_data = {
        "User Information": user_data,
        "Messages": messages,
        "Group Members": group_members,
        "Keyword Search": keyword_search,
        "Extracted Contacts": extracted_contacts
    }
    await export_data_to_file("osint_results", [all_data])

with client:
    client.loop.run_until_complete(main())