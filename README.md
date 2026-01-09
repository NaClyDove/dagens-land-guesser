# Dagens Land Solver

An automatic solver for [Dagens Land](https://dagensland.dk) - the Danish geography guessing game where you try to identify the mystery country of the day.

## What is Dagens Land?

Dagens Land ("Today's Country" in Danish) is a Wordle-style geography game. Each day there's a new mystery country, and you guess countries to narrow it down. After each guess, you get:

- **Distance** - How far your guess is from the target (border-to-border, not centroid)
- **Direction** - Which way to look
- **Neighbor indicator** - Whether your guess borders the target country

## How the Solver Works

The solver uses a distance-filtering algorithm:

1. **Start with Germany** - Central location for good triangulation
2. **Filter candidates** - After each guess, eliminate countries that don't match the reported distance
3. **Pick best match** - Choose the candidate whose expected distance best matches the API response
4. **Exploit neighbors** - When distance is 0 km (bordering country), the answer is adjacent

The solver typically finds the answer in **3-6 guesses**.

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/dagens-land-guesser.git
cd dagens-land-guesser

# Run (automatically sets up venv and installs dependencies)
./run.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python solver.py
```

## Example Output

```
Solving for 2026-01-09...
Total countries: 197

1. Tyskland: 2530 km
   Remaining candidates: 23
2. Marokko: 3416 km
   Remaining candidates: 16
3. Egypten: 8 km
   Remaining candidates: 3
4. Israel: 0 km  (NEIGHBOR!)
   Remaining candidates: 2
5. Jordan: CORRECT!

========================================
Found: Jordan in 5 guesses
```

## How Distance is Calculated

According to Dagens Land, distances are calculated as:

- **Data source**: Natural Earth 50m dataset
- **Coordinate system**: WGS84 (EPSG:4326)
- **Method**: ~100 points sampled along each country's border, shortest geodesic distance between point pairs
- **Library**: Turf.js

This means distances are **border-to-border**, not centroid-to-centroid, which is why small countries and islands can have surprisingly short distances to large neighbors.

## Country List

The solver includes ~197 countries with Danish names (Danmark, Sverige, Tyskland, etc.) and approximate geographic centroids. The list covers all sovereign nations recognized by the game.

## Requirements

- Python 3.8+
- requests

## License

MIT
