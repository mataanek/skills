#!/usr/bin/env python3
import json, os, sys, datetime, pathlib

health_dir = pathlib.Path("/mnt/c/Users/mataa/iCloudDrive/Documents/Personal/Health")
wiki_file = pathlib.Path.home() / ".hermes" / "wiki" / "health.md"
log_file = pathlib.Path.home() / ".hermes" / "logs" / "health_extract.log"

def log(msg):
    timestamp = datetime.datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(msg, flush=True)

def get_latest_export():
    files = list(health_dir.glob("health_export_*.json"))
    if not files:
        log("No health export files found")
        return None
    latest = max(files, key=lambda f: f.stat().st_mtime)
    return latest

def extract_metrics(json_path, target_date):
    with open(json_path) as f:
        data = json.load(f)
    def get_val(key):
        arr = data.get(key, [])
        for entry in arr:
            if entry.get("date") == target_date:
                return entry.get("value")
        return None
    steps = get_val("stepCount")
    resting_hr = get_val("restingHeartRate")
    weight = get_val("weight")
    return {
        "date": target_date,
        "steps": steps,
        "resting_hr": resting_hr,
        "weight": weight,
    }

def already_logged(wiki_file, date_str):
    if not wiki_file.exists():
        return False
    content = wiki_file.read_text()
    for line in content.splitlines():
        if line.strip().startswith(date_str):
            return True
    return False

def append_to_wiki(wiki_file, metrics):
    date_str = metrics["date"]
    steps = metrics["steps"] if metrics["steps"] is not None else "N/A"
    hr = metrics["resting_hr"] if metrics["resting_hr"] is not None else "N/A"
    weight = metrics["weight"] if metrics["weight"] is not None else "N/A"
    line = f"- {date_str}: Steps: {steps}, Resting HR: {hr} bpm, Weight: {weight} kg\n"
    with open(wiki_file, "a") as f:
        f.write(line)
    log(f"Appended to wiki: {line.strip()}")

def main():
    wiki_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    latest = get_latest_export()
    if not latest:
        log("Exiting: no export file")
        return
    
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    target_date = yesterday.isoformat()
    
    log(f"Processing export {latest.name} for date {target_date}")
    
    if already_logged(wiki_file, target_date):
        log(f"Data for {target_date} already logged, skipping")
        return
    
    metrics = extract_metrics(latest, target_date)
    if all(v is None for v in [metrics["steps"], metrics["resting_hr"], metrics["weight"]]):
        log("No metrics found for target date")
        return
    
    append_to_wiki(wiki_file, metrics)

if __name__ == "__main__":
    main()