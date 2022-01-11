"""
Integration Layer

Handles the connection to the Database and provides an
interface to query it.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Result

from .model import RentalInstrument, Rental


# DATABASE LOCAITON, CREDENTIALS, DIALECT AND DRIVER

USER = 'postgres'
PASSWD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB = 'soundgood'

URL = f'postgresql+psycopg2://{USER}:{PASSWD}@{HOST}:{PORT}/{DB}'


# TABLE AND COLUMN NAMES

DEFAULT_PK_NAME = 'id'

INST_TABLE_NAME = 'rental_instrument'
INST_PK_COL_NAME = DEFAULT_PK_NAME
INST_TYPE_COL_NAME = 'type'
INST_BRAND_COL_NAME = 'brand'
INST_PRICE_COL_NAME = 'price'
INST_QUANTITY_COL_NAME = 'quantity'
INST_FK_COL_NAME = 'rental_instrument_id'

RENTAL_TABLE_NAME = 'rental'
RENTAL_PK_COL_NAME = DEFAULT_PK_NAME
RENTAL_TERMINATED_COL_NAME = 'terminated'

STUDENT_TABLE_NAME = 'student'
STUDENT_PK_COL_NAME = DEFAULT_PK_NAME
STUDENT_FK_COL_NAME = 'student_id'

TIME_TABLE_NAME = 'time_period'
TIME_PK_COL_NAME = DEFAULT_PK_NAME
TIME_START_COL_NAME = 'start_time'
TIME_END_COL_NAME = 'end_time'
TIME_FK_COL_NAME = 'time_period_id'

PERS_DET_TABLE_NAME = 'personal_details'
PERS_DET_PK_COL_NAME = DEFAULT_PK_NAME
PERS_DET_SSN_COL_NAME = 'ssn'
PERS_DET_FK_COL_NAME = 'personal_details_id'


class RentalDAO:
    """
    Data Access Object for interacting with the Rental parts
    of the Soundgood Database.
    Does not commit writes automatically. Use the `commit`
    method for that. Reads commit themselves.
    """

    def __init__(self) -> None:
        """Initalizes an instance and opens the DB connection."""
        self.engine = create_engine(URL)
        self.conn = None
        self.open()

    def open(self) -> None:
        """Opens a new DB connection."""
        self.close()
        self.conn = self.engine.connect() # Auto-commit is False by default

    def close(self) -> None:
        """Closes any open DB connection."""
        if self.conn is not None:
            self.conn.close()
        self.conn = None

    def execute(self, query: str, *args, **kwargs) -> Result:
        """Prepares the `query` statement, formats it's parameters with args,
        and executes it in the database."""
        try:
            # The `text` method provides parameter formatting
            # and protects from SQL injection.
            return self.conn.execute(text(query), *args, **kwargs)
        except Exception as e:
            self.handle_error(e)

    def commit(self) -> None:
        """Commits the current transaction."""
        try:
            self.conn.connection.connection.commit()
        except Exception as e:
            self.handle_error(e)

    def rollback(self) -> None:
        """Rolls back the current transaction."""
        try:
            self.conn.connection.connection.rollback()
        except Exception as e:
            raise DatabaseError('Transaction rollback failed!') from e

    def handle_error(self, e: Exception) -> None:
        """Handles errors by rolling back an ongoing transaction
        and re-raising an Exception from the root cause."""
        self.rollback()
        raise DatabaseError('Database operation failed.') from e

    def get_instrument_by_id(self, inst_id: int, lock_exclusive: bool = False) -> RentalInstrument:
        """Returns a `RentalInstrument` object representing the
        instrument with id `inst_id`.
        If `lock_exclusive` is True, the table row will remain
        locked until the current transaction is done. Also, this
        method won't commit when it is done. If False, the
        row is not locked, and this method commits on it's own.
        Raises error if no instrument is found."""
        res = self.execute(f"""
                SELECT * FROM {INST_TABLE_NAME}
                WHERE {INST_PK_COL_NAME} = :i
                {'FOR UPDATE' if lock_exclusive else ''}
                ;""",
                {'i': inst_id}
            )
        if not lock_exclusive:
            self.commit()
        return RentalInstrument(**res.one())

    def get_instruments_in_stock(self, type: str | None = None) -> list[RentalInstrument]:
        """Returns list of all `RentalInstrument`s in stock.
        Optionally, the instruments can be filtered with `type`."""
        res = self.execute(f"""
                SELECT * FROM {INST_TABLE_NAME}
                WHERE {INST_QUANTITY_COL_NAME} > 0
                {f"AND {INST_TYPE_COL_NAME} = :t" if type else ""}
                ;""",
                {'t': type}
            )
        self.commit()
        return [RentalInstrument(**row) for row in res]

    def update_instrument(self, inst: RentalInstrument) -> None:
        """Updates the DB entry for the `RentalInstrument` object."""
        res = self.execute(f"""
                UPDATE {INST_TABLE_NAME} SET
                    {INST_TYPE_COL_NAME} = :t,
                    {INST_BRAND_COL_NAME} = :b,
                    {INST_PRICE_COL_NAME} = :p,
                    {INST_QUANTITY_COL_NAME} = :q
                WHERE {INST_PK_COL_NAME} = :i
                ;""",
                {
                    't': inst.type,
                    'b': inst.brand,
                    'p': inst.price,
                    'q': inst.quantity,
                    'i': inst.id,
                }
            )
        if res.rowcount != 1:
            raise DatabaseError('Update instrument failed.')

    def get_rental_by_id(self, rental_id: int, lock_exclusive: bool = False) -> Rental:
        """Returns a `Rental` object representing the
        rental with id `rental_id`.
        If `lock_exclusive` is True, the table row will remain
        locked until the current transaction is done. Also, this
        method won't commit when it is done. If False, the
        row is not locked, and this method commits on it's own.
        Raises error if no rental is found."""
        res = self.execute(f"""
                SELECT * FROM {RENTAL_TABLE_NAME}
                WHERE {RENTAL_PK_COL_NAME} = :i
                {'FOR UPDATE' if lock_exclusive else ''}
                ;""",
                {'i': rental_id}
            )
        if not lock_exclusive:
            self.commit()
        return Rental(**res.one())

    def get_all_rentals(self) -> list[Rental]:
        """Returns list with all `Rental`s."""
        res = self.execute(f"SELECT * FROM {RENTAL_TABLE_NAME};")
        self.commit()
        return [Rental(**row) for row in res]

    def create_rental(self, student_id: int, inst_id: int, months: int) -> None:
        """Creates a new rental in the DB with the provided student and instrument."""
        # Create an entry in the time table to use for the rental entry
        res = self.execute(f"""
                INSERT INTO {TIME_TABLE_NAME} ({TIME_START_COL_NAME}, {TIME_END_COL_NAME}) VALUES
                    (LOCALTIMESTAMP, LOCALTIMESTAMP + INTERVAL ':m months')
                RETURNING {TIME_PK_COL_NAME}
                ;""",
                {'m': months}
            )
        time_id = res.scalar_one()

        # Insert the Rental
        self.execute(f"""
                INSERT INTO {RENTAL_TABLE_NAME} ({STUDENT_FK_COL_NAME}, {INST_FK_COL_NAME}, {TIME_FK_COL_NAME}) VALUES
                    (:s, :i, :t)
                ;""",
                {
                    's': student_id,
                    'i': inst_id,
                    't': time_id
                }
            )

    def update_rental(self, rental: Rental) -> None:
        """Updates the DB entry for the `Rental` object."""
        res = self.execute(f"""
                UPDATE {RENTAL_TABLE_NAME} SET
                    {STUDENT_FK_COL_NAME} = :s,
                    {INST_FK_COL_NAME} = :i,
                    {TIME_FK_COL_NAME} = :t,
                    {RENTAL_TERMINATED_COL_NAME} = :tr
                WHERE {RENTAL_PK_COL_NAME} = :id
                ;""",
                {
                    's': rental.student_id,
                    'i': rental.rental_instrument_id,
                    't': rental.time_period_id,
                    'tr': rental.terminated,
                    'id': rental.id,
                }
            )
        if res.rowcount != 1:
            raise DatabaseError('Update instrument failed.')

    def get_student_id_from_ssn(self, ssn: str) -> int:
        """Looks up student by `ssn` and returns their id."""
        res = self.execute(f"""
                SELECT s.id
                FROM {STUDENT_TABLE_NAME} s INNER JOIN {PERS_DET_TABLE_NAME} pd
                    ON s.{PERS_DET_FK_COL_NAME} = pd.{PERS_DET_PK_COL_NAME}
                WHERE pd.{PERS_DET_SSN_COL_NAME} = :s
                ;""",
                {'s': ssn}
            )
        self.commit()
        return res.scalar_one()

    def get_number_of_active_rentals(self, student_id: int) -> int:
        """Counts how many active rentals a student has."""
        res = self.execute(f"""
                SELECT COUNT(*) FROM {RENTAL_TABLE_NAME}
                WHERE {STUDENT_FK_COL_NAME} = :i AND {RENTAL_TERMINATED_COL_NAME} = FALSE
                ;""",
                {'i': student_id}
            )
        self.commit()
        return res.scalar_one()


class DatabaseError(Exception):
    """Raised when a Database operation fails"""
