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
HISTORY_FILE = os.path.join(FOLDER_PATH, "ipo_history.json")

# Full Nepali Month Mapping for 100% Accuracy
NEP_MONTHS = {
    'Baishakh': 1, 'Jestha': 2, 'Ashadh': 3, 'Shrawan': 4,
    'Bhadra': 5, 'Ashwin': 6, 'Kartik': 7, 'Mangsir': 8,
    'Poush': 9, 'Magh': 10, 'Falgun': 11, 'Chaitra': 12
}

def extract_dates_from_text(text):
    """Universal date extractor for Nepali formats in news text."""
    pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s*-\s*(\d{1,2})(?:st|nd|rd|th)?\s*([a-zA-Z]+),\s*(\d{4})'
    match = re.search(pattern, text)
    if match:
        s_day, e_day, m_name, year = match.group(1), match.group(2), match.group(3).capitalize(), match.group(4)
        m_num = NEP_MONTHS.get(m_name)
        if m_num:
            # Conversion to standard AD dates for math
            start_ad = nepali_datetime.date(int(year), m_num, int(s_day)).to_datetime_date()
            end_ad = nepali_datetime.date(int(year), m_num, int(e_day)).to_datetime_date()
            return start_ad, end_ad
    return None, None

def show_popup(title, message, color="#e6f7ff"):
    root = tk.Tk()
    root.withdraw()
    top = tk.Toplevel(root)
    top.title("Nepal IPO Alert System")
    top.attributes('-topmost', True)
    top.configure(bg=color)
    top.geometry("450x250+500+300")
    
    tk.Label(top, text=title, font=("Arial", 12, "bold"), bg=color, wraplength=400).pack(pady=15)
    tk.Label(top, text=message, font=("Arial", 10), bg=color, wraplength=400).pack(pady=10)
    tk.Button(top, text="Close", command=root.destroy, width=15).pack(pady=20)
    root.mainloop()

def check_ipos():
    print(f"--- SCRAPER STARTED: {datetime.date.today()} ---")
    today = datetime.date.today()
    
    if not os.path.exists(FOLDER_PATH): os.makedirs(FOLDER_PATH)
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f: history = json.load(f)
        except: history = {}
    else: history = {}

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. SCAN TEXT (News Items)
        # This catches "Company X is going to issue shares on 7th - 11th Poush, 2082"
        page_text = soup.get_text()
        announcements = re.findall(r'([A-Z][a-zA-Z\s]+Limited).*?(\d+.*?208\d)', page_text)
        
        for company, date_str in announcements:
            company = company.strip()
            open_date, close_date = extract_dates_from_text(date_str)
            if open_date and close_date:
                process_logic(company, open_date, close_date, today, history)

        # 2. SCAN TABLE (Standard Listings)
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 4:
                    comp_name = cols[0].text.strip()
                    # If table contains AD dates (YYYY/MM/DD), parse them here:
                    try:
                        raw_open = cols[3].text.strip().split(' ')[0]
                        open_ad = datetime.datetime.strptime(raw_open, "%Y/%m/%d").date()
                        # Assuming table logic for close date or range
                        process_logic(comp_name, open_ad, open_ad + datetime.timedelta(days=4), today, history)
                    except: continue
                        
    except Exception as e:
        print(f"Error: {e}")

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)
    print("--- SCRAPER FINISHED ---")

def process_logic(name, open_date, close_date, today, history):
    diff_open = (open_date - today).days
    diff_close = (close_date - today).days
    
    # --- MULTI-STAGE ALERT LOGIC ---
    if diff_open == 1:
        trigger_alert(name, "PRE", f"💰 FUND ALERT: {name}", "IPO opens tomorrow! Check your balance.", "#fff4cc", history)
    elif diff_open == 0:
        trigger_alert(name, "OPEN", f"🚀 IPO OPEN: {name}", "It's opening day! Apply now.", "#e6f7ff", history)
    elif diff_close == 0:
        trigger_alert(name, "LAST", f"⚠️ LAST DAY: {name}", "FINAL chance to apply today!", "#ffcccc", history)
    elif open_date < today < close_date:
        days_active = (today - open_date).days
        if days_active % 2 == 0:
            trigger_alert(name, f"ALT_{today}", f"🔔 IPO REMINDER: {name}", f"IPO is still running. {diff_close} days left.", "#e6f7ff", history)

def trigger_alert(name, stage, title, msg, color, history):
    key = f"{name}_{stage}"
    if history.get(key) != str(datetime.date.today()):
        print(f"ALERT TRIGGERED: {title}")
        show_popup(title, msg, color)
        history[key] = str(datetime.date.today())

if __name__ == "__main__":
    check_ipos()