"""
Controller Layer

Binds the View, Model and Integration Layers together.
"""

from .integration import RentalDAO
from .model import Rental, RentalInstrument, MAX_RENTALS, RentalError


class Controller:
    """
    Takes calls from the View Layer and performs the appropriate
    calls to the Model and Integration Layers.
    """

    def __init__(self) -> None:
        """Creates a connection to the Integration Layer."""
        self.db = RentalDAO()

    def get_all_instruments(self, type: str | None = None) -> list[RentalInstrument]:
        """Returns a list of all availible instruments, optionally filtered by `type`."""
        return self.db.get_instruments_in_stock(type)

    def rent_instrument(self, inst_id: int, ssn: str, months: int = 12) -> None:
        """Looks up student by `ssn`, and creates a rental for the specified instrument."""
        # Get student details
        try:
            student_id = self.db.get_student_id_from_ssn(ssn)
            n_rentals = self.db.get_number_of_active_rentals(student_id)
        except Exception as e:
            raise RentalError('Failed to get student info.') from e

        # This is business logic in the controller...
        # I have compromised and kept it this way because the proper solution would
        # involve adding a Student representation to the Model and more queries in
        # Integration, all for achieving this single if-case.
        # This would be moved to the appropriate layer if this project
        # was of a bigger scale.
        if(n_rentals >= MAX_RENTALS):
            raise RentalError('Student already has 2 active rentals.')

        # Create Rental
        try:
            instrument = self.db.get_instrument_by_id(inst_id, True) # lock, since it will be updated
            instrument.rent()
            self.db.update_instrument(instrument)
            self.db.create_rental(student_id, instrument.id, months)
            self.db.commit()
        except Exception as e:
            raise RentalError('Instrument could not be rented.') from e

    def get_all_rentals(self) -> list[Rental]:
        """Returns list of all rentals."""
        return self.db.get_all_rentals()

    def terminate_rental(self, rental_id: int) -> None:
        """Terminates the specifed rental and puts the instrument back in stock."""
        try:
            # Get relevant objects, keep them locked since they will be updated
            rental = self.db.get_rental_by_id(rental_id, True)
            instrument = self.db.get_instrument_by_id(rental.rental_instrument_id, True)
            # Terminate rental and put the instrument back in stock
            rental.terminate()
            instrument.put_back()
            # Update the database to reflect these changes and commit
            self.db.update_rental(rental)
            self.db.update_instrument(instrument)
            self.db.commit()
        except Exception as e:
            raise RentalError('Failed to terminate rental.') from e
