import requests
from bs4 import BeautifulSoup
import datetime
import nepali_datetime
import tkinter as tk
import json
import os
import re

# --- CONFIGURATION ---
URL = "https://merolagani.com/Ipo.aspx?type=upcoming"
FOLDER_PATH = r"C:\Scripts"
# This file stores the IPO details permanently
DATA_FILE = os.path.join(FOLDER_PATH, "ipo_database.json")
# This file tracks which specific daily alerts were already shown
HISTORY_FILE = os.path.join(FOLDER_PATH, "alert_history.json")

NEP_MONTHS = {
    'Baishakh': 1, 'Baisakh': 1, 'Jestha': 2, 'Jeth': 2,
    'Ashadh': 3, 'Asadh': 3, 'Shrawan': 4, 'Sawan': 4, 'Saun': 4,
    'Bhadra': 5, 'Bhadau': 5, 'Ashwin': 6, 'Asoj': 6,
    'Kartik': 7, 'Kattik': 7, 'Mangsir': 8, 'Mangshir': 8,
    'Poush': 9, 'Push': 9, 'Magh': 10, 'Falgun': 11, 'Phagun': 11,
    'Chaitra': 12, 'Chait': 12
}

TARGET_KEYWORDS = ["general public", "public issue", "ordinary share"]
BLOCK_KEYWORDS = ["working abroad", "migrant workers", "project affected", "local residents"]

def extract_dates_from_text(text):
    pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s*(?:\-|to)\s*(\d{1,2})(?:st|nd|rd|th)?\s+([a-zA-Z]+),?\s+(\d{4})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        s_day, e_day, m_name, year = match.group(1), match.group(2), match.group(3).capitalize(), match.group(4)
        m_num = NEP_MONTHS.get(m_name)
        if m_num:
            try:
                start_ad = nepali_datetime.date(int(year), m_num, int(s_day)).to_datetime_date()
                end_ad = nepali_datetime.date(int(year), m_num, int(e_day)).to_datetime_date()
                return str(start_ad), str(end_ad) # Save as strings for JSON
            except: return None, None
    return None, None

def show_popup(title, message, color="#e6f7ff"):
    root = tk.Tk()
    root.withdraw()
    top = tk.Toplevel(root)
    top.title("IPO Alert")
    top.attributes('-topmost', True)
    top.configure(bg=color)
    top.geometry("400x200+500+300")
    tk.Label(top, text=title, font=("Arial", 11, "bold"), bg=color, wraplength=350).pack(pady=10)
    tk.Label(top, text=message, font=("Arial", 10), bg=color, wraplength=350).pack(pady=10)
    tk.Button(top, text="OK", command=root.destroy, width=10).pack(pady=10)
    root.mainloop()

def run_system():
    if not os.path.exists(FOLDER_PATH): os.makedirs(FOLDER_PATH)
    today = datetime.date.today()
    
    # 1. Load existing database and history
    db = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f: db = json.load(f)
    
    history = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f: history = json.load(f)

    # 2. Scrape for NEW information only
    print(f"--- SCRAPING WEB: {today} ---")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for item in soup.find_all(['p', 'div', 'tr']):
            text = item.get_text().strip()
            name_match = re.search(r'([A-Z][a-zA-Z\s\.]+(?:Limited|Company|Bank|Hydropower|Microfinance))', text)
            
            if name_match:
                company = name_match.group(1).strip()
                # Skip if we already have this in our database
                if company in db: continue

                text_lower = text.lower()
                if any(k in text_lower for k in TARGET_KEYWORDS) and not any(k in text_lower for k in BLOCK_KEYWORDS):
                    open_d, close_d = extract_dates_from_text(text)
                    if open_d:
                        db[company] = {"open": open_d, "close": close_d}
                        print(f"🆕 NEW IPO SAVED: {company}")
    except Exception as e:
        print(f"Web access error (using stored data): {e}")

    # 3. Process Reminders from DATABASE (Independent of website)
    print("--- PROCESSING REMINDERS ---")
    updated_db = {}
    for company, dates in db.items():
        open_date = datetime.datetime.strptime(dates['open'], "%Y-%m-%d").date()
        close_date = datetime.datetime.strptime(dates['close'], "%Y-%m-%d").date()

        # If IPO is already over, don't keep it in active database
        if today > close_date:
            print(f"🗑️ REMOVED (Expired): {company}")
            continue
        
        updated_db[company] = dates # Keep in database
        
        diff_open = (open_date - today).days
        diff_close = (close_date - today).days

        # ALERTS LOGIC
        if diff_open == 1:
            trigger(company, "PRE", f"💰 FUND ALERT: {company}", f"Opens tomorrow ({open_date})", "#fff4cc", history, today)
        elif diff_open == 0:
            trigger(company, "OPEN", f"🚀 IPO OPEN: {company}", "Opening day! Apply now.", "#e6f7ff", history, today)
        elif diff_close == 0:
            trigger(company, "LAST", f"⚠️ LAST DAY: {company}", "Final day to apply!", "#ffcccc", history, today)
        elif open_date < today < close_date:
            if (today - open_date).days % 2 == 0:
                trigger(company, f"ALT_{today}", f"🔔 REMINDER: {company}", "IPO still running.", "#e6f7ff", history, today)

    # 4. Save everything back to files
    with open(DATA_FILE, 'w') as f: json.dump(updated_db, f, indent=4)
    with open(HISTORY_FILE, 'w') as f: json.dump(history, f, indent=4)
    print("--- FINISHED ---")

def trigger(name, stage, title, msg, color, history, today):
    key = f"{name}_{stage}"
    if history.get(key) != str(today):
        show_popup(title, msg, color)
        history[key] = str(today)

if __name__ == "__main__":
    run_system()