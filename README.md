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
### Important Notes Before Running the Script

1. **Initial Run**: Run the script once to check if it works correctly.  
   - If any issues occur, troubleshoot and resolve them using AI or other tools before proceeding to the next step.

2. **JSON File Handling**:  
   - Each time you make changes to the code or run it for testing, **delete the `alert_history.json` and `ipo_database.json` file** before running the script.  
   - This ensures that old alert history does not interfere with testing.  
   
3. **Remember that both JSON files will only appear after you run the code for the first time.**

3. **After Successful Run**:  
   - Once the script runs correctly and alerts are working as expected, **do not delete any of the JSON files**.  
   - Leave it as is and continue with the next steps.

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
   - **Program/script**: `cmd.exe`
   - **Add arguments**: `"/c python "C:\Scripts\ipo_reminder.py"`
   - **Start in**: `C:\Scripts`

5. **Conditions Tab**:
   - Uncheck "Start the task only if the computer is on AC power"

6. **Settings Tab**:
   - Check "Run task as soon as possible after a scheduled start is missed"
   - Check "Stop the task if it runs longer than 1 hour"
   - Check "If the task fails, restart every 1 hour"

---

### ✅ Final Testing (Recommended)

To confirm that everything is working correctly:

1. Go to the `C:\Scripts` folder and **delete the both `alert_history.json` and `ipo_database.json` files**.
2. Open **Windows Task Scheduler**.
3. Edit the existing task (`Nepal_IPO_Alert`).
4. In the **Triggers** tab, temporarily change the scheduled time to **2 minutes ahead of the current time on your PC**.
5. Save the task and wait.

If the setup is correct, you should receive a **desktop popup notification** within a few minutes.

Once the test is successful:
- Change the trigger time back to your preferred schedule.
- Do **not** delete any of the JSON files again.


## ⚙️ How It Works

- **Hybrid Scanning**  
  Uses **Requests**, **BeautifulSoup**, and **Regex** together to detect IPO details even when they appear inside news paragraphs, mixed text, or non-standard layouts (not just clean tables).

- **Persistent Memory (JSON)**  
  Maintains two local files:
  - `ipo_database.json` → stores active IPO opening and closing dates  
  - `alert_history.json` → records which alerts were already shown  
  This ensures **each alert is triggered only once per day per company**, even if the script runs multiple times.

- **Alert Logic**
  - **1 Day Before Opening** → 💰 *Fund Reminder* (prepare bank balance)
  - **Opening Day** → 🚀 *IPO Open* notification
  - **Every 2nd Day During Issue** → 🔔 *Mid-issue reminder* while IPO is still open
  - **Closing Day** → ⚠️ *Last Day* urgent alert

- **Automation**  
  The script is scheduled using **Windows Task Scheduler** to run daily without manual execution.

---

## 🖥️ Technologies Used

- **Python 3.x**  
  Core programming language used for the entire system.

- **Requests**  
  Fetches IPO data from the Merolagani website.

- **BeautifulSoup4**  
  Parses and extracts relevant IPO information from HTML content.

- **Regex (re module)**  
  Detects company names and extracts IPO opening and closing dates from text.

- **nepali-datetime**  
  Converts Nepali calendar dates into English (AD) dates for accurate reminders.

- **Tkinter**  
  Displays desktop popup alerts for IPO notifications.

- **JSON**  
  Stores IPO details and alert history persistently.

- **OS & File Handling**  
  Manages folders and files for local data storage.

- **Datetime**  
  Handles date calculations and reminder logic.

- **Windows Task Scheduler**  
  Automates daily execution of the script.
