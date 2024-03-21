"""
This script visualizes the randomness of card shuffling using a histogram and matplotlib animations. 
It demonstrates the distribution of similarity between consecutively shuffled decks over time, 
allowing for the dynamic observation of how often cards retain their positions after shuffles. 

Usage:
    python script_name.py --interval [milliseconds] --n [number of shuffles]

Arguments:
    --interval: Interval between frames in milliseconds (default=100).
    --n: Number of recent shuffles to consider for the frequency of increase (default=50).
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
import random
from matplotlib.colors import LinearSegmentedColormap
import argparse

parser = argparse.ArgumentParser(description='Animation Interval Setter')
parser.add_argument('--interval', type=int, default=100,
                    help='Interval between frames in milliseconds')
parser.add_argument('--n', type=int, default=50,
                    help='Number of recent shuffles to consider for frequency of increase')
args = parser.parse_args()

def shuffle_deck():
    """Returns a shuffled deck of cards."""
    return random.sample(range(52), 52)

def compare_decks(deck1, deck2):
    """Returns the count of matching cards at the same positions in two decks."""
    return sum(card1 == card2 for card1, card2 in zip(deck1, deck2))

shuffled_decks = [shuffle_deck()]
similarity_histogram = np.zeros(53)
rolling_histograms = np.zeros((args.n, 53))  # Track the last n histograms
total_decks_shuffled = 1

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)

colors = ["orange", "green", "green"] 
cmap = LinearSegmentedColormap.from_list("my_colormap", colors)

def animate(i):
    global shuffled_decks, similarity_histogram, rolling_histograms, total_decks_shuffled
    
    new_deck = shuffle_deck()
    shuffled_decks.append(new_deck)
    total_decks_shuffled += 1
    
    previous_histogram = similarity_histogram.copy()

    current_max_similarity = 0
    for previous_deck in shuffled_decks[:-1]:
        match_count = compare_decks(new_deck, previous_deck)
        if match_count > current_max_similarity:
            current_max_similarity = match_count

    similarity_histogram[current_max_similarity] += 1
    
    # Update rolling histograms
    rolling_histograms = np.roll(rolling_histograms, -1, axis=0)
    rolling_histograms[-1, :] = similarity_histogram - previous_histogram
    
    # Calculate frequency of increase for each position, adjusting for the number of shuffles
    min_shuffles_for_n = min(total_decks_shuffled, args.n)
    increase_frequency = np.sum(rolling_histograms[-min_shuffles_for_n:] > 0, axis=0) / min_shuffles_for_n
    
    ax.clear()
    norm = plt.Normalize(0, 1)  # Normalize frequency between 0 and 1
    bars = ax.bar(range(53), similarity_histogram, color=cmap(norm(increase_frequency)))
    max_x_limit = np.max(np.nonzero(similarity_histogram))  # Find last non-zero index for max value
    
     # Calculating the average total value among the cards
    weighted_totals = np.dot(range(53), similarity_histogram)
    average_similarity = weighted_totals / np.sum(similarity_histogram)
    
    for idx, bar in enumerate(bars):
        height = bar.get_height()
        if height > 0:
            text_x_position = bar.get_x() + bar.get_width() / 2.
            if idx == 0: 
                text_x_position += 0.1
            ax.text(text_x_position, height + .5, f'{int(height)}', ha='center', va='bottom')
    
    # Displaying the max value and average similarity
    ax.text(0.95, 0.95, f'Max Value: {max_x_limit}\nAvg Similarity: {average_similarity:.2f}', 
            ha='right', va='top', transform=ax.transAxes, fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
    
    ax.set_title(f"Frequency of Maximum Similarity per Shuffle (Total Decks: {total_decks_shuffled})")
    ax.set_xlabel("Number of Matching Cards")
    ax.set_ylabel("Frequency")
    ax.set_xlim([0, max_x_limit + 1]) 
    ax.set_ylim([0, np.max(similarity_histogram) * 1.05 + 5])


animation_running = True

def toggle_shuffling(event):
    global animation_running
    if animation_running:
        ani.event_source.stop()
        button.label.set_text("Start Shuffling")
    else:
        ani.event_source.start()
        button.label.set_text("Stop Shuffling")
    animation_running = not animation_running

ani = animation.FuncAnimation(fig, animate, interval=args.interval)

button_width = 0.2
button_height = 0.075
button_left = 0.78
button_bottom = 0.05

ax_button = plt.axes([button_left, button_bottom, button_width, button_height])
button = Button(ax_button, 'Stop Shuffling')
button.on_clicked(toggle_shuffling)

plt.show()
