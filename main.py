# Glacier Esports - Week 2 Tournament Management App


tournaments = {
    "RL001": {"game": "Rocket League", "entry_fee": 35.00, "fixed_cost": 400.00, "cost_per_team": 5.00, "max_teams": 24},
    "VAL001": {"game": "Valorant", "entry_fee": 45.00, "fixed_cost": 500.00, "cost_per_team": 8.00, "max_teams": 16},
    "RL002": {"game": "Fortnite", "entry_fee": 25.00, "fixed_cost": 400.00, "cost_per_team": 5.00, "max_teams": 24}
}



def show_menu():
    print("\n=== Glacier Esports Tournament Manager ===")
    print("1. View tournament details")
    print("2. Update tournament details")
    print("3. Register a team")
    print("4. View teams and update payments")
    print("5. View financial summary")
    print("6. Run entry fee simulation")
    print("7. Display charts")
    print("8. Save and exit")



def view_tournaments():
    print("\n--- Tournament Details ---")
    for tournament_id, details in tournaments.items():
        print("\nTournament ID:", tournament_id)
        print("Game:", details["game"])
        print("Entry fee: $" + format(details["entry_fee"], ".2f"))
        print("Fixed cost: $" + format(details["fixed_cost"], ".2f"))
        print("Cost per team: $" + format(details["cost_per_team"], ".2f"))
        print("Team capacity:", details["max_teams"])



def get_number(prompt, whole_number=False):
    while True:
        try:
            if whole_number:
                value = int(input(prompt))
            else:
                value = float(input(prompt))
            if value < 0 or (whole_number and value == 0):
                print("Enter a positive number (money amounts can be zero).")
            else:
                return value
        except ValueError:
            print("Invalid number. Please try again.")


# Update an existing tournament by ID, or add a new one with all required details.
def update_tournament():
    tournament_id = input("Enter tournament ID: ").strip().upper()
    if not tournament_id:
        print("Tournament ID cannot be empty.")
        return
    if tournament_id in tournaments:
        print("Existing tournament found. Enter its updated details.")
    else:
        print("New tournament ID. Enter its details to add it.")
    game = input("Game name: ").strip()
    while not game:
        print("Game name cannot be empty.")
        game = input("Game name: ").strip()
    entry_fee = get_number("Entry fee ($): ")
    fixed_cost = get_number("Fixed cost ($): ")
    cost_per_team = get_number("Cost per team ($): ")
    max_teams = get_number("Maximum teams: ", True)
    tournaments[tournament_id] = {
        "game": game,
        "entry_fee": entry_fee,
        "fixed_cost": fixed_cost,
        "cost_per_team": cost_per_team,
        "max_teams": max_teams
    }
    print("Tournament saved successfully!")


# Keep displaying the menu until the user chooses option 8 to exit.
def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            view_tournaments()
        elif choice == "2":
            update_tournament()
        elif choice in ("3", "4", "5", "6", "7"):
            print("Coming soon")
        elif choice == "8":
            print("Goodbye! CSV saving is coming next week.")
            break
        else:
            print("Invalid menu option. Please choose 1 through 8.")


if __name__ == "__main__":
    main()
