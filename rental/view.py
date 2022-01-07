
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
    PROMPT = '>>> '

    def __init__(self, controller: Controller) -> None:
        self.cont = controller
        self.reading_commands = False

    def run_prompt(self) -> None:
        print('\n\n### SOUNDGOOD MUSIC INC (c) ###')
        print(    ' ~~ Instrument Rental tool  ~~ ')
        print(    "Type 'help' for a list of commands.\n")
        self.reading_commands = True
        while self.reading_commands:
            cmd = input(self.PROMPT)
            try:
                self.reading_commands = self.parse_cmd(cmd.split())
            except (DatabaseError, RentalError) as e:
                print('Error occured:', e)

    def parse_cmd(self, args: list[str]) -> bool:
        match args:
            # LIST
            case ['l' | 'list', ('i' | 'instruments') | ('r' | 'rentals') as what, *types]:
                # LIST INSTRUMENTS
                if what in ('i', 'instruments'):
                    print('  id |         Type          |      Brand      | Price/month | # in stock ')
                    print('-----+-----------------------+-----------------+-------------+------------')
                    for i in self.cont.get_all_instruments(types[0] if types else None):
                        print(f' {i.id:>3} | {i.type:<21} | {i.brand or "":<15} | {i.price:>11.2f} | {i.quantity:>10} ')
                # LIST RENTALS
                elif what in ('r', 'rentals'):
                    print('Rental stuff')
                    for r in self.cont.get_all_rentals():
                        print(r)
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
            case _:
                print("Unknown command. Type 'help' for a list of commands.")
        print()
        return True
