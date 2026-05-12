#!/usr/bin/env python3
import requests
from math import radians, sin, cos, sqrt, atan2
from datetime import date

# Complete list of countries with Danish names and approximate centroids (lat, lon)
COUNTRIES = {
    # Europe
    "Danmark": (56.0, 10.0),
    "Sverige": (62.0, 15.0),
    "Norge": (62.0, 10.0),
    "Finland": (64.0, 26.0),
    "Island": (65.0, -18.0),
    "Tyskland": (51.0, 9.0),
    "Frankrig": (46.0, 2.0),
    "Spanien": (40.0, -4.0),
    "Portugal": (39.5, -8.0),
    "Italien": (42.0, 12.0),
    "Polen": (52.0, 20.0),
    "Storbritannien": (54.0, -2.0),
    "Irland": (53.0, -8.0),
    "Nederlandene": (52.0, 5.0),
    "Belgien": (50.5, 4.0),
    "Schweiz": (47.0, 8.0),
    "Østrig": (47.5, 14.0),
    "Tjekkiet": (50.0, 15.0),
    "Slovakiet": (48.5, 19.5),
    "Ungarn": (47.0, 20.0),
    "Rumænien": (46.0, 25.0),
    "Bulgarien": (43.0, 25.0),
    "Grækenland": (39.0, 22.0),
    "Kroatien": (45.0, 16.0),
    "Slovenien": (46.0, 15.0),
    "Serbien": (44.0, 21.0),
    "Bosnien-Hercegovina": (44.0, 18.0),
    "Montenegro": (42.5, 19.0),
    "Nordmakedonien": (41.5, 22.0),
    "Albanien": (41.0, 20.0),
    "Kosovo": (42.5, 21.0),
    "Ukraine": (49.0, 32.0),
    "Belarus": (53.0, 28.0),
    "Moldova": (47.0, 29.0),
    "Litauen": (55.0, 24.0),
    "Letland": (57.0, 25.0),
    "Estland": (59.0, 26.0),
    "Luxembourg": (49.75, 6.0),
    "Monaco": (43.75, 7.4),
    "Andorra": (42.5, 1.5),
    "Liechtenstein": (47.15, 9.5),
    "San Marino": (43.94, 12.45),
    "Vatikanstaten": (41.9, 12.45),
    "Malta": (35.9, 14.4),
    "Cypern": (35.0, 33.0),

    # Russia & Caucasus
    "Rusland": (60.0, 100.0),
    "Tyrkiet": (39.0, 35.0),
    "Georgien": (42.0, 43.5),
    "Armenien": (40.0, 45.0),
    "Aserbajdsjan": (40.5, 47.5),

    # Middle East
    "Israel": (31.0, 35.0),
    "Palæstina": (32.0, 35.2),
    "Libanon": (34.0, 36.0),
    "Syrien": (35.0, 38.0),
    "Jordan": (31.0, 36.0),
    "Irak": (33.0, 44.0),
    "Iran": (32.0, 53.0),
    "Saudi-Arabien": (24.0, 45.0),
    "Yemen": (15.5, 48.0),
    "Oman": (21.0, 57.0),
    "Forenede Arabiske Emirater": (24.0, 54.0),
    "Qatar": (25.5, 51.0),
    "Bahrain": (26.0, 50.5),
    "Kuwait": (29.5, 47.5),

    # Central Asia
    "Kasakhstan": (48.0, 68.0),
    "Usbekistan": (41.0, 64.0),
    "Turkmenistan": (39.0, 59.0),
    "Tadsjikistan": (39.0, 71.0),
    "Kirgisistan": (41.0, 75.0),
    "Afghanistan": (33.0, 65.0),

    # South Asia
    "Indien": (22.0, 79.0),
    "Pakistan": (30.0, 70.0),
    "Bangladesh": (24.0, 90.0),
    "Sri Lanka": (7.0, 81.0),
    "Nepal": (28.0, 84.0),
    "Bhutan": (27.5, 90.5),
    "Maldiverne": (3.0, 73.0),

    # East Asia
    "Kina": (35.0, 105.0),
    "Japan": (36.0, 138.0),
    "Sydkorea": (36.0, 128.0),
    "Nordkorea": (40.0, 127.0),
    "Mongoliet": (46.0, 105.0),
    "Taiwan": (23.5, 121.0),

    # Southeast Asia
    "Thailand": (15.0, 101.0),
    "Vietnam": (16.0, 108.0),
    "Cambodja": (13.0, 105.0),
    "Laos": (18.0, 105.0),
    "Myanmar": (21.0, 96.0),
    "Malaysia": (4.0, 109.0),
    "Singapore": (1.35, 103.8),
    "Indonesien": (-2.0, 118.0),
    "Filippinerne": (12.0, 122.0),
    "Brunei": (4.5, 114.5),
    "Østtimor": (-8.5, 126.0),

    # Africa - North
    "Egypten": (27.0, 30.0),
    "Libyen": (27.0, 17.0),
    "Tunesien": (34.0, 9.0),
    "Algeriet": (28.0, 3.0),
    "Marokko": (32.0, -6.0),
    "Sudan": (16.0, 30.0),
    "Sydsudan": (7.0, 30.0),

    # Africa - West
    "Mauretanien": (20.0, -10.0),
    "Mali": (17.0, -4.0),
    "Niger": (16.0, 8.0),
    "Tchad": (15.0, 19.0),
    "Senegal": (14.5, -14.5),
    "Gambia": (13.5, -16.0),
    "Guinea-Bissau": (12.0, -15.0),
    "Guinea": (10.0, -10.0),
    "Sierra Leone": (8.5, -11.5),
    "Liberia": (6.5, -9.5),
    "Elfenbenskysten": (8.0, -5.0),
    "Burkina Faso": (12.0, -1.5),
    "Ghana": (8.0, -1.0),
    "Togo": (8.5, 1.0),
    "Benin": (9.5, 2.0),
    "Nigeria": (10.0, 8.0),
    "Kap Verde": (15.0, -23.5),

    # Africa - Central
    "Cameroun": (6.0, 12.0),
    "Centralafrikanske Republik": (7.0, 21.0),
    "Ækvatorialguinea": (1.5, 10.5),
    "Gabon": (-1.0, 12.0),
    "Congo": (-1.0, 15.0),
    "Den Demokratiske Republik Congo": (-3.0, 23.0),
    "Angola": (-12.0, 18.0),
    "São Tomé og Príncipe": (0.5, 6.5),

    # Africa - East
    "Etiopien": (9.0, 39.0),
    "Eritrea": (15.0, 39.0),
    "Djibouti": (11.5, 43.0),
    "Somalia": (6.0, 46.0),
    "Kenya": (1.0, 38.0),
    "Uganda": (1.0, 32.0),
    "Tanzania": (-6.0, 35.0),
    "Rwanda": (-2.0, 30.0),
    "Burundi": (-3.5, 30.0),
    "Malawi": (-13.0, 34.0),
    "Mozambique": (-18.0, 35.0),
    "Zambia": (-15.0, 28.0),
    "Zimbabwe": (-19.0, 29.0),
    "Mauritius": (-20.0, 57.5),
    "Seychellerne": (-4.5, 55.5),
    "Comorerne": (-12.0, 44.0),
    "Madagaskar": (-19.0, 47.0),

    # Africa - South
    "Sydafrika": (-29.0, 25.0),
    "Namibia": (-22.0, 17.0),
    "Botswana": (-22.0, 24.0),
    "Lesotho": (-29.5, 28.5),
    "Eswatini": (-26.5, 31.5),

    # North America
    "USA": (39.0, -98.0),
    "Canada": (56.0, -106.0),
    "Mexico": (23.0, -102.0),

    # Central America
    "Guatemala": (15.5, -90.5),
    "Belize": (17.0, -88.5),
    "Honduras": (15.0, -86.5),
    "El Salvador": (13.8, -89.0),
    "Nicaragua": (13.0, -85.0),
    "Costa Rica": (10.0, -84.0),
    "Panama": (9.0, -80.0),

    # Caribbean
    "Cuba": (22.0, -79.5),
    "Jamaica": (18.0, -77.5),
    "Haiti": (19.0, -72.5),
    "Dominikanske Republik": (19.0, -70.0),
    "Bahamas": (24.0, -76.0),
    "Trinidad og Tobago": (10.5, -61.0),
    "Barbados": (13.0, -59.5),
    "Saint Lucia": (14.0, -61.0),
    "Grenada": (12.0, -61.5),
    "Saint Vincent og Grenadinerne": (13.0, -61.2),
    "Antigua og Barbuda": (17.0, -61.8),
    "Dominica": (15.5, -61.4),
    "Saint Kitts og Nevis": (17.3, -62.7),

    # South America
    "Brasilien": (-10.0, -55.0),
    "Argentina": (-34.0, -64.0),
    "Chile": (-33.0, -71.0),
    "Peru": (-10.0, -76.0),
    "Colombia": (4.0, -72.0),
    "Venezuela": (8.0, -66.0),
    "Ecuador": (-2.0, -78.0),
    "Bolivia": (-17.0, -65.0),
    "Paraguay": (-23.0, -58.0),
    "Uruguay": (-33.0, -56.0),
    "Guyana": (5.0, -59.0),
    "Surinam": (4.0, -56.0),

    # Oceania
    "Australien": (-25.0, 135.0),
    "New Zealand": (-42.0, 174.0),
    "Papua Ny Guinea": (-6.0, 147.0),
    "Fiji": (-18.0, 179.0),
    "Salomonøerne": (-9.0, 160.0),
    "Vanuatu": (-16.0, 167.0),
    "Samoa": (-14.0, -172.0),
    "Tonga": (-21.0, -175.0),
    "Mikronesien": (7.0, 158.0),
    "Palau": (7.5, 134.5),
    "Marshalløerne": (7.0, 171.0),
    "Kiribati": (1.5, -157.0),
    "Nauru": (-0.5, 167.0),
    "Tuvalu": (-8.0, 178.0),
}

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth in km."""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))


class DagensLandSolver:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Origin": "https://dagensland.dk",
            "Referer": "https://dagensland.dk/"
        })
        self.guesses = []
        self.guess_results = []  # Store (country, distance, lat, lng) tuples
        self.neighbors = []  # Countries marked as neighbors

    def guess(self, country: str, date_str: str) -> dict:
        """Make a guess and return the API response."""
        resp = self.session.post(
            "https://dagensland.dk/api/guess",
            json={"guess": country, "date": date_str}
        )
        result = resp.json()

        # Handle unknown country error
        if result.get("error") == "Unknown country":
            return {"unknown": True, "country": country}

        self.guesses.append(country)

        if not result.get("correct"):
            # Use API coordinates for better accuracy
            lat = result.get("lat", COUNTRIES.get(country, (0, 0))[0])
            lng = result.get("lng", COUNTRIES.get(country, (0, 0))[1])
            distance = result.get("distance", 0)
            self.guess_results.append((country, distance, lat, lng))

            if result.get("isNeighbor"):
                self.neighbors.append(country)

        return result

    def _filter_candidates(self, candidates: set) -> set:
        """Filter candidates based on all previous guess distances."""
        if not self.guess_results:
            return candidates

        filtered = set()
        for candidate in candidates:
            if candidate in self.guesses:
                continue

            is_consistent = True
            for guessed_country, reported_dist, api_lat, api_lng in self.guess_results:
                lat2, lon2 = COUNTRIES[candidate]
                # Use API coordinates for the guessed country
                expected_dist = haversine(api_lat, api_lng, lat2, lon2)

                # Very lenient tolerance - API uses border-to-border distance,
                # but we calculate centroid-to-centroid, which can differ greatly
                # for large countries or island nations
                if reported_dist < 100:
                    tolerance = 1500  # Very lenient for close guesses
                elif reported_dist < 500:
                    tolerance = 2000  # Island nations can have large centroid offsets
                elif reported_dist < 1000:
                    tolerance = 2000
                else:
                    tolerance = max(1500, reported_dist * 0.5)

                if abs(expected_dist - reported_dist) > tolerance:
                    is_consistent = False
                    break

            if is_consistent:
                filtered.add(candidate)

        return filtered

    def _pick_best_candidate(self, candidates: set) -> str:
        """Pick the candidate closest to the last reported distance."""
        if not self.guess_results:
            return "Tyskland"  # Central starting point

        last_country, last_dist, last_lat, last_lng = self.guess_results[-1]

        best = None
        best_diff = float('inf')

        for candidate in candidates:
            lat2, lon2 = COUNTRIES[candidate]
            expected = haversine(last_lat, last_lng, lat2, lon2)
            diff = abs(expected - last_dist)
            if diff < best_diff:
                best_diff = diff
                best = candidate

        return best

    def solve(self, date_str: str = None) -> str:
        """Solve the puzzle for the given date."""
        if date_str is None:
            date_str = date.today().isoformat()

        candidates = set(COUNTRIES.keys())
        print(f"Solving for {date_str}...")
        print(f"Total countries: {len(candidates)}\n")

        # Start with Germany for good triangulation
        first_guess = "Tyskland"
        result = self.guess(first_guess, date_str)

        print(f"1. {first_guess}: ", end="")
        if result.get("correct"):
            print("CORRECT!")
            return first_guess

        distance = result.get("distance", 0)
        direction = result.get("direction", "")
        is_neighbor = result.get("isNeighbor", False)
        print(f"{distance} km {direction}" + (" (NEIGHBOR!)" if is_neighbor else ""))

        candidates.discard(first_guess)

        guess_num = 2
        for _ in range(50):  # Max iterations to find answer
            candidates = self._filter_candidates(candidates)

            if not candidates:
                print("\nNo candidates left! The country might not be in our list.")
                break

            print(f"   Remaining candidates: {len(candidates)}")

            next_guess = self._pick_best_candidate(candidates)
            candidates.discard(next_guess)

            result = self.guess(next_guess, date_str)

            # Skip unknown countries silently
            if result.get("unknown"):
                print(f"   (Skipping {next_guess} - not recognized by API)")
                continue

            print(f"{guess_num}. {next_guess}: ", end="")
            if result.get("correct"):
                print("CORRECT!")
                return next_guess

            distance = result.get("distance", 0)
            direction = result.get("direction", "")
            is_neighbor = result.get("isNeighbor", False)
            print(f"{distance} km {direction}" + (" (NEIGHBOR!)" if is_neighbor else ""))
            guess_num += 1

            if guess_num > 20:
                print("\nMax guesses reached.")
                break

        return None


def main():
    solver = DagensLandSolver()
    answer = solver.solve()

    print(f"\n{'='*40}")
    if answer:
        print(f"Found: {answer} in {len(solver.guesses)} guesses")
    else:
        print(f"Could not find answer after {len(solver.guesses)} guesses")
    print(f"Guesses: {', '.join(solver.guesses)}")


if __name__ == "__main__":
    main()
