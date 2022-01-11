"""
View Layer

Contains the CLI that the user uses to interact with the database.
"""

from .model import RentalError
from .controller import Controller
from .integration import DatabaseError

HELP_PAGE = """\
Commands:
    list instruments [type]
        List all instruments availible for rental.
        `type` (optional) specifes what type of instrument to filter for.
    list rentals
        List all rentals.
    rent <instrument_id>
        Rent an instrument.
        The user is prompted for Personal Number and how many months to rent for.
        A student can rent at most 2 instruments at a time.
    terminate <rental_id>
        Terminates (ends) specified rental.
    help
        Show this page.
    quit
        Exit the program.

All commands can be invoked with only their first letter, example: 'l i all'.
"""


class RentalCLI:
    """
    Command Line Interface used to control the program from the terminal.
    Takes a `Controller` at creation, and then the interface can be run.
    """

    PROMPT = '>>> '

    def __init__(self, controller: Controller) -> None:
        """Readies the instance with a `Controller`."""
        self.cont = controller
        self.reading_commands = False

    def run_interpreter(self) -> None:
        """Runs a blocking interpreter reading from stdin."""
        print('\n\n### SOUNDGOOD MUSIC INC (c) ###')
        print(    ' ~~ Instrument Rental tool  ~~ ')
        print(    "Type 'help' for a list of commands.\n")
        self.reading_commands = True
        while self.reading_commands:
            cmd = input(self.PROMPT)
            try:
                self.reading_commands = self.parse_cmd(cmd.split())
            except (DatabaseError, RentalError) as e:
                print('Error occurred:', e)
            except Exception as e:
                raise InterpreterError('Failed to execute command.')
            finally:
                print()

    def parse_cmd(self, args: list[str]) -> bool:
        """Takes a list of string arguments, parses and executes the
        appropriate command, and returns boolean wether the
        interpreter should keep parsing commands or not."""
        match args:
            # LIST
            case ['l' | 'list', 'i' | 'instruments' | 'r' | 'rentals' as what, *types]:
                # LIST INSTRUMENTS
                if what in ('i', 'instruments'):
                    print('  id |         Type          |      Brand      | Price/month | # in stock ')
                    print('-----+-----------------------+-----------------+-------------+------------')
                    for i in self.cont.get_all_instruments(types[0] if types else None):
                        print(f' {i.id:>3} | {i.type:<21} | {i.brand or "":<15} | {i.price:>11.2f} | {i.quantity:>10} ')
                # LIST RENTALS
                elif what in ('r', 'rentals'):
                    print('  id | Instrument id | Active ')
                    print('-----+---------------+--------')
                    for r in self.cont.get_all_rentals():
                        print(f' {r.id:>3} | {r.rental_instrument_id:>13} | {not r.terminated!r:<6} ')
            # RENT
            case ['r' | 'rent', id]:
                id = int(id)
                print('Personal number? (YYYYMMDD-NNNN)')
                ssn = input(self.PROMPT)
                print('How many months? (1 to 12)')
                months = int(input(self.PROMPT))
                self.cont.rent_instrument(id, ssn, months)
                print('Rental created')
            # TERMINATE
            case ['t' | 'terminate', id]:
                id = int(id)
                self.cont.terminate_rental(id)
                print('Rental terminated')
            # HELP
            case ['h' | 'help']:
                print(HELP_PAGE)
            # QUIT
            case ['q' | 'quit']:
                return False
            case []:
                pass
            case _:
                print("Unknown command. Type 'help' for a list of commands.")
        return True

class InterpreterError(Exception):
    """Raised when a command execution fails."""
