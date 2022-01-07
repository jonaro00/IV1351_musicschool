"""
Main entry point for the application.
"""

from rental.view import RentalCLI
from rental.controller import Controller
from rental.integration import DatabaseError

def main():
    try:
        RentalCLI(Controller()).run_prompt()
    except DatabaseError as e:
        print(e)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
