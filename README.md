> ⚠ **TwitchWatcherPlaywright** is now deprecated. Moved away from browser automation. Here is the [TwitchSniffer](https://github.com/kubikulek231/TwitchSniffer).

# TwitchWatcherPlaywright

- Simple automated tool for watching Twitch streames and collectings drops/chat bonusses
- Using Playwright-Firefox avoiding Twitch API

## Dependencies

- Works on Linux and Windows
- Python 3.11 required
- Uses Playwright, playwright_stealth, keyboard

## Setup
**Update and upgrade**
```bash
sudo apt-get update && sudo apt-get upgrade
```
**Clone this repository**
```bash
git clone https://github.com/kubikulek231/TwitchWatcher/
```
**Install python3.11 and pip**
```bash
sudo apt-get install python3.11
sudo apt-get install pip3
```
**Install all dependencies**
```bash
sudo pip install playwright
sudo playwright install firefox
sudo playwright install-deps firefox
```
**Run the main script**
```bash
sudo python3 main.py
```
