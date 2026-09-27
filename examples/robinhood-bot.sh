#!/bin/sh
# Example: Robinhood CLI - Simple Trading Bot
# This script demonstrates a basic automated trading pattern

# Configuration (set these before running)
WATCHLIST="AAPL MSFT GOOGL TSLA"
LOG_FILE="$HOME/.robinhood/trading.log"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# Initialize log file
log_message "========================================="
log_message "Robinhood CLI Trading Bot Started"
log_message "========================================="

# Check if authenticated
if ! robinhood-cli account > /dev/null 2>&1; then
    log_message "ERROR: Not authenticated. Please run 'robinhood-cli login' first."
    exit 1
fi

log_message "✓ Authentication verified"

# Scan watchlist and report prices
log_message ""
log_message "Scanning watchlist..."
for symbol in $WATCHLIST; do
    log_message "Checking $symbol..."
    robinhood-cli quote "$symbol" >> "$LOG_FILE"
done

# Get portfolio summary
log_message ""
log_message "Current Portfolio:"
robinhood-cli portfolio >> "$LOG_FILE"

# Get recent orders
log_message ""
log_message "Recent Orders:"
robinhood-cli orders >> "$LOG_FILE"

log_message ""
log_message "Bot run completed successfully"
log_message "Log saved to: $LOG_FILE"
