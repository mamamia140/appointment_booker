from booker import task
import schedule
import time


def main():

    schedule.every(5).minutes.do(task)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()