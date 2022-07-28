import queue
import threading
import time
from datetime import datetime, timedelta
import uuid
import random

start_time = time.time()
q = queue.Queue()
class OrdersManager:
    __orders_processed = 0
    __last_printed_log = datetime.now()

    def __init__(self) -> None:
        self.__generate_fake_orders(quantity=1000)

    def __generate_fake_orders(self, quantity):
        self.__log(f"Generating fake orders")
        for j in range(quantity):
            q.put([uuid.uuid4(), j])
            start_time = time.time()
        self.__log(f"{q.qsize()} generated...")

        "Thread Creation"

        for i in range(5):
            t = threading.Thread(target=self.task, args=(q,quantity))
            print("Thread created:" +str(i))
            t.start()

    def __log(self, message):
        print(f"{datetime.now()} > {message}")

    def task(self,q,quantity):
          while q.empty()!=True:
            task = q.get()
            try:
             uuid = task[0]
             index = task[1]
             self.__log(
                 message=f'Order number {uuid} {index} was successfully prosecuted.'
             )

             self.__orders_processed += 1
             if datetime.now() > self.__last_printed_log:
                self.__last_printed_log = datetime.now() + timedelta(seconds=5)
                self.__log(
                    message=f"Total orders executed: {self.__orders_processed}/{quantity}"
                )
             time.sleep(random.uniform(0, 1))
            finally:
             q.task_done()
orders_manager = OrdersManager()
q.join()
delay = time.time() - start_time
print(f"{datetime.now()} > Total Execution time: {delay} seconds...")
