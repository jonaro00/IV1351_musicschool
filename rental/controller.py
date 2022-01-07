from .integration import RentalDAO
from .model import Rental, RentalInstrument, MAX_RENTALS, RentalError


class Controller:
    def __init__(self) -> None:
        self.db = RentalDAO()

    def get_all_instruments(self, type: str | None = None) -> list[RentalInstrument]:
        return self.db.get_instruments_in_stock(type)

    def rent_instrument(self, inst_id: int, ssn: str, months: int = 12) -> None:
        try:
            student_id = self.db.get_student_id_from_ssn(ssn)
            n_rentals = self.db.get_number_of_active_rentals(student_id)
        except Exception as e:
            raise RentalError('Failed to get student info') from e

        if(n_rentals >= MAX_RENTALS):
            raise RentalError('Student already has 2 active rentals')

        try:
            ins = self.db.get_instrument_by_id(inst_id)
            ins.rent()
            self.db.update_instrument(ins)
            self.db.create_rental(student_id, ins.id, months)
            # ROLLBACK ???
            self.db.commit()
        except Exception as e:
            raise RentalError('Instrument could not be rented') from e

    def get_all_rentals(self) -> list[Rental]:
        return self.db.get_all_rentals()

    def terminate_rental(self, rental_id) -> None:
        try:
            rental = self.db.get_rental_by_id(rental_id)
            rental.terminate()
            # INCREASE STOCK
            self.db.update_rental(rental)
            self.db.commit()
        except Exception as e:
            raise RentalError('Failed to modify rental')



