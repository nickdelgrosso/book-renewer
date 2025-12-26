
from abc import ABC, abstractmethod
from dataclasses import Field, dataclass, field
from datetime import datetime



class BooksRepo(ABC):
    
    @abstractmethod
    def add_book(self, title: str, due_on: datetime, extensions: int): ...
        

class Clock(ABC):

    @abstractmethod
    def set_current(self, current: datetime): ...

    @abstractmethod
    def get_current(self) -> datetime: ...



@dataclass
class AppSettings:
    extension_days_threshold: int = 2
    
    
    

@dataclass
class App:
    _books_repo: BooksRepo
    _clock: Clock
    _settings: AppSettings = field(default_factory=AppSettings)

    def set_extension_days_threshold(self, value: int): 
        self._settings.extension_days_threshold = value


    