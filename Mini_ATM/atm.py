account = {
    "name": "Caique Novaes",
    "balance": 50500.0,
    "pin": "1234",
    "type": "businessaccount"
}

print("===MINI ATM===")
pin = input("Enter your PIN: ")

if pin == account["pin"]:
    while True:
        print("***ATM MENU***")
        print("1.Check Balance")
        print("2.Deposit Money")
        print("3.Withdraw Money")
        print("4.Account Details")
        print("5.Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print(f"Your balance is: {account['balance']:.2f}")
            
        elif choice == "2":
            amount = float(input("Enter your amount: "))
            if amount > 0:
                account["balance"] += amount
                print("Money deposited successfully.")
                print(f"New balance: {account['balance']:.2f}")
            else:
                print("Invalid amount.")
                
        elif choice == "3":
            amount = float(input("Enter your amount to withdraw: "))
            if 0 < amount <= account["balance"]:
                account["balance"] -= amount
                print("Money withdrawn successfully.")
                print("Collect your cash.")
                print(f"New balance: {account['balance']:.2f}")
            elif amount > account["balance"]:
                print("Insufficient balance.")
            else:
                print("Invalid amount.")
                
        elif choice == "4":
            print("\nAccount type:", account["type"])
            print("Account Holder name:", account["name"])
            print(f"Balance: {account['balance']:.2f}")
            
        elif choice == "5":
            print("Thank you.")
            break
        else:
            print("Invalid choice.")
else:
    print("Invalid PIN. Access denied.")