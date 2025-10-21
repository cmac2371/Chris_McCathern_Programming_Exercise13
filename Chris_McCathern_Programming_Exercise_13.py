import sqlite3
import matplotlib.pyplot as plt
import random

# ---------- 1. Create the database ----------
def create_database(initials):
    """Create SQLite database with a population table."""
    db_name = f"population_{initials}.db"
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS population (
            city TEXT,
            year INTEGER,
            population INTEGER,
            PRIMARY KEY (city, year)
        )
    ''')
    conn.commit()
    return conn


# ---------- 2. Insert 2023 data ----------
def insert_2023_data(conn):
    """Insert 10 Florida cities with 2023 population data."""
    cities = {
        "Jacksonville": 985000,
        "Miami": 451000,
        "Tampa": 398000,
        "Orlando": 317000,
        "St. Petersburg": 261000,
        "Hialeah": 220000,
        "Tallahassee": 202000,
        "Port St. Lucie": 241000,
        "Cape Coral": 216000,
        "Fort Lauderdale": 184000
    }

    cur = conn.cursor()
    for city, pop in cities.items():
        cur.execute("INSERT OR IGNORE INTO population VALUES (?, ?, ?)", (city, 2023, pop))
    conn.commit()


# ---------- 3. Simulate population growth ----------
def simulate_growth(conn):
    """Simulate growth or decline for the next 20 years."""
    cur = conn.cursor()
    cur.execute("SELECT city, population FROM population WHERE year = 2023")
    rows = cur.fetchall()

    for city, pop in rows:
        population = pop
        for year in range(2024, 2044):
            # random yearly growth/decline (-1% to +3%)
            growth_rate = random.uniform(-0.01, 0.03)
            population = int(population * (1 + growth_rate))
            cur.execute("INSERT OR REPLACE INTO population VALUES (?, ?, ?)", (city, year, population))
    conn.commit()


# ---------- 4. Plot one city ----------
def show_city_plot(conn):
    """Ask user for a city and show its population growth."""
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT city FROM population ORDER BY city")
    cities = [row[0] for row in cur.fetchall()]

    print("\nAvailable cities:")
    for c in cities:
        print("-", c)

    choice = input("\nType a city name exactly as shown: ").strip()
    if choice not in cities:
        print("Invalid city — showing first city instead.")
        choice = cities[0]

    cur.execute("SELECT year, population FROM population WHERE city = ? ORDER BY year", (choice,))
    data = cur.fetchall()

    years = [row[0] for row in data]
    pops = [row[1] for row in data]

    plt.figure()
    plt.plot(years, pops, marker='o')
    plt.title(f"Population Growth for {choice}")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ---------- 5. Run everything ----------
def main():
    initials = "CM"  # change to your initials
    conn = create_database(initials)
    insert_2023_data(conn)
    simulate_growth(conn)
    show_city_plot(conn)
    conn.close()


if __name__ == "__main__":
    main()

