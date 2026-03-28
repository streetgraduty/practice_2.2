import psutil
import time

def monitor_resourses():  
    print("Мониторинг CPU и памяти (Ctrl+C для выхода)\n")

    try:
        while True:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").per cent
            
            print(f"CPU: {cpu}% | Память: {memory}% | Загрузка диска: {disk}")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\nЗавершено")

if __name__ == "__main__":
    monitor_resourses()
