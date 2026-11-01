from website_blocker import hosts
from website_blocker.classifier import classify


def test_normalize():
    assert hosts.normalize("https://www.Example.com/path?x=1") == "example.com"
    assert hosts.normalize("youtube.com") == "youtube.com"


def test_block_unblock(tmp_path):
    f = tmp_path / "hosts"
    f.write_text("127.0.0.1 localhost\n")
    hosts.block(["https://www.facebook.com", "twitter.com"], str(f))
    assert hosts.get_blocked(str(f)) == ["facebook.com", "twitter.com"]
    hosts.unblock(["facebook.com"], str(f))
    assert hosts.get_blocked(str(f)) == ["twitter.com"]
    assert "localhost" in f.read_text()  # original lines untouched


def test_classifier():
    text = "Join the casino! Betting jackpot slots and poker wager here"
    matched, _ = classify(text, threshold=3)
    assert matched[0][0] == "gambling"
