import time
import json
import os
from collections import Counter
from datetime import datetime, timedelta
import sys

STATS_FILE = "stats.json"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_stats(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as f:
            try: 
                return json.load(f)
            except json.JSONDecodeError:
                print("file is corrupted")
                return []
    return []

def save_stats(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def del_stat(filename):
    save_stats(filename, [])
    
def safe_input(prompt=""):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nExit.")
        sys.exit(0)
        
def user_input(req, a, b):
    while True:
        try:
            user_choice = int(safe_input(req))
            if a <= user_choice <= b:
                return user_choice
            else:
                print(f"Input error. Enter a number from {a} to {b}. Try again.")
        except ValueError:
            print("Error. You entered a non-integer number. Try again.")
            
def format_seconds(total_seconds):
    if total_seconds < 0:
        return "0 seconds"
    else:
        td = timedelta(seconds=total_seconds)
        
        days = td.days
        seconds = td.seconds
        microseconds = td.microseconds
        
        hours = (days * 24) + (seconds // 3600)
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        
        # if there are microseconds, a tail with two decimal places is saved; if there are none, there will be no microseconds
        ms_part = f".{microseconds // 10000:02d}" if microseconds else ""
        
        result = []
        
        if hours > 0:
            result.append(f"{hours} hour(s)")
        if minutes > 0:
            result.append(f"{minutes} minutes")
        if remaining_seconds > 0 or microseconds > 0 or not result:
            result.append(f"{remaining_seconds}{ms_part} seconds")
            
        return " ".join(result)
        
def best_match_stats(file_data):
    results = []
    for item in file_data:
        time_val = item['time']
        rate_val = item['rate']
        date_val = item['date']
                    
        ratio_res = rate_val / time_val if time_val > 0 else float('inf')
    
        results.append({
            'date': date_val,
            'calc_value': ratio_res
        })
                    
    # the best one is the longest session with the lowest difficulty, the smallest rate / time ratio
    return min(results, key=lambda x: x['calc_value'])
        
def are_you_sure(fun, stats_file):
    while True:
        confirm = safe_input("Are you sure (y/n): ").strip().lower()
        if confirm == "y":
            fun(stats_file)
            break
        elif confirm == "n": 
            break
        else:
            print("Error! Please enter only 'y' or 'n'.")
        
def menu():
    print(f"{'BOREDOM TIMER':^36}")
    print(f"{'='*36}\n")
    print("1. Start timer\n"
          "2. Statistics\n"
          "3. Exit\n")

def show_stats(stats_file):
    while True:
        clear_screen()
        print("====================== STATISTICS ======================\n")
        
        file_data = load_stats(stats_file)
        
        if file_data:
            print(f"{'DATE':^16} | {'TIME':^26} | {'DIFFICULTY':^10}")
            print("-" * 56)
            for session in file_data:
                print(f"{session['date']:<16} |  {format_seconds(session['time']):>25} | {session['rate']:^10}") 
                
            total_time = sum(s["time"] for s in file_data)
            all_rates = [item["rate"] for item in file_data]
            most_freq_rate, _ = Counter(all_rates).most_common(1)[0]
            
            best_match = best_match_stats(file_data)
                        
            print(f"\nAverage time: {format_seconds(round(total_time / len(file_data), 2))}"
                  f"\nMost frequent rating: {most_freq_rate}"
                  f"\nTotal sessions: {len(file_data)}"
                  f"\nBest session (date): {best_match['date']}")
        else:
            print("No statistics available.")  
            
        print(f"\n{'='*56}\n")
        print("1. Delete statistics\n"
              "2. Back\n")
        if user_input("Select an action (1-2): ", 1, 2) == 1:
            are_you_sure(del_stat, stats_file)
        else:
            break
        
    
def timer(stats_file):
    clear_screen() 
    
    safe_input("Press <Enter> to start the timer ...")
    start = time.perf_counter()
    
    safe_input("Press <Enter> to stop the timer ...")
    stop = time.perf_counter() 
    
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
       
    dur = stop - start
    
    rate = user_input("Enter boredom difficulty (1-5): ", 1, 5)         
    clear_screen()  
           
    print("Time:", format_seconds(round(dur, 2)), "\nDifficulty:", rate)  # output current session statistics
    
    new_session = {
        "date": date,
        "time": dur,
        "rate": rate
    }   
      
    # saving statistics to a file
    file_data = load_stats(stats_file)
    file_data.append(new_session)
    save_stats(stats_file, file_data)
    
    safe_input("Press Enter...")
            


# --------------- launch ---------------

def main():
    while True:
        clear_screen()
        menu()
        
        choice = user_input("Select an action (1-3): ", 1, 3)
        
        # boredom timer
        if choice == 1:  
            timer(STATS_FILE)
        # statistics output
        elif choice == 2:
            show_stats(STATS_FILE)  
        # exit
        elif choice == 3:
            break
            
if __name__ == "__main__":
    main()