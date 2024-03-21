# Card Shuffling Visualization

This repository contains two Python scripts designed to analyze and visualize the randomness and patterns in card shuffling. The first script, `shuffler.py`, provides a real-time animated histogram to observe the distribution of similarity between consecutively shuffled decks. The second script, `shufflerCSV.py`, exports data on the highest number of matching cards between new and all previously shuffled decks over a specified number of shuffles, which can then be analyzed or visualized externally.

## shuffler.py

### Overview
`shuffler.py` uses `matplotlib` animations to display a histogram that dynamically updates with each shuffle. It allows users to visually track how often cards retain their positions after shuffles, offering insights into the randomness of the shuffling process.

### Usage
python shuffler.py --interval [milliseconds] --n [number of shuffles]


### Arguments
- `--interval`: Interval between frames in milliseconds. Default is 100ms.
- `--n`: Number of recent shuffles to consider for the frequency of increase. Default is 50.

### Requirements
- Python 3
- `matplotlib`
- `numpy`

## shufflerCSV.py

### Overview
`shufflerCSV.py` exports the results of card shuffling into a CSV file. Each row contains the number of decks shuffled and the highest number of matching cards found between a new deck and all previously shuffled decks.

### Usage
The script is executed without command-line arguments and begins processing automatically. It saves the output to a CSV file in a directory named `CreatedCSVs`.

### Functionality
- Creates a CSV file with a timestamp in the filename.
- Writes the number of decks shuffled and the highest number of matching cards for each iteration.

### Requirements
- Python 3
- `numpy`
- `random`

## Installation
Ensure you have Python 3 installed along with the required libraries: `matplotlib`, `numpy`, and `random` (built-in). You can install `matplotlib` and `numpy` using pip:

pip install matplotlib numpy

## License
[MIT](https://choosealicense.com/licenses/mit/)