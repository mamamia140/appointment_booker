from booker import task
import schedule
import time


def main():
    schedule.every(3).minutes.do(task)
    while len(schedule.get_jobs())!=0:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
