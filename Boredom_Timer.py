import time
import json
import os
from collections import Counter
from datetime import datetime, timedelta

filename = "stats.json"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_stats(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as f:
           return json.load(f)
    return []   

def del_stat(filename):
    save_stats(filename, [])

def save_stats(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def user_input(req, a, b):
    while True:
        try:
            user_choice = int(input(req))
            if a <= user_choice <= b:
                return user_choice
            else:
                print(f"Input error. Enter a number from {a} to {b}. Try again.")
        except ValueError:
            print("Error. You entered a non-integer number. Try again.")
            
def format_seconds(total_seconds):
    if total_seconds < 0:
        return 0
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
        
def menu():
    print(f"{'BOREDOM TIMER':^36}")
    print(f"{'='*36}\n")
    print("1. Start timer\n"
          "2. Statistics\n"
          "3. Exit\n")

def show_stats():
    while True:
        clear_screen()
        print("====================== STATISTICS ======================\n")
        
        file_data = load_stats(filename)
        
        if file_data:
            print(f"{'DATE':^16} | {'TIME':^26} | {'DIFFICULTY':^10}")
            print("-" * 56)
            for session in file_data:
                print(f"{session['date']:<12} |  {format_seconds(session['time']):>25} | {session['rate']:^10}") 
                
            total_time = sum(s["time"] for s in file_data)
            all_rates = [item["rate"] for item in file_data]
            most_freq_rate, _ = Counter(all_rates).most_common(1)[0]
            
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
            best_match = min(results, key=lambda x: x['calc_value'])
                        
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
            while True:
                confirm = input("Are you sure (y/n): ").strip().lower()
                if confirm == "y":
                    del_stat(filename)
                    break
                elif confirm == "n": 
                    break
                else:
                    print("Error! Please enter only 'y' or 'n'.")
        else:
            break
        
    
def timer():
    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    clear_screen() 
    
    input("Press <Enter> to start the timer ...")
    start = time.time()
    
    input("Press <Enter> to stop the timer ...")
    stop = time.time()  
       
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
    file_data = load_stats(filename)
    file_data.append(new_session)
    save_stats(filename, file_data)
    
    input("Press Enter...")
            


# --------------- launch ---------------

def main():
    while True:
        clear_screen()
        menu()
        
        choice = user_input("Select an action (1-3): ", 1, 3)
        
        # boredom timer
        if choice == 1:  
            timer()
        # statistics output
        elif choice == 2:
            show_stats()       
        # exit
        elif choice == 3:
            break
            
if __name__ == "__main__":
    main()