import time
import datetime
import json
import os
from collections import Counter
from datetime import timedelta

filename = "stats.json"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_stats(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as f:
           return json.load(f)
    return []   

def del_stat(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        pass  

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
                print(f"Ошибка ввода. Введите число от {a} до {b}. Попробуйте ещё раз.")
        except ValueError:
            print("Ошибка. Вы ввели не целое число. Попробуйте ещё раз.")
            
def format_seconds(total_seconds):
    td = timedelta(seconds=total_seconds)
    
    days = td.days
    seconds = td.seconds
    microseconds = td.microseconds
    
    hours = (days * 24) + (seconds // 3600)
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    ms_part = f".{microseconds // 10000:02d}" if microseconds else ""
    
    result = []
    
    if hours > 0:
        result.append(f"{hours} час.")
    if minutes > 0:
        result.append(f"{minutes} мин.")
    if remaining_seconds > 0 or microseconds > 0 or not result:
        result.append(f"{remaining_seconds}{ms_part} сек.")
        
    return " ".join(result)
        
def menu():
    print(f"{'ТАЙМЕР СКУКИ':^36}")
    print(f"{'='*36}\n")
    print("1. Запустить таймер\n"
          "2. Статистика\n"
          "3. Выход\n")

def show_stats():
    while True:
        clear_screen()
        print("====================== СТАТИСТИКА ======================\n")
        
        file_data = load_stats(filename)
        is_empty = not file_data
        
        if is_empty == False:
            print(f"{'ДАТА':^16} | {'ВРЕМЯ':^26} | {'СЛОЖНОСТЬ':^10}")
            print("-" * 56)
            for session in file_data:
                print(f"{session['date']:<12} |  {format_seconds(session['time']):>25} | {session['rate']:^10}") 
                
            total_time = sum(s["time"] for s in file_data)
            all_rates = [item["rate"] for item in file_data]
            most_freq_rate, count_rate = Counter(all_rates).most_common(1)[0]
            
            results = []
            
            for item in file_data:
                time_val = item['time']
                rate_val = item['rate']
                date_val = item['date']
                
                ratio_res = rate_val / time_val

                results.append({
                    'date': date_val,
                    'calc_value': ratio_res
                })
                
            best_match = min(results, key=lambda x: x['calc_value'])
                        
            print(f"\nСреднее время: {format_seconds(round(total_time / len(file_data), 2))}"
                  f"\nСамая частая оценка: {most_freq_rate}"
                  f"\nВсего сессий: {len(file_data)}"
                  f"\nЛучшая сессия(дата): {best_match['date']}")
        else:
            print("Статистика отсутствует.")  
            
        print(f"\n{'='*56}\n")
        print("1. Удалить статистику\n"
            "2. Назад\n")
        if user_input("Выберите действие (1-2): ", 1, 2) == 1:
            while True:
                confirm = input("Вы уверены (y/n): ").strip().lower()
                if confirm == "y":
                    del_stat(filename)
                    break
                elif confirm == "n": 
                    break
                else:
                    print("Ошибка! Пожалуйста, введите только 'y' или 'n'.")
        else:
            break
        
    
def timer():
    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    clear_screen() 
    
    input("Нажмите <Enter>, чтобы запустить таймер ...")
    start = time.time()
    
    input("Нажмите <Enter>, чтобы остановить таймер ...")
    stop = time.time()  
       
    dur = round(stop - start, 2)
    
    rate = user_input("Введите сложность скуки (1-5): ", 1, 5)         
    clear_screen()  
           
    print("Время:", dur, "секунд. Сложность:", rate) # Вывод статистики текущей сессии
    
    new_session = {
        "date": date,
        "time": dur,
        "rate": rate
    }   
      
    # Сохранение статистики в файл
    file_data = load_stats(filename)
    file_data.append(new_session)
    save_stats(filename, file_data)
    
    input("Нажмите Enter...")
            


# --------------- запуск ---------------

def main():
    while True:
        clear_screen()
        menu()
        
        choice = user_input("Выберите действие (1-3): ", 1, 3)
        
        # Таймер скуки
        if choice == 1:  
            timer()
        # Вывод статистики
        elif choice == 2:
            show_stats()       
        # Выход
        elif choice == 3:
            break
            
if __name__ == "__main__":
    main()