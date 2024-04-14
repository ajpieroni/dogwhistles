import csv
import pandas as pd
# /opt/homebrew/bin/python3.11 "/Users/alexpieroni/Documents/Documents - Alex’s MacBook /Projects/dogwhistles/parse.py"

# Sample non-dogwhistle sentences
non_dogwhistles = [
    "I just finished reading a great book.",
    "It's a beautiful day outside.",
    "We should meet up for coffee sometime.",
    "I need to buy some groceries later.",
    "Can you help me with this project?",
    "I'm going to watch a movie tonight.",
    "I love spending time with my family.",
    "What's your favorite kind of music?",
    "I've been learning how to play the guitar.",
    "Let's go for a walk in the park.",
    "Do you have any plans for the weekend?",
    "I usually wake up early in the morning.",
    "I like to stay organized.",
    "That restaurant has great reviews.",
    "I need to clean my room.",
    "The weather has been really nice lately.",
    "I'm planning a trip for next month.",
    "I've been feeling a bit tired lately.",
    "I think I need a new laptop.",
    "That's a very interesting point.",
    "I usually prefer tea over coffee.",
    "I need to get a haircut soon.",
    "Do you have any recommendations for a good book?",
    "I think it's going to rain today.",
    "I need to charge my phone.",
    "Let's get together soon.",
    "I'm looking forward to the holidays.",
    "That's a great idea!",
    "I think I saw you at the concert last night.",
    "I usually go to bed around 10 PM.",
    "I need to finish some work before I go out.",
    "I've been trying to eat healthier.",
    "Can you send me the details?",
    "I'm looking for a new job.",
    "Do you know where I left my keys?",
    "I think we met before.",
    "I like to spend my free time reading.",
    "I need to make an appointment.",
    "That's exactly what I was thinking.",
    "I'm not sure where we should go.",
    "I'm trying to save money for a car.",
    "I need to study for my exam.",
    "Can you tell me more about that?",
    "I like your shoes.",
    "Let's share a taxi.",
    "I need some advice on something.",
    "It's getting late, I should head home.",
    "Can you explain this to me?",
    "I think you're right.",
    "I need to relax a bit this weekend."
]

# Append to the existing CSV
csv_file = 'dogwhistle_dataset.csv'

# Open the CSV to append
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for sentence in non_dogwhistles:
        writer.writerow([sentence, 0])  # Append non-dogwhistle with label 0

# Notify completion
print(f"Added 50 non-dogwhistle entries to {csv_file}.")

