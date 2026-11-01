# Python Website Blocker

A command-line tool that blocks websites by redirecting them to `127.0.0.1` in your system hosts file. It can also **scrape** a page and use **pattern recognition** (keyword scoring) to detect whether it belongs to a category you want blocked (social, gaming, gambling, video, shopping, adult).

## Features
- Block / unblock websites from user input
- Scrape page title, meta tags, headings and body text (requests + BeautifulSoup)
- Pattern-based category detection with an adjustable threshold
- Auto-block sites that match chosen categories
- Safe edits: only touches its own marked block in the hosts file, makes a one-time `.bak` backup

## Setup
```bash
git clone <your-repo-url>
cd python-website-blocker
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
Editing the hosts file needs admin rights: use `sudo` (Linux/macOS) or an Administrator terminal (Windows).

```bash
sudo python main.py block facebook.com https://www.twitter.com
sudo python main.py list
sudo python main.py unblock facebook.com
sudo python main.py clear

# scrape + detect (scanning alone needs no admin)
python main.py scan example.com
sudo python main.py scan somesite.com -c gambling social --block
```

## How it works
1. `hosts.py` cleans input into a bare domain and writes `127.0.0.1 domain` lines between start/end markers in the hosts file.
2. `scraper.py` downloads a page and extracts readable text.
3. `classifier.py` counts keyword-pattern matches per category; categories at or above the threshold are flagged.
4. `cli.py` ties these together with `argparse`.

## Tests
```bash
pytest
```

## Ideas to extend
- Replace keyword scoring with a scikit-learn TF-IDF + Naive Bayes classifier trained on labelled pages
- Add a schedule (e.g. block only 9am-5pm)
- Add a small GUI with Tkinter

## Disclaimer
Browsers with DNS-over-HTTPS or VPNs can bypass hosts-file blocking. Learning project.
