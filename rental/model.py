"""
Model Layer

Object representations of the database entries.
These classes hold data and implement their own business logic.
"""

from dataclasses import dataclass


MAX_RENTALS = 2

@dataclass
class RentalInstrument:
    id: int
    type: str
    brand: str
    price: float
    quantity: int

    def rent(self) -> None:
        if self.quantity <= 0:
            raise RentalError('None in stock.')
        self.quantity -= 1

    def put_back(self) -> None:
        self.quantity += 1

@dataclass
class Rental:
    id: int
    student_id: int
    rental_instrument_id: int
    time_period_id: int
    terminated: bool = False

    def terminate(self) -> None:
        if self.terminated:
            raise RentalError('Rental is already terminated.')
        self.terminated = True


class RentalError(Exception):
    """Raised when read, create or update Rental fails."""
