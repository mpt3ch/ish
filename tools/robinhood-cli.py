#!/usr/bin/env python3
"""
Robinhood CLI Tool for ish

A command-line interface for interacting with Robinhood trading platform.
Designed to work within the ish Linux shell environment on iOS.

Usage:
    robinhood-cli.py login [--username USERNAME] [--password PASSWORD]
    robinhood-cli.py logout
    robinhood-cli.py quote SYMBOL
    robinhood-cli.py portfolio
    robinhood-cli.py account
    robinhood-cli.py buy SYMBOL QUANTITY [--price LIMIT_PRICE]
    robinhood-cli.py sell SYMBOL QUANTITY [--price LIMIT_PRICE]
    robinhood-cli.py orders
    robinhood-cli.py --version
    robinhood-cli.py --help
"""

import sys
import os
import json
import argparse
import getpass
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import robin_stocks.robinhood as rh
except ImportError:
    print("Error: robin_stocks module not found.", file=sys.stderr)
    print("Install it with: pip install robin_stocks", file=sys.stderr)
    sys.exit(1)


__version__ = "1.0.0"

# Configuration directory for storing credentials
CONFIG_DIR = Path.home() / ".robinhood"
CONFIG_DIR.mkdir(exist_ok=True)


class RobinhoodCLI:
    """Main CLI handler for Robinhood interactions."""

    def __init__(self):
        """Initialize the Robinhood CLI."""
        self.config_file = CONFIG_DIR / "config.json"
        self.auth_token_file = CONFIG_DIR / ".auth_token"
        self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}", file=sys.stderr)
        return {}

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error: Failed to save config: {e}", file=sys.stderr)

    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return self.auth_token_file.exists() and self.auth_token_file.stat().st_size > 0

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """
        Login to Robinhood account.

        Args:
            username: Optional username (prompts if not provided)
            password: Optional password (prompts if not provided)

        Returns:
            True if login successful, False otherwise
        """
        if not username:
            username = input("Robinhood username (email): ").strip()
            if not username:
                print("Error: Username required", file=sys.stderr)
                return False

        if not password:
            password = getpass.getpass("Password: ")
            if not password:
                print("Error: Password required", file=sys.stderr)
                return False

        try:
            print("Logging in...", file=sys.stderr)
            login_result = rh.login(username, password, store_session=True)
            print("✓ Successfully logged in", file=sys.stderr)
            self.auth_token_file.touch()
            return True
        except Exception as e:
            print(f"Error: Login failed: {e}", file=sys.stderr)
            return False

    def logout(self) -> bool:
        """
        Logout from Robinhood account.

        Returns:
            True if logout successful
        """
        try:
            rh.logout()
            if self.auth_token_file.exists():
                self.auth_token_file.unlink()
            print("✓ Successfully logged out", file=sys.stderr)
            return True
        except Exception as e:
            print(f"Error: Logout failed: {e}", file=sys.stderr)
            return False

    def get_quote(self, symbol: str) -> bool:
        """
        Get stock quote for a symbol.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            True if successful
        """
        if not self.is_authenticated():
            print("Error: Not authenticated. Run 'login' first.", file=sys.stderr)
            return False

        try:
            quote = rh.stocks.get_quotes(symbol)
            if quote:
                q = quote[0]
                print(f"\nQuote for {symbol.upper()}:")
                print(f"  Price:        ${q.get('last_trade_price', 'N/A')}")
                print(f"  Bid:          ${q.get('bid_price', 'N/A')}")
                print(f"  Ask:          ${q.get('ask_price', 'N/A')}")
                print(f"  High:         ${q.get('high_price', 'N/A')}")
                print(f"  Low:          ${q.get('low_price', 'N/A')}")
                print(f"  Previous:     ${q.get('previous_close', 'N/A')}")
                print(f"  Volume:       {q.get('volume', 'N/A')}")
                return True
            else:
                print(f"Error: No quote found for {symbol}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error: Failed to get quote: {e}", file=sys.stderr)
            return False

    def get_portfolio(self) -> bool:
        """
        Display user's portfolio.

        Returns:
            True if successful
        """
        if not self.is_authenticated():
            print("Error: Not authenticated. Run 'login' first.", file=sys.stderr)
            return False

        try:
            positions = rh.account.build_holdings()
            if not positions:
                print("No positions found in portfolio")
                return True

            print("\nPortfolio:")
            print(f"{'Symbol':<10} {'Quantity':<10} {'Value':<12} {'Cost':<12}")
            print("-" * 44)
            total_value = 0
            total_cost = 0

            for symbol, position in positions.items():
                quantity = position.get("quantity", 0)
                price = position.get("average_buy_price", 0)
                cost = float(quantity) * float(price)
                value = position.get("equity", 0)
                total_value += float(value)
                total_cost += cost

                print(f"{symbol:<10} {quantity:<10} ${value:<11.2f} ${cost:<11.2f}")

            print("-" * 44)
            print(f"{'TOTAL':<10} {' ':<10} ${total_value:<11.2f} ${total_cost:<11.2f}")
            return True
        except Exception as e:
            print(f"Error: Failed to get portfolio: {e}", file=sys.stderr)
            return False

    def get_account_info(self) -> bool:
        """
        Display account information.

        Returns:
            True if successful
        """
        if not self.is_authenticated():
            print("Error: Not authenticated. Run 'login' first.", file=sys.stderr)
            return False

        try:
            profile = rh.account.get_account()
            if profile:
                print("\nAccount Information:")
                print(f"  Account Number: {profile.get('account_number', 'N/A')}")
                print(f"  Status:         {profile.get('status', 'N/A')}")
                print(f"  Type:           {profile.get('account_type', 'N/A')}")
                print(f"  Created:        {profile.get('created_at', 'N/A')}")

            equity = rh.account.get_account_profile()
            if equity:
                print(f"  Buying Power:   ${equity.get('cash', 'N/A')}")
                return True
        except Exception as e:
            print(f"Error: Failed to get account info: {e}", file=sys.stderr)
            return False

    def place_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        price: Optional[float] = None,
    ) -> bool:
        """
        Place a buy or sell order.

        Args:
            symbol: Stock ticker symbol
            quantity: Number of shares
            side: 'buy' or 'sell'
            price: Limit price (optional, defaults to market order)

        Returns:
            True if successful
        """
        if not self.is_authenticated():
            print("Error: Not authenticated. Run 'login' first.", file=sys.stderr)
            return False

        try:
            symbol = symbol.upper()
            quantity = int(quantity)

            if quantity <= 0:
                print("Error: Quantity must be positive", file=sys.stderr)
                return False

            order_type = "limit" if price else "market"
            print(
                f"Placing {order_type} {side} order: {quantity} shares of {symbol}",
                file=sys.stderr,
            )

            if side.lower() == "buy":
                order = rh.orders.order_buy_market(
                    symbol, quantity, timeInForce="gfd"
                )
            elif side.lower() == "sell":
                order = rh.orders.order_sell_market(
                    symbol, quantity, timeInForce="gfd"
                )
            else:
                print("Error: Side must be 'buy' or 'sell'", file=sys.stderr)
                return False

            if order:
                print(f"✓ Order placed successfully", file=sys.stderr)
                print(f"Order ID: {order.get('id', 'N/A')}")
                return True
            else:
                print("Error: Failed to place order", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error: Failed to place order: {e}", file=sys.stderr)
            return False

    def get_orders(self) -> bool:
        """
        Display recent orders.

        Returns:
            True if successful
        """
        if not self.is_authenticated():
            print("Error: Not authenticated. Run 'login' first.", file=sys.stderr)
            return False

        try:
            orders = rh.orders.get_all_orders()
            if not orders:
                print("No orders found")
                return True

            print("\nRecent Orders:")
            print(f"{'Created':<20} {'Symbol':<8} {'Type':<6} {'Qty':<6} {'Price':<10} {'State':<10}")
            print("-" * 60)

            for order in orders[:10]:  # Show last 10 orders
                created = order.get("created_at", "N/A")[:10]
                symbol = order.get("symbol", "N/A")
                side = order.get("side", "N/A")[0].upper()
                quantity = order.get("quantity", "N/A")
                price = order.get("price", "N/A")
                state = order.get("state", "N/A")

                print(f"{created:<20} {symbol:<8} {side:<6} {quantity:<6} ${price:<9} {state:<10}")

            return True
        except Exception as e:
            print(f"Error: Failed to get orders: {e}", file=sys.stderr)
            return False


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Robinhood CLI Tool - Trade stocks from the terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Login command
    login_parser = subparsers.add_parser("login", help="Login to Robinhood")
    login_parser.add_argument("--username", help="Username (email)")
    login_parser.add_argument("--password", help="Password (prompted if not provided)")

    # Logout command
    subparsers.add_parser("logout", help="Logout from Robinhood")

    # Quote command
    quote_parser = subparsers.add_parser("quote", help="Get stock quote")
    quote_parser.add_argument("symbol", help="Stock ticker symbol (e.g., AAPL)")

    # Portfolio command
    subparsers.add_parser("portfolio", help="View portfolio")

    # Account command
    subparsers.add_parser("account", help="View account information")

    # Buy command
    buy_parser = subparsers.add_parser("buy", help="Buy shares")
    buy_parser.add_argument("symbol", help="Stock ticker symbol")
    buy_parser.add_argument("quantity", type=int, help="Number of shares")
    buy_parser.add_argument("--price", type=float, help="Limit price (optional)")

    # Sell command
    sell_parser = subparsers.add_parser("sell", help="Sell shares")
    sell_parser.add_argument("symbol", help="Stock ticker symbol")
    sell_parser.add_argument("quantity", type=int, help="Number of shares")
    sell_parser.add_argument("--price", type=float, help="Limit price (optional)")

    # Orders command
    subparsers.add_parser("orders", help="View recent orders")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    cli = RobinhoodCLI()

    if args.command == "login":
        success = cli.login(args.username, args.password)
        return 0 if success else 1
    elif args.command == "logout":
        success = cli.logout()
        return 0 if success else 1
    elif args.command == "quote":
        success = cli.get_quote(args.symbol)
        return 0 if success else 1
    elif args.command == "portfolio":
        success = cli.get_portfolio()
        return 0 if success else 1
    elif args.command == "account":
        success = cli.get_account_info()
        return 0 if success else 1
    elif args.command == "buy":
        success = cli.place_order(args.symbol, args.quantity, "buy", args.price)
        return 0 if success else 1
    elif args.command == "sell":
        success = cli.place_order(args.symbol, args.quantity, "sell", args.price)
        return 0 if success else 1
    elif args.command == "orders":
        success = cli.get_orders()
        return 0 if success else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
