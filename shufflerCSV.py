import numpy as np
import random
import csv
import datetime
import os

def shuffle_deck():
    """Shuffles and returns a deck of 52 cards."""
    return random.sample(range(52), 52)

def compare_decks(new_deck, previous_decks):
    """Compares the new deck against all previous decks and returns the highest number of matching cards."""
    max_similarity = 0
    for deck in previous_decks:
        match_count = sum(card1 == card2 for card1, card2 in zip(new_deck, deck))
        max_similarity = max(max_similarity, match_count)
    return max_similarity

def perform_shuffles_and_save(start=2, step=10, max_decks=1000000):
    # Generate the directory and filename within the current working directory or a subdirectory
    dir_name = "CreatedCSVs/"  # Adjusted to be relative to the current working directory
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)  # Create the directory if it doesn't exist
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{dir_name}{current_time}.csv"
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number of Decks Shuffled', 'Highest Number of Matching Cards'])

        previous_decks = [shuffle_deck()]  # Start with one shuffled deck
        for num_decks in range(start, max_decks + 1, step):
            new_deck = shuffle_deck()
            max_similarity = compare_decks(new_deck, previous_decks)
            previous_decks.append(new_deck)  # Add the new deck to the collection of previous decks

            writer.writerow([num_decks, max_similarity])
            print(f"Processed {num_decks} decks: Max Matching Cards = {max_similarity}")

perform_shuffles_and_save()
