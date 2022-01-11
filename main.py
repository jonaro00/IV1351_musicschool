"""
Main entry point for the application.
"""

from traceback import print_exc

from rental.view import RentalCLI, InterpreterError
from rental.controller import Controller
from rental.integration import DatabaseError

def main():
    """Starts a CLI with a Controller and runs it."""
    try:
        RentalCLI(Controller()).run_interpreter()
    except (DatabaseError, InterpreterError) as e:
        print(e)
    except Exception:
        print('Unexpected error:')
        print_exc()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
