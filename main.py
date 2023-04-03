import questionary
from db import get_db
from tracker import Tracker
from analyse import calculate_count, get_tracker_names


def cli():
    db = get_db()
    habits_list = get_tracker_names(db)
    questionary.confirm("Do you want to use preset habits?").ask()

    stop = False
    while not stop:
        main_menu = questionary.select(
            "Welcome to the main menu, what do you want to do?",
            choices=["Complete habit", "Create new habit", "Analyse habits", "Change habits", "Exit"]
        ).ask()

        if main_menu == "Complete habit":
            if not habits_list:
                print("There are no habits to complete")
            else:
                print("Here are your current habits:", habits_list)
                name = questionary.text("Type the name of the habit?").ask()
                choice = questionary.select(
                    "Do you want to complete this task?",
                    choices=["Yes", "No"]
                ).ask()
                if choice == "Yes":
                    tracker = Tracker(name, "no description")
                    tracker.increment()
                    tracker.add_event(db)
                else:
                    main_menu

        elif main_menu == "Create new habit":
            name = questionary.text("What is the name of your habit?").ask()
            desc = questionary.text("What is the description of your counter?").ask()
            tracker = Tracker(name, desc)
            tracker.store(db)

        elif main_menu == "Analyse habits":
            print(habits_list)
            name = questionary.text("What is the name of the habit?").ask()
            choice = questionary.select(
                "Welcome to the main menu, what do you want to do?",
                choices=["List of all currently tracked habits", "List of all habits with the same periodicity", "Longest run streak of all defined habits", "Longest run streak for a given habit", "Back"]
            ).ask()
            if choice == "List of all currently tracked habits":
                count = calculate_count(db, name)
                print(f"{name} has been incremented {count} times")
            elif choice == "List of all habits with the same periodicity":
                print("Hello")
                stop = True
            elif choice == "Longest run streak of all defined habits":
                print("Bye!")
                stop = True
            elif choice == "Longest run streak for a given habit":
                print("Bye!")
                stop = True
            else:
                main_menu

        elif main_menu == "Change habits":
            print(habits_list)
            name = questionary.text("What is the name of the habit?").ask()
            tracker = Tracker(name, "no description")
            tracker.reset()
            tracker.add_event(db)

        else:
            print("Bye!")
            stop = True


if __name__ == '__main__':
    cli()