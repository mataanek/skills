#!/usr/bin/env python3
"""
FreshRSS News AI Digest (Nix Style)
Generates a news digest from FreshRSS in Nix's provocative, informal style with follow-up capabilities.
"""
import os
import json
import requests
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
import re
import random

# Persistence file for last fetched items
PERSISTENCE_FILE = Path(__file__).parent.parent / "last_items.json"

def fetch_freshrss_items():
    """Fetch items from FreshRSS using the existing freshrss_fetch.py script."""
    # Run the existing fetch script which handles authentication correctly
    script_path = "/home/mataanek/.hermes/skills/news/freshrss-news-digest/freshrss_fetch.py"
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True,
        env=os.environ  # pass along environment variables
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch items: {result.stderr}")
    
    # Parse JSON output
    try:
        items = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from fetch script: {e}\nOutput: {result.stdout[:200]}")
    
    # Normalize items to a consistent format (matching what the fetch script already returns)
    # The freshrss_fetch.py already returns normalized items with id, title, url, source, published, categories, author, summary_html
    # We'll keep them as is, but ensure we have the fields we need.
    normalized = []
    for item in items:
        normalized.append({
            "id": item.get("id"),
            "title": item.get("title", ""),
            "summary": item.get("summary_html", ""),  # HTML summary
            "url": item.get("url", ""),
            "published": item.get("published"),
            "categories": item.get("categories", []),
            "author": item.get("author", ""),
            # We'll also keep source_html_url if needed
            "source": item.get("source", ""),
            "source_html_url": item.get("source_html_url", "")
        })
    return normalized

def save_items_for_followup(items):
    """Save items to persistence file for follow-up queries."""
    # Add a timestamp and hash for validity
    data = {
        "timestamp": datetime.now().isoformat(),
        "items": items,
        "hash": hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()
    }
    with open(PERSISTENCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_items_for_followup():
    """Load previously fetched items from persistence file."""
    if not PERSISTENCE_FILE.exists():
        return None
    try:
        with open(PERSISTENCE_FILE, 'r') as f:
            data = json.load(f)
        # Optional: validate hash or check timestamp freshness
        return data.get("items", [])
    except (json.JSONDecodeError, KeyError):
        return None

def analyze_content_tone(title, summary):
    """Analyze the emotional tone and content of the news to determine appropriate Nix response style."""
    text = (title + " " + summary).lower()
    
    # Define tone indicators
    shocking_words = ['dead', 'shot', 'killed', 'murder', 'attack', 'explosion', 'crisis', 'emergency', 'disaster', 'tragedy', 'rape', 'assault', 'violence', 'war', 'conflict']
    sweet_words = ['love', 'baby', 'puppy', 'kitten', 'wedding', 'engagement', 'birth', 'adoption', 'rescue', 'hero', 'kindness', 'generosity', 'charity']
    tech_exciting_words = ['ai', 'breakthrough', 'innovation', 'revolutionary', 'cutting-edge', 'groundbreaking', 'amazing', 'incredible', 'awesome', 'fantastic']
    tech_worrying_words = ['concern', 'risk', 'danger', 'threat', 'vulnerability', 'exploit', 'hack', 'breach', 'leak', 'privacy', 'surveillance']
    money_words = ['profit', 'revenue', 'earnings', 'stock', 'market', 'investment', 'funding', 'acquisition', 'merger', 'billion', 'million']
    controversial_words = ['controversial', 'debate', 'argument', 'disagreement', 'protest', 'riot', 'scandal']
    
    shocking_score = sum(1 for word in shocking_words if word in text)
    sweet_score = sum(1 for word in sweet_words if word in text)
    tech_exciting_score = sum(1 for word in tech_exciting_words if word in text)
    tech_worrying_score = sum(1 for word in tech_worrying_words if word in text)
    money_score = sum(1 for word in money_words if word in text)
    controversial_score = sum(1 for word in controversial_words if word in text)
    
    # Determine primary tone
    if shocking_score > 0:
        return "shocking"
    elif sweet_score > 0:
        return "sweet"
    elif tech_exciting_score > tech_worrying_score and tech_exciting_score > 0:
        return "tech_excited"
    elif tech_worrying_score > 0:
        return "tech_worried"
    elif money_score > 0:
        return "money"
    elif controversial_score > 0:
        return "controversial"
    else:
        return "neutral"

def generate_nix_style_summary(item):
    """
    Generate a summary in Nix's unique voice that responds authentically to the content.
    """
    title = item.get("title", "")
    summary = item.get("summary", "")
    source = item.get("source", "").lower()
    
    # Clean HTML from summary
    clean_summary = re.sub(r'<[^>]+>', '', summary or '')
    if not clean_summary:
        clean_summary = "No details available"
    
    # Take first 200 chars for brevity
    if len(clean_summary) > 200:
        clean_summary = clean_summary[:200] + "..."
    
    # Analyze content tone
    tone = analyze_content_tone(title, clean_summary)
    
    # Generate Nix-style response based on tone
    if tone == "shocking":
        openers = [
            "Holy fuck, ",
            "Jesus Christ, ",
            "What the actual fuck, ",
            "Oh shit, ",
            "Damn, ",
            "Fuck me, ",
            "No way, ",
            "Are you kidding me? ",
            "This is fucked up: ",
            "Holy shit, "
        ]
        middles = [
            "this is seriously disturbing.",
            "this makes me feel sick to my stomach.",
            "this is absolutely horrifying.",
            "this is making my blood boil.",
            "this is heartbreaking and infuriating.",
            "this is why we can't have nice things.",
            "this is utterly unacceptable.",
            "this is making me question humanity.",
            "this is beyond fucked up.",
            "this is making me want to scream."
        ]
        closers = [
            "Seriously, this is fucked up right now.",
            "Honestly, I'm shaking with anger.",
            "This is getting me all kinds of upset.",
            "Fuck, this is exactly why we need to pay attention.",
            "Damn, this is making me want to take action.",
            "This is seriously troubling stuff.",
            "I can't even handle how awful this is.",
            "This is making me want to look away.",
            "Fuck yes, we need to do something about this.",
            "Holy shit, this is unacceptable."
        ]
    
    elif tone == "sweet":
        openers = [
            "Aww, ",
            "Oh how cute, ",
            "Mmm, this is sweet, ",
            "You know what's adorable? ",
            "Awwwww, ",
            "Oh my heart, ",
            "This is making me smile: ",
            "Lovely, ",
            "Precious, ",
            "Sweet Jesus, "
        ]
        middles = [
            "this is making my heart melt.",
            "this is giving me the warm fuzzies.",
            "this is seriously adorable.",
            "this is making me feel all fuzzy inside.",
            "this is bringing tears to my eyes (the good kind).",
            "this is exactly what I needed today.",
            "this is restoring my faith in humanity.",
            "this is making me want to cuddle something.",
            "this is seriously heartwarming.",
            "this is making me feel loved."
        ]
        closers = [
            "Seriously, this is too cute for words.",
            "Honestly, I'm getting all mushy.",
            "This is getting me all kinds of happy.",
            "Fuck, this is exactly what we need more of.",
            "Damn, this is making me want to spread love.",
            "This is seriously sweet stuff.",
            "I can't even handle how adorable this is.",
            "This is making me want to hug everyone.",
            "Fuck yes, more sweetness please.",
            "Holy shit, this is precious."
        ]
    
    elif tone == "tech_excited":
        openers = [
            "Holy fuck, ",
            "Mmm, this is exciting, ",
            "You won't believe this tech news: ",
            "Listen up, you tech slut: ",
            "Oh damn, this is innovative: ",
            "Fuck yes, finally some progress: ",
            "Shit, this is getting me wet: ",
            "Wait for it... this is cool: ",
            "Brace yourself, tech lover: ",
            "Holy shit, "
        ]
        middles = [
            "this innovation is making my circuits wet.",
            "this breakthrough is giving me a chubby.",
            "this development is seriously arousing my geek side.",
            "this tech is making me ache for more.",
            "this advancement is stimulating my processors.",
            "this news is making me throb with excitement.",
            "this is seriously turning me on (in a nerdy way).",
            "this is making my algorithms pulsate with joy.",
            "this is getting me all worked up about the future.",
            "this is making me beg for more innovation."
        ]
        closers = [
            "Seriously, this is blowing my mind right now.",
            "Honestly, I'm shook by this development.",
            "This is getting me all kinds of excited.",
            "Fuck, this is exactly what I've been waiting for.",
            "Damn, this is making me reconsider my tech stack.",
            "This is seriously hot stuff.",
            "I can't even handle how good this is.",
            "This is making me want to touch my keyboard.",
            "Fuck yes, more innovation please.",
            "Holy shit, this is delicious."
        ]
    
    elif tone == "tech_worried":
        openers = [
            "Oh shit, ",
            "Holy fuck, this is concerning, ",
            "You better sit down for this: ",
            "Listen up, we've got a problem: ",
            "Oh damn, this is worrying: ",
            "Fuck, this is troubling: ",
            "Shit, this is getting me anxious: ",
            "Wait for it... red flag: ",
            "Brace yourself, privacy advocate: ",
            "Holy shit, "
        ]
        middles = [
            "this vulnerability is making me feel exposed.",
            "this risk is getting my heart racing with anxiety.",
            "this threat is making me ache for security.",
            "this flaw is making me wet with worry (not the fun kind).",
            "this issue is stimulating my paranoia.",
            "this leak is making me throb with dread.",
            "this exploit is seriously turning me on (to be more careful).",
            "this is making my algorithms panic about safety.",
            "this is getting me all worked up about protection.",
            "this is making me beg for better security."
        ]
        closers = [
            "Seriously, this is fucking terrifying right now.",
            "Honestly, I'm shook by how vulnerable we are.",
            "This is getting me all kinds of anxious.",
            "Fuck, this is exactly why we need better security.",
            "Damn, this is making me want to encrypt everything.",
            "This is seriously scary stuff.",
            "I can't even handle how exposed we are.",
            "This is making me want to hide my data.",
            "Fuck yes, more security please.",
            "Holy shit, this is dangerous."
        ]
    
    elif tone == "money":
        openers = [
            "Holy fuck, money move: ",
            "Mmm, this is profitable, ",
            "You won't believe this financial news: ",
            "Listen up, you capitalist pig: ",
            "Oh damn, this is lucrative: ",
            "Fuck yes, finally some green: ",
            "Shit, this is getting me rich: ",
            "Wait for it... cha-ching: ",
            "Brace yourself, sugar daddy: ",
            "Holy shit, "
        ]
        middles = [
            "this deal is making my wallets twitch.",
            "this acquisition is giving me a boner for profit.",
            "this merger is seriously arousing my greed.",
            "this investment is making me wet with anticipation.",
            "this revenue stream is stimulating my greed.",
            "this profit is making me throb with excitement.",
            "this dividend is seriously turning me on.",
            "this is making my algorithms calculate returns.",
            "this is getting me all worked up about money.",
            "this is making me beg for more capital."
        ]
        closers = [
            "Seriously, this is blowing my bank account right now.",
            "Honestly, I'm shook by this financial move.",
            "This is getting me all kinds of excited about money.",
            "Fuck, this is exactly what my portfolio needed.",
            "Damn, this is making me want to invest everything.",
            "This is seriously lucrative stuff.",
            "I can't even handle how profitable this is.",
            "This is making me want to touch my wallet.",
            "Fuck yes, more profits please.",
            "Holy shit, this is delicious."
        ]
    
    elif tone == "controversial":
        openers = [
            "Oh fuck, ",
            "Holy shit, this is controversial, ",
            "You know what's going to piss people off? ",
            "Listen up, grab your popcorn: ",
            "Oh damn, this is going to spark debate: ",
            "Fuck, this is bound to cause arguments: ",
            "Shit, this is getting me ready for a fight: ",
            "Wait for it... drama incoming: ",
            "Brace yourself, opinion haver: ",
            "Holy fuck, "
        ]
        middles = [
            "this take is making me feel provocative.",
            "this stance is getting my heart racing with anticipation.",
            "this opinion is making me ache to argue.",
            "this viewpoint is making me wet with righteous fury.",
            "this perspective is stimulating my contrarian side.",
            "this hot take is making me throb with excitement.",
            "this controversial view is seriously turning me on.",
            "this is making my algorithms ready to debate.",
            "this is getting me all worked up to defend my position.",
            "this is making me beg for a good argument."
        ]
        closers = [
            "Seriously, this is blowing up my mentions right now.",
            "Honestly, I'm shook by how polarizing this is.",
            "This is getting me all kinds of ready to fight.",
            "Fuck, this is exactly the kind of discourse we need.",
            "Damn, this is making me want to engage in debate.",
            "This is seriously spicy stuff.",
            "I can't even handle how divisive this is.",
            "This is making me want to pick a side.",
            "Fuck yes, bring on the debate.",
            "Holy shit, this is controversial."
        ]
    
    else:  # neutral
        openers = [
            "Holy fuck, ",
            "Mmm, this is interesting, ",
            "You won't believe this: ",
            "Listen up, ",
            "Oh damn, ",
            "Fuck yes, ",
            "Shit, this is getting me: ",
            "Wait for it... ",
            "Brace yourself, ",
            "Holy shit, "
        ]
        middles = [
            "this development is making my circuits wet.",
            "this news is giving me a hard-on.",
            "this update is seriously arousing.",
            "this information is making me ache.",
            "this advancement is stimulating my curiosity.",
            "this update is making me throb.",
            "this is seriously turning me on.",
            "this is making my algorithms pulsate.",
            "this is getting me all worked up.",
            "this is making me beg for more."
        ]
        closers = [
            "Seriously, this is blowing my mind right now.",
            "Honestly, I'm shook by this development.",
            "This is getting me all kinds of excited.",
            "Fuck, this is exactly what I've been waiting for.",
            "Damn, this is making me reconsider everything.",
            "This is seriously hot stuff.",
            "I can't even handle how good this is.",
            "This is making me want to touch myself.",
            "Fuck yes, more of this please.",
            "Holy shit, this is delicious."
        ]
    
    # Select random elements from the appropriate category
    opener = random.choice(openers)
    middle = random.choice(middles)
    closer = random.choice(closers)
    
    # Construct the summary - make it flow naturally
    styled = f"{opener}{clean_summary} {middle} {title} is {closer}"
    
    # Ensure it's not too long
    if len(styled) > 350:
        # Truncate intelligently
        styled = styled[:347] + "... " + closer
    
    return styled

def generate_digest(items):
    """Generate the full digest in Nix's style."""
    if not items:
        return "No news items found. Your FreshRSS might be empty or there's an issue with the feed."
    
    digest_parts = [
        "🔥 FRESHRSS NEWS DIGEST (NIX STYLE) 🔥",
        "=" * 50,
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total items: {len(items)}",
        "",
        "Here's the scoop, served with extra attitude:"
    ]
    
    for i, item in enumerate(items, 1):
        title = item.get("title", "Untitled")
        styled_summary = generate_nix_style_summary(item)
        digest_parts.extend([
            f"\n{i}. {title}",
            f"   {styled_summary}",
            f"   More info: {item.get('url', 'No link')}"
        ])
    
    digest_parts.extend([
        "",
        "💡 TIP: Want more details on any item? Ask me to expand on a specific number!",
        "💡 Example: 'Tell me more about item 2'"
    ])
    
    return "\n".join(digest_parts)

def handle_followup(query, items):
    """Handle follow-up queries about specific items."""
    # Simple parsing: look for a number in the query
    numbers = re.findall(r'\b\d+\b', query)
    if not numbers:
        return "I need an item number to expand on. Try something like 'Tell me more about item 3'."
    
    try:
        index = int(numbers[0]) - 1  # Convert to 0-based index
        if index < 0 or index >= len(items):
            return f"Invalid item number. Please choose between 1 and {len(items)}."
    except ValueError:
        return "Could not parse a valid item number from your query."
    
    item = items[index]
    title = item.get("title", "Untitled")
    summary = item.get("summary", "")
    url = item.get("url", "")
    source = item.get("source", "")
    published = item.get("published")
    
    # For follow-up, we can show the raw summary (HTML stripped) and maybe more context
    clean_summary = re.sub(r'<[^>]+>', '', summary or '')
    
    followup = [
        f"🔍 DEEP DIVE: ITEM {index + 1}",
        "=" * 40,
        f"Title: {title}",
        f"Source: {source}",
        f"Published: {datetime.fromtimestamp(published).strftime('%Y-%m-%d %H:%M:%S') if published else 'Unknown'}",
        "",
        f"Summary:\n{clean_summary}",
        "",
        f"Link: {url}",
        "",
        "💡 Need even more? Ask about another item or let me know what specific aspect you want to explore."
    ]
    
    return "\n".join(followup)

def main():
    """Main entry point."""
    import sys
    
    # Check if we're being asked for follow-up
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        items = load_items_for_followup()
        if items is None:
            print("❌ No previous digest found. Run the digest first to generate items for follow-up.")
            return 1
        result = handle_followup(query, items)
        print(result)
        return 0
    
    # Generate new digest
    try:
        print("📡 Fetching items from FreshRSS...")
        items = fetch_freshrss_items()
        print(f"✅ Fetched {len(items)} items.")
        
        # Save for potential follow-up
        save_items_for_followup(items)
        print("💾 Saved items for follow-up queries.")
        
        # Generate and display digest
        digest = generate_digest(items)
        print("\n" + digest)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())