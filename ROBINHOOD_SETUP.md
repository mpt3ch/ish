# Robinhood Integration for ish

This guide explains how to set up and use the Robinhood trading CLI tool within the ish Linux shell environment on iOS.

## Overview

The `robinhood-cli.py` tool provides a command-line interface for interacting with your Robinhood trading account directly from the ish shell. You can check stock quotes, view your portfolio, place orders, and manage your account—all from your iOS device.

## Prerequisites

- ish Linux shell environment installed on your iOS device
- Python 3.6 or later
- pip package manager
- Active Robinhood account

## Installation

### Step 1: Install Python Dependencies

First, ensure you have Python and pip available in your ish environment. Alpine Linux (used by ish) includes these by default:

```bash
# Update package manager (optional but recommended)
apk update

# Install Python and pip if not already present
apk add python3 py3-pip

# Install robin_stocks library
pip install robin_stocks
```

### Step 2: Set Up the CLI Tool

```bash
# Copy the tool to a location in your PATH
cp tools/robinhood-cli.py ~/.local/bin/robinhood-cli
chmod +x ~/.local/bin/robinhood-cli

# Or create a symlink
ln -s /path/to/tools/robinhood-cli.py ~/.local/bin/robinhood-cli
```

If `~/.local/bin` is not in your PATH, you can add it:

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.profile
source ~/.profile
```

## Quick Start

### 1. Login to Your Account

```bash
robinhood-cli login
```

You'll be prompted for your username (email) and password. Your credentials are handled securely by the robin_stocks library.

To login non-interactively:

```bash
robinhood-cli login --username your@email.com --password yourpassword
```

### 2. Get Stock Quotes

```bash
robinhood-cli quote AAPL
robinhood-cli quote GOOGL
robinhood-cli quote TSLA
```

Output example:
```
Quote for AAPL:
  Price:        $150.45
  Bid:          $150.42
  Ask:          $150.48
  High:         $151.20
  Low:          $149.80
  Previous:     $150.12
  Volume:       45672389
```

### 3. View Your Portfolio

```bash
robinhood-cli portfolio
```

Shows all your positions with current values:
```
Portfolio:
Symbol     Quantity   Value        Cost        
--------------------------------------------
AAPL       10         $1504.50     $1500.00    
GOOGL      5          $7250.75     $7200.00    
TSLA       2          $378.90      $400.00     
--------------------------------------------
TOTAL                 $9134.15     $9100.00
```

### 4. View Account Information

```bash
robinhood-cli account
```

Shows account details and buying power.

### 5. Place Orders

**Buy shares (market order):**
```bash
robinhood-cli buy AAPL 10
```

**Sell shares (market order):**
```bash
robinhood-cli sell AAPL 5
```

### 6. View Recent Orders

```bash
robinhood-cli orders
```

Shows your last 10 orders with their status.

### 7. Logout

```bash
robinhood-cli logout
```

## Complete Command Reference

```
robinhood-cli login [--username EMAIL] [--password PASSWORD]
    Login to your Robinhood account

robinhood-cli logout
    Logout from your account

robinhood-cli quote SYMBOL
    Get current stock quote for a symbol (e.g., AAPL, GOOGL)

robinhood-cli portfolio
    Display all your current positions and their values

robinhood-cli account
    Show account information and buying power

robinhood-cli buy SYMBOL QUANTITY [--price LIMIT_PRICE]
    Buy shares of a stock
    If --price is specified, places a limit order; otherwise places a market order

robinhood-cli sell SYMBOL QUANTITY [--price LIMIT_PRICE]
    Sell shares of a stock
    If --price is specified, places a limit order; otherwise places a market order

robinhood-cli orders
    View your 10 most recent orders and their statuses

robinhood-cli --version
    Show version information

robinhood-cli --help
    Show help message
```

## Advanced Usage

### Scripting and Automation

You can use the tool in shell scripts to automate trading workflows:

```bash
#!/bin/sh
# daily-portfolio-check.sh

echo "Daily Portfolio Check"
echo "====================="
robinhood-cli portfolio
echo ""
echo "Stock Prices"
echo "============"
robinhood-cli quote AAPL
robinhood-cli quote GOOGL
robinhood-cli quote MSFT
```

Run with: `sh daily-portfolio-check.sh`

### Piping Data

Get quote data and process with other commands:

```bash
# Get quotes and check for prices above $150
robinhood-cli quote AAPL | grep "Price"
```

## Configuration

The tool stores configuration and session data in:

```
~/.robinhood/
├── config.json       (user configuration)
└── .auth_token       (authentication state)
```

**Important**: Keep these files private. They may contain sensitive authentication data.

## Troubleshooting

### "robin_stocks module not found"

Install the required package:
```bash
pip install robin_stocks
```

### "Not authenticated. Run 'login' first."

You need to login before using most commands:
```bash
robinhood-cli login
```

### Login fails with incorrect credentials

Ensure you're using the correct email and password. If you use Robinhood's web interface, use the same credentials there.

### Order placement fails

- Ensure you have sufficient buying power
- Check that the market is open (orders during market hours work better)
- Verify the stock symbol is correct

### Performance Issues

On slower iOS devices, some operations may take time:
- Stock quotes typically load in 2-5 seconds
- Portfolio data may take 5-10 seconds
- Be patient while waiting for order confirmations

## Security Notes

- **Don't share your password**: Never commit password in scripts
- **Use environment variables for automation**:
  ```bash
  export ROBINHOOD_USER="your@email.com"
  export ROBINHOOD_PASS="yourpassword"
  robinhood-cli login --username $ROBINHOOD_USER --password $ROBINHOOD_PASS
  ```
- **Keep ~/.robinhood private**: This directory contains authentication tokens
  ```bash
  chmod 700 ~/.robinhood
  ```

## Limitations

- **Market hours**: Some features work better during market hours
- **Rate limiting**: Robinhood API has rate limits; don't make excessive requests
- **Order types**: Currently supports market orders; limit orders available via --price flag
- **Real-time data**: Quotes may have slight delays

## Support

For issues or questions:

1. Check the [Robinhood API documentation](https://github.com/jmfernandes/robin_stocks)
2. Review this guide's troubleshooting section
3. Check ish documentation at [ish.app](https://ish.app) or [GitHub wiki](https://github.com/ish-app/ish/wiki)

## License

This integration tool is provided as part of the ish project. See LICENSE.md for details.

## Disclaimer

Trading stocks involves risk. This tool is provided as-is for educational and operational purposes. Always:

- Do your own research before trading
- Understand the risks involved
- Test with small amounts first
- Monitor your positions regularly
- Be aware of tax implications

Neither this tool nor ish makes any warranties about trading results or market data accuracy.
