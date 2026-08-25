from abc import ABCMeta, abstractmethod

class Pet(metaclass=ABCMeta):
    @abstractmethod
    def speak(self):
        ...

class Perrot(Pet):
    ...

print(Perrot())