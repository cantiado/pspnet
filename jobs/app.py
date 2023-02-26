from datetime import datetime, timedelta
import time
from redis import Redis
from rq import Queue
import tasks

redis = Redis()
queue = Queue(connection=redis)


def main():
    queue.enqueue(tasks.print_task, 5)
    queue.enqueue( tasks.print_numbers, 5)
    
if __name__ == "__main__":
    main()
