"""
================================================================================
  Project Title  : Stock Portfolio Tracker
  Author         : [Your Name]
  Description    : A command-line stock portfolio tracker that lets users build
                   a portfolio from hardcoded stock prices, calculates individual
                   and total investments, displays results in a formatted table,
                   and optionally saves the portfolio to TXT and CSV files.
  Python Version : 3.8+
  Features       :
      - Hardcoded stock price dictionary (no internet required)
      - Case-insensitive stock name input
      - Full input validation (stock name, quantity, yes/no prompts)
      - Neat tabular console output with separators
      - Portfolio saving to portfolio.txt and portfolio.csv with timestamps
      - Continuous operation until the user chooses to exit
================================================================================
"""
import csv
from datetime import datetime
from typing import List, Dict, Set


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 350,
    "AMZN": 160,
    "NFLX": 450,
    "META": 320,
}

SEPARATOR = "=" * 62
THIN_SEP  = "-" * 62
TITLE_ART = r"""
  ╔═══════════════════════════════════════════════════════════╗
  ║            STOCK  PORTFOLIO  TRACKER                     ║
  ╚═══════════════════════════════════════════════════════════╝
"""


# ──────────────────────────────────────────────────────────────────────────────
# Helper utilities
# ──────────────────────────────────────────────────────────────────────────────

def get_timestamp() -> str:
    """Return current date-time as a human-readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_positive_integer(prompt: str) -> int:
    """Keep asking until the user provides a positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("  ⚠  Please enter a positive integer (> 0).")
                continue
            return value
        except ValueError:
            print("  ⚠  Invalid input. Please enter a whole number.")


def ask_yes_no(prompt: str) -> bool:
    """Ask a yes / no question and return True for yes, False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  ⚠  Please enter 'y' or 'n'.")


# ──────────────────────────────────────────────────────────────────────────────
# Core functions
# ──────────────────────────────────────────────────────────────────────────────

def display_available_stocks() -> None:
    """Print all available stocks and their prices in a formatted table."""
    print(SEPARATOR)
    print("  AVAILABLE STOCKS")
    print(SEPARATOR)
    print(f"  {'Symbol':<10} {'Price (USD)':>12}")
    print(THIN_SEP)
    for symbol, price in STOCK_PRICES.items():
        print(f"  {symbol:<10} ${price:>10,.2f}")
    print(SEPARATOR)
    print()


def get_stock_input() -> List[Dict]:
    """
    Interactively collect stock names and quantities from the user.

    Returns a list of dicts:
        [{"symbol": "AAPL", "price": 180, "quantity": 5}, ...]
    """
    num_stocks = get_positive_integer(
        "  How many different stocks do you own? "
    )
    print()

    portfolio: List[Dict] = []

    for i in range(1, num_stocks + 1):
        print(f"  --- Stock #{i} ---")

        # Validate stock name
        while True:
            symbol = input("  Enter stock symbol: ").strip().upper()
            if symbol in STOCK_PRICES:
                break
            print(f"  ⚠  '{symbol}' is not a valid stock.")
            print(f"      Available: {', '.join(STOCK_PRICES.keys())}")
            print()

        # Validate quantity
        quantity = get_positive_integer("  Enter quantity owned : ")

        portfolio.append({
            "symbol": symbol,
            "price": STOCK_PRICES[symbol],
            "quantity": quantity,
        })
        print()

    return portfolio


def calculate_portfolio(portfolio: List[Dict]) -> Dict:
    """
    Given the raw portfolio list, compute derived metrics.

    Returns a dict with:
        - items            : list of dicts with an added 'investment' key
        - total_investment : float
        - total_stocks     : int   (sum of all quantities)
        - num_companies    : int   (distinct stock symbols)
    """
    total_investment = 0
    total_stocks = 0
    companies: Set[str] = set()

    for entry in portfolio:
        investment = entry["price"] * entry["quantity"]
        entry["investment"] = investment
        total_investment += investment
        total_stocks += entry["quantity"]
        companies.add(entry["symbol"])

    return {
        "items": portfolio,
        "total_investment": total_investment,
        "total_stocks": total_stocks,
        "num_companies": len(companies),
    }


def display_portfolio(result: dict) -> None:
    """Print a formatted portfolio summary to the console."""
    items = result["items"]
    total_investment = result["total_investment"]
    total_stocks = result["total_stocks"]
    num_companies = result["num_companies"]

    print()
    print(SEPARATOR)
    print("  YOUR PORTFOLIO SUMMARY")
    print(SEPARATOR)
    header = (
        f"  {'Stock':<10} {'Price':>10} {'Qty':>8} {'Investment':>14}"
    )
    print(header)
    print(THIN_SEP)

    for item in items:
        print(
            f"  {item['symbol']:<10} "
            f"${item['price']:>9,.2f} "
            f"{item['quantity']:>7} "
            f"${item['investment']:>13,.2f}"
        )

    print(SEPARATOR)
    print(f"  {'Total Investment':<30} ${total_investment:>13,.2f}")
    print(f"  {'Total Number of Stocks':<30} {total_stocks:>14}")
    print(f"  {'Different Companies':<30} {num_companies:>14}")
    print(SEPARATOR)
    print()


# ──────────────────────────────────────────────────────────────────────────────
# File-saving functions
# ──────────────────────────────────────────────────────────────────────────────

def save_to_txt(result: dict, filepath: str = "portfolio.txt") -> None:
    """Save the portfolio summary to a plain-text file."""
    timestamp = get_timestamp()
    items = result["items"]
    total_investment = result["total_investment"]
    total_stocks = result["total_stocks"]
    num_companies = result["num_companies"]

    lines: List[str] = [
        SEPARATOR,
        "  STOCK PORTFOLIO REPORT",
        SEPARATOR,
        f"  Generated on: {timestamp}",
        SEPARATOR,
        "",
        f"  {'Stock':<10} {'Price':>10} {'Qty':>8} {'Investment':>14}",
        THIN_SEP,
    ]

    for item in items:
        lines.append(
            f"  {item['symbol']:<10} "
            f"${item['price']:>9,.2f} "
            f"{item['quantity']:>7} "
            f"${item['investment']:>13,.2f}"
        )

    lines += [
        SEPARATOR,
        f"  {'Total Investment':<30} ${total_investment:>13,.2f}",
        f"  {'Total Number of Stocks':<30} {total_stocks:>14}",
        f"  {'Different Companies':<30} {num_companies:>14}",
        SEPARATOR,
    ]

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def save_to_csv(result: dict, filepath: str = "portfolio.csv") -> None:
    """Save the portfolio data to a CSV file with a timestamp header."""
    timestamp = get_timestamp()
    items = result["items"]
    total_investment = result["total_investment"]
    total_stocks = result["total_stocks"]
    num_companies = result["num_companies"]

    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Stock Portfolio Report"])
        writer.writerow([f"Generated on: {timestamp}"])
        writer.writerow([])  # blank row
        writer.writerow(["Stock", "Price (USD)", "Quantity", "Investment (USD)"])

        for item in items:
            writer.writerow([
                item["symbol"],
                f"{item['price']:.2f}",
                item["quantity"],
                f"{item['investment']:.2f}",
            ])

        writer.writerow([])  # blank row
        writer.writerow(["Total Investment", f"{total_investment:.2f}"])
        writer.writerow(["Total Stocks", total_stocks])
        writer.writerow(["Different Companies", num_companies])


def save_portfolio(result: dict) -> None:
    """Prompt the user and, if confirmed, save to both TXT and CSV."""
    if ask_yes_no("  Would you like to save your portfolio? (y/n): "):
        try:
            save_to_txt(result)
            save_to_csv(result)
            print()
            print("  ✔  Portfolio saved successfully!")
            print("      → portfolio.txt")
            print("      → portfolio.csv")
        except OSError as err:
            print(f"  ✖  Error saving files: {err}")
    else:
        print("  Portfolio was not saved.")
    print()


# ──────────────────────────────────────────────────────────────────────────────
# Main application loop
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point — runs the tracker in a loop until the user exits."""
    print(TITLE_ART)

    while True:
        # 1. Show available stocks
        display_available_stocks()

        # 2. Collect user input
        portfolio = get_stock_input()

        # 3. Calculate investments
        result = calculate_portfolio(portfolio)

        # 4. Display summary
        display_portfolio(result)

        # 5. Offer to save
        save_portfolio(result)

        # 6. Continue or exit
        if not ask_yes_no("  Would you like to track another portfolio? (y/n): "):
            break
        print("\n")

    print()
    print(SEPARATOR)
    print("  Thank you for using the Stock Portfolio Tracker.")
    print(SEPARATOR)
    print()


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
