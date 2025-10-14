class Item:
    def __init__(self, name, desc, price):
        self.name, self.desc, self.price = name, desc, price
    def show(self):
        print(f"{self.name} - {self.desc} - Rs {self.price}")
class MP3(Item):
    def __init__(self, name, desc, price, artist, duration):
        super().__init__(name, desc, price)
        self.artist, self.duration = artist, duration
    def play(self):
        print(f"Playing {self.name} by {self.artist}")
class DVD(Item):
    def __init__(self, name, desc, price, cert, duration, actors):
        super().__init__(name, desc, price)
        self.cert, self.duration, self.actors = cert, duration, actors
    def trailer(self):
        print(f"Trailer of {self.name} starring {self.actors}")
class Book(Item):
    def __init__(self, name, desc, price, author, pages, genre):
        super().__init__(name, desc, price)
        self.author, self.pages, self.genre = author, pages, genre
    def preview(self):
        print(f"Preview of {self.name} by {self.author}")
m = MP3("Shape of You", "Pop Song", 150, "Ed Sheeran", "4:20")
m.show(); m.play()
d = DVD("Inception", "Sci-Fi Movie", 1200, "PG-13", "2h 28m", "Leonardo DiCaprio")
d.show(); d.trailer()
b = Book("Harry Potter", "Fantasy Novel", 800, "J.K. Rowling", 500, "Fantasy")
b.show(); b.preview()
