from sqlalchemy import create_engine, text
from sqlalchemy.engine import Result

from .model import RentalInstrument, Rental


USER = 'postgres'
PASSWD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB = 'soundgood'

URL = f'postgresql+psycopg2://{USER}:{PASSWD}@{HOST}:{PORT}/{DB}'


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
    def __init__(self) -> None:
        self.engine = create_engine(URL)
        self.conn = None
        self.open()

    def open(self) -> None:
        self.conn = self.engine.connect()

    def close(self) -> None:
        self.conn.close()
        self.conn = None

    def execute(self, cmd: str, *args, **kwargs) -> Result:
        return self.conn.execute(text(cmd), *args, **kwargs)

    def commit(self) -> None:
        try:
            self.conn.connection.connection.commit()
        except Exception as e:
            print(e)

    def get_instrument_by_id(self, inst_id: int) -> RentalInstrument:
        res = self.execute(f"""
                SELECT * FROM {INST_TABLE_NAME}
                WHERE {INST_PK_COL_NAME} = :i
                ;""",
                {'i': inst_id}
            )
        return RentalInstrument(**res.first())

    def get_instruments_in_stock(self, type: str | None = None) -> list[RentalInstrument]:
        res = self.execute(f"""
                SELECT * FROM {INST_TABLE_NAME}
                WHERE {INST_QUANTITY_COL_NAME} > 0
                {f"AND {INST_TYPE_COL_NAME} = :t" if type else ""}
                ;""",
                {'t': type}
            )
        return [RentalInstrument(**row) for row in res]

    def update_instrument(self, inst: RentalInstrument) -> None:
        self.execute(f"""
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

    def get_rental_by_id(self, rental_id: int) -> Rental:
        res = self.execute(f"""
                SELECT * FROM {RENTAL_TABLE_NAME}
                WHERE {RENTAL_PK_COL_NAME} = :i
                ;""",
                {'i': rental_id}
            )
        return Rental(**res.first())

    def get_all_rentals(self) -> list[Rental]:
        res = self.execute(f"SELECT * FROM {RENTAL_TABLE_NAME};")
        return [Rental(**row) for row in res]

    def create_rental(self, student_id: int, inst_id: int, months: int = 12) -> None:
        res = self.execute(f"""
                INSERT INTO {TIME_TABLE_NAME} ({TIME_START_COL_NAME}, {TIME_END_COL_NAME}) VALUES
                    (LOCALTIMESTAMP, LOCALTIMESTAMP + INTERVAL ':m months')
                RETURNING id
                ;""",
                {'m': months}
            )
        time_id = res.scalar()

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
        self.execute(f"""
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

    def get_student_id_from_ssn(self, ssn: str) -> int:
        res = self.execute(f"""
                SELECT s.id
                FROM {STUDENT_TABLE_NAME} s INNER JOIN {PERS_DET_TABLE_NAME} pd
                    ON s.{PERS_DET_FK_COL_NAME} = pd.{PERS_DET_PK_COL_NAME}
                WHERE pd.{PERS_DET_SSN_COL_NAME} = :s
                ;""",
                {'s': ssn}
            )
        return res.scalar()

    def get_number_of_active_rentals(self, student_id) -> int:
        res = self.execute(f"""
                SELECT COUNT(*) FROM {RENTAL_TABLE_NAME}
                WHERE {STUDENT_FK_COL_NAME} = :i AND {RENTAL_TERMINATED_COL_NAME} = FALSE
                ;""",
                {'i': student_id}
            )
        return res.scalar()


class DatabaseError(Exception):
    """Raised when a Database operation fails"""
