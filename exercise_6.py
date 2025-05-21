from abc import ABC, abstractmethod
from typing import List, Dict


# ---------- Клас Автор (композиція) ----------
class Author:
    def __init__(self, first_name: str, last_name: str, birth_date: str):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__birth_date = birth_date

    def full_name(self):
        return f"{self.__first_name} {self.__last_name}"


# ---------- Абстрактний клас Матеріал Бібліотеки ----------
class LibraryItem(ABC):
    def __init__(self, title: str, year: int):
        self._title = title
        self._year = year

    @abstractmethod
    def get_description(self) -> str:
        pass


# ---------- Клас Рейтинг ----------
class Rating:
    def __init__(self, user: str, score: int, comment: str = ""):
        self.user = user
        self.score = score
        self.comment = comment


# ---------- Клас Книга (успадковує LibraryItem) ----------
class Book(LibraryItem):
    def __init__(self, title: str, year: int, author: Author):
        super().__init__(title, year)
        self.__author = author
        self.__ratings: List[Rating] = []

    def add_rating(self, rating: Rating):
        self.__ratings.append(rating)

    def average_rating(self):
        if not self.__ratings:
            return 0
        return sum(r.score for r in self.__ratings) / len(self.__ratings)

    def get_description(self):
        return f"Книга: '{self._title}', {self._year}, Автор: {self.__author.full_name()}, Рейтинг: {self.average_rating():.1f}"


# ---------- Клас ЕлектроннаКнига ----------
class EBook(Book):
    def __init__(self, title: str, year: int, author: Author, file_format: str, file_size: float):
        super().__init__(title, year, author)
        self.file_format = file_format
        self.file_size = file_size  # в MB

    def get_description(self):
        return f"{super().get_description()} [Електронна книга: {self.file_format}, {self.file_size}MB]"


# ---------- Клас DVD ----------
class DVD(LibraryItem):
    def __init__(self, title: str, year: int, video_format: str):
        super().__init__(title, year)
        self.video_format = video_format

    def get_description(self):
        return f"DVD: '{self._title}', {self._year}, Формат: {self.video_format}"


# ---------- Клас Аудіокнига ----------
class AudioBook(LibraryItem):
    def __init__(self, title: str, year: int, duration_minutes: int):
        super().__init__(title, year)
        self.duration = duration_minutes

    def get_description(self):
        return f"Аудіокнига: '{self._title}', {self._year}, Тривалість: {self.duration} хв."


# ---------- Клас Журнал ----------
class Magazine(LibraryItem):
    def __init__(self, title: str, year: int, issue_number: int, date: str):
        super().__init__(title, year)
        self.issue_number = issue_number
        self.date = date

    def get_description(self):
        return f"Журнал: '{self._title}', Випуск №{self.issue_number}, Дата: {self.date}"


# ---------- Клас Відділ (агрегація книг) ----------
class Department:
    def __init__(self, name: str):
        self.name = name
        self.items: List[LibraryItem] = []

    def add_item(self, item: LibraryItem):
        self.items.append(item)

    def remove_item(self, title: str):
        self.items = [i for i in self.items if i._title != title]

    def list_items(self):
        return [item.get_description() for item in self.items]


# ---------- Клас Бібліотека (агрегація відділів) ----------
class Library:
    def __init__(self, name: str, address: str, founded_year: int):
        self.name = name
        self.address = address
        self.founded_year = founded_year
        self.departments: Dict[str, Department] = {}

    def add_department(self, department: Department):
        self.departments[department.name] = department

    def remove_department(self, name: str):
        if name in self.departments:
            del self.departments[name]

    def list_all_items(self):
        result = []
        for dept_name, dept in self.departments.items():
            result.append(f"Відділ: {dept_name}")
            result.extend(dept.list_items())
        return result


# ---------- Абстрактний клас Читач ----------
class Reader(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def max_books_allowed(self) -> int:
        pass


# ---------- Класи-нащадки Читача ----------
class Student(Reader):
    def max_books_allowed(self) -> int:
        return 10

class Worker(Reader):
    def max_books_allowed(self) -> int:
        return 7

class Guest(Reader):
    def max_books_allowed(self) -> int:
        return 3



if __name__ == "__main__":
    author1 = Author("Айзек", "Азі́мов", "1920-01-02")
    author2 = Author("Джордж", "Оруелл", "1903-06-25")

    book1 = Book("Фундація", 1951, author1)
    book2 = EBook("1984", 1949, author2, "PDF", 2.4)

    dvd = DVD("Інтерстеллар", 2014, "MP4")
    audiobook = AudioBook("Фундація (аудіо)", 2020, 600)
    magazine = Magazine("Наука і життя", 2024, 5, "2024-03-01")

    fiction = Department("Фантастика")
    fiction.add_item(book1)
    fiction.add_item(book2)
    fiction.add_item(audiobook)

    media = Department("Медіа")
    media.add_item(dvd)
    media.add_item(magazine)

    lib = Library("Центральна бібліотека", "вул. Наукова, 12", 1950)
    lib.add_department(fiction)
    lib.add_department(media)

    book1.add_rating(Rating("Іван", 5, "Шедевр!"))
    book1.add_rating(Rating("Оля", 4, "Цікаво."))

    print("\n--- Каталог бібліотеки ---")
    for desc in lib.list_all_items():
        print(desc)

    student = Student("Андрій")
    guest = Guest("Марта")
    print(f"\nСтудент {student.name} може взяти до {student.max_books_allowed()} книг.")
    print(f"Гість {guest.name} може взяти до {guest.max_books_allowed()} книг.")