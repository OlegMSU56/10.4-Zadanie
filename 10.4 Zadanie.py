from queue import Queue
from threading import Thread
from time import sleep
from random import randint


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        wait_time = randint(1, 3)
        sleep(wait_time)


class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = Queue()

    def guest_arrival(self, *guests):
        for guest in guests:
            assigned = False
            for table in self.tables:
                if table.guest is None:  # Если стол свободен
                    table.guest = guest  # Присаживаем гостя за стол
                    guest.start()  # Запускаем поток
                    print(f"{guest.name} сел(-а) за стол номер {table.number}")
                    assigned = True
                    break
            if not assigned:  # Если нет свободных столов
                self.queue.put(guest)  # Ставим в очередь
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                if table.guest is None and not self.queue.empty():
                    guest_from_queue = self.queue.get()  # Берем гостя из очереди
                    table.guest = guest_from_queue  # Сажаем его за свободный стол
                    table.guest.start()  # Запускаем поток
                    print(f"{guest_from_queue.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
