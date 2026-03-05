from BankAccount import BankAccount


def menu():
    accounts = BankAccount()

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Account management")
        print("2. Transactions")
        print("3. Budgets")
        print("4. Investments")
        print("Anything else: Exit")

        try:
            choice = int(input("\nSelect category: "))

            match choice:
                case 1:  # Подменю Аккаунтов
                    print("\n[Account Management]")
                    print("1. Print accounts\n2. Create account\n3. Delete account\n4. Back")
                    sub_choice = int(input("Select action: "))
                    match sub_choice:
                        case 1:
                            print(accounts)
                        case 2:
                            accounts.create_bank_account(input("Input name: "))
                        case 3:
                            accounts.delete_bank_account(input("Input name: "))

                case 2:  # Подменю Транзакций
                    print("\n[Transactions]")
                    print("1. Deposit\n2. Withdraw\n3. Inside transaction\n4. Outside transaction\n5. History\n6. Back")
                    sub_choice = int(input("Select action: "))
                    match sub_choice:
                        case 1:
                            accounts.deposit(input("Name: "), int(input("Amount: ")))
                        case 2:
                            accounts.withdraw(input("Name: "), int(input("Amount: ")))
                        case 3:
                            accounts.transaction(input("Sender: "), input("Recipient: "), int(input("Amount: ")))
                        case 4:
                            accounts.transaction_out(input("Sender: "), input("Recipient: "), int(input("Amount: ")))
                        case 5:
                            accounts.show_transaction_history()

                case 3:  # Подменю Бюджетов
                    print("\n[Budgets]")
                    print("1. Show budgets\n2. Add budget\n3. Delete budget\n4. Reset budget\n5. Change limit\n6. Back")
                    sub_choice = int(input("Select action: "))
                    match sub_choice:
                        case 1:
                            accounts.show_budget_database()
                        case 2:
                            accounts.add_budget()
                        case 3:
                            accounts.delete_budget()
                        case 4:
                            accounts.reset_budget()
                        case 5:
                            accounts.change_limit()

                case 4:  # Подменю Инвестиций
                    print("\n[Investments]")
                    print(
                        "1. Show database\n2. Add investment\n3. Delete investment\n4. Transaction from investment\n5. Back")
                    sub_choice = int(input("Select action: "))
                    match sub_choice:
                        case 1:
                            accounts.show_investment_database()
                        case 2:
                            accounts.add_investment()
                        case 3:
                            accounts.delete_investment()
                        case 4:
                            accounts.transaction_from_investment()

                case _:
                    print("Goodbye!")
                    break

        except ValueError:
            print("Goodbye!")
            break