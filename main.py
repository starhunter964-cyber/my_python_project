# Glacier Esports Tournament Manager - Week 3
# Uses dictionaries, a list of dictionaries, loops, functions, and CSV files.

import csv

# These are filled by load_data() when the program starts.
tournaments = {}
teams = []


def load_data():
    # Load tournament details into the main dictionary.
    with open("tournament.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tournament_id = row["tournament_id"]
            tournaments[tournament_id] = {
                "game": row["game"],
                "entry_fee": float(row["entry_fee"]),
                "fixed_cost": float(row["fixed_cost"]),
                "cost_per_team": float(row["cost_per_team"]),
                "max_teams": int(row["max_teams"])
            }

    # Each registration is a transaction stored as a dictionary in a list.
    with open("teams.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            team = {
                "tournament_id": row["tournament_id"],
                "team_id": row["team_id"],
                "team_name": row["team_name"],
                "players": int(row["players"]),
                "paid": row["paid"]
            }
            teams.append(team)


def save_data():
    with open("tournament.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["tournament_id", "game", "entry_fee", "fixed_cost", "cost_per_team", "max_teams"])
        for tournament_id in tournaments:
            details = tournaments[tournament_id]
            writer.writerow([
                tournament_id, details["game"], details["entry_fee"],
                details["fixed_cost"], details["cost_per_team"],
                details["max_teams"]
            ])

    with open("teams.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["tournament_id", "team_id", "team_name", "players", "paid"])
        for team in teams:
            writer.writerow([
                team["tournament_id"], team["team_id"],
                team["team_name"], team["players"], team["paid"]
            ])


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


def get_money(prompt):
    while True:
        answer = input(prompt).strip()
        # Check text before calling float(), without using try/except.
        if answer.replace(".", "", 1).isdigit() and answer != ".":
            return float(answer)
        print("Please enter a number that is zero or greater.")


def get_whole_number(prompt):
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and int(answer) > 0:
            return int(answer)
        print("Please enter a whole number greater than zero.")


def get_tournament_id():
    tournament_id = input("Tournament ID: ").strip().upper()
    if tournament_id not in tournaments:
        print("That tournament does not exist.")
        return ""
    return tournament_id


def count_teams(tournament_id):
    count = 0
    for team in teams:
        if team["tournament_id"] == tournament_id:
            count = count + 1
    return count


def view_tournaments():
    print("\n--- Tournament Details ---")
    for tournament_id in tournaments:
        details = tournaments[tournament_id]
        print("\nTournament ID:", tournament_id)
        print("Game:", details["game"])
        print("Entry fee: $" + format(details["entry_fee"], ".2f"))
        print("Fixed cost: $" + format(details["fixed_cost"], ".2f"))
        print("Cost per team: $" + format(details["cost_per_team"], ".2f"))
        print("Team capacity:", details["max_teams"])
        print("Teams registered:", count_teams(tournament_id))


def update_tournament():
    tournament_id = input("Enter tournament ID: ").strip().upper()
    if tournament_id == "":
        print("Tournament ID cannot be empty.")
        return

    game = input("Game name: ").strip()
    if game == "":
        print("Game name cannot be empty. No changes made.")
        return

    entry_fee = get_money("Entry fee ($): ")
    fixed_cost = get_money("Fixed cost ($): ")
    cost_per_team = get_money("Cost per team ($): ")
    max_teams = get_whole_number("Maximum teams: ")

    if max_teams < count_teams(tournament_id):
        print("Capacity cannot be less than the number already registered.")
        return

    tournaments[tournament_id] = {
        "game": game,
        "entry_fee": entry_fee,
        "fixed_cost": fixed_cost,
        "cost_per_team": cost_per_team,
        "max_teams": max_teams
    }
    print("Tournament updated. Choose Save and exit to keep changes.")


def register_team():
    print("\n--- Register a Team ---")
    tournament_id = get_tournament_id()
    if tournament_id == "":
        return

    if count_teams(tournament_id) >= tournaments[tournament_id]["max_teams"]:
        print("This tournament is full.")
        return

    team_id = input("New team ID: ").strip().upper()
    if team_id == "":
        print("Team ID cannot be empty.")
        return

    for team in teams:
        if team["team_id"] == team_id:
            print("That team ID is already registered. Use a unique ID.")
            return

    team_name = input("Team name: ").strip()
    if team_name == "":
        print("Team name cannot be empty.")
        return

    players = get_whole_number("Number of players: ")
    paid = input("Entry fee paid? (Yes/No): ").strip().lower()
    if paid != "yes" and paid != "no":
        print("Enter Yes or No. Registration was not added.")
        return

    if paid == "yes":
        paid = "Yes"
    else:
        paid = "No"

    registration = {
        "tournament_id": tournament_id,
        "team_id": team_id,
        "team_name": team_name,
        "players": players,
        "paid": paid
    }
    teams.append(registration)
    print("Team registered! Choose Save and exit to keep the registration.")


def view_teams_and_payments():
    print("\n--- Registered Teams ---")
    if len(teams) == 0:
        print("No teams are registered.")
        return

    for team in teams:
        print(team["team_id"], "|", team["team_name"], "| Tournament:",
              team["tournament_id"], "| Players:", team["players"],
              "| Paid:", team["paid"])

    answer = input("Update a payment? (Yes/No): ").strip().lower()
    if answer != "yes":
        return

    team_id = input("Team ID to update: ").strip().upper()
    for team in teams:
        if team["team_id"] == team_id:
            paid = input("Paid? (Yes/No): ").strip().lower()
            if paid == "yes":
                team["paid"] = "Yes"
                print("Payment marked as paid.")
            elif paid == "no":
                team["paid"] = "No"
                print("Payment marked as unpaid.")
            else:
                print("Invalid payment status. No changes made.")
            return

    print("Team ID not found.")


def financial_summary():
    print("\n--- Financial Summary ---")
    tournament_id = get_tournament_id()
    if tournament_id == "":
        return

    details = tournaments[tournament_id]
    registered = 0
    paid_count = 0
    for team in teams:
        if team["tournament_id"] == tournament_id:
            registered = registered + 1
            if team["paid"] == "Yes":
                paid_count = paid_count + 1

    collected = paid_count * details["entry_fee"]
    possible_revenue = registered * details["entry_fee"]
    total_cost = details["fixed_cost"] + registered * details["cost_per_team"]
    projected_profit = possible_revenue - total_cost
    current_balance = collected - total_cost

    print("Registered teams:", registered)
    print("Paid teams:", paid_count)
    print("Entry fees collected: $" + format(collected, ".2f"))
    print("Revenue if all registered teams pay: $" + format(possible_revenue, ".2f"))
    print("Expected tournament costs: $" + format(total_cost, ".2f"))
    print("Projected profit if all teams pay: $" + format(projected_profit, ".2f"))
    print("Balance based on fees collected: $" + format(current_balance, ".2f"))


def main():
    load_data()
    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            view_tournaments()
        elif choice == "2":
            update_tournament()
        elif choice == "3":
            register_team()
        elif choice == "4":
            view_teams_and_payments()
        elif choice == "5":
            financial_summary()
        elif choice == "6":
            print("Entry fee simulation will be added in a later week.")
        elif choice == "7":
            print("Charts will be added in a later week.")
        elif choice == "8":
            save_data()
            print("Tournament details and team registrations saved. Goodbye!")
            break
        else:
            print("Invalid menu option. Please choose 1 through 8.")


main()
