from redis import Redis
from rq import Queue
import utils.tasks_todo as tasks


r = Redis()
queue = Queue(connection=r)


def main():
    queue.enqueue(tasks.print_task, 5)
    queue.enqueue(tasks.print_numbers, 5)
    
if __name__ == "__main__":
    main()
