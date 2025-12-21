# 🚀 Nepal IPO Alert System

**Automated IPO tracking and desktop notifications for the Nepal Stock Market.**

---

## 📝 The Problem
Tracking upcoming IPOs on portals like Merolagani can be a hassle.  
It’s easy to forget to check the website, and missing an IPO deadline means missing out on potential investment opportunities.  

Sometimes the news is buried in paragraphs, and other times it's in structured tables—making manual tracking inconsistent and time-consuming.

---

## ✅ The Solution
This Python script automates the entire process.  
It acts as a **hybrid scraper** that:
- Extracts IPO data from both news text and tables  
- Calculates deadlines using Nepali date logic  
- Triggers **desktop popup reminders** so you never miss an issue again

---

## 🛠️ Step-by-Step Installation Guide

### Step 1: Folder Preparation
1. Open your C: Drive  
2. Create a new folder named `Scripts` (Full Path: `C:\Scripts`)  
3. Save the Python script as `ipo_reminder.py` inside this folder  

### Step 2: Install Required Libraries
Open your Command Prompt (CMD) and run:

```bash
pip install requests beautifulsoup4 nepali-datetime
```
## 🛠️ Step 3: Setting Up Windows Task Scheduler

To make the script run automatically every day at 2:35 PM:

1. **Create Task**: Open Task Scheduler → Click "Create Task" (not Basic Task)

2. **General Tab**:
   - Name: `Nepal_IPO_Alert`
   - Check "Run with highest privileges"
   - Check "Run only when user is logged on" (Required for popup window)

3. **Triggers Tab**:
   - Click "New" → Set to Daily at 2:35 PM

4. **Actions Tab**:
   - Click "New" → Start a program
   - **Program/script**: `python.exe`
   - **Add arguments**: `"C:\Scripts\ipo_reminder.py"`
   - **Start in**: `C:\Scripts`

5. **Conditions Tab**:
   - Uncheck "Start the task only if the computer is on AC power"

6. **Settings Tab**:
   - Check "Run task as soon as possible after a scheduled start is missed"
   - Check "Stop the task if it runs longer than 1 hour"
   - Check "If the task fails, restart every 1 hour"

---

## ⚙️ How it Works

- **Hybrid Scanning**: Uses BeautifulSoup and Regex to find IPO details even if hidden in news paragraphs or non-standard table formats
- **Memory (JSON)**: Creates `ipo_history.json` in the folder to remember which alerts were already sent. Ensures only **one alert per day per company**

**Alert Logic**:  
- **1 Day Before**: Fund reminder alert (Check your bank balance!)  
- **Opening Day**: "IPO Open" notification  
- **Every 2nd Day**: Mid-issue reminders to keep it on your radar  
- **Closing Day**: "Last Call" urgent alert

---

## 🖥️ Technologies Used

- Python 3.x  
- BeautifulSoup4 (Web Scraping)  
- Tkinter (Desktop UI)  
- Regex (Advanced Pattern Matching)  
- Windows Task Scheduler (Automation)
