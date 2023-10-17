from carparkhelperFunctions import *
from carpark import Carpark


def main():

    file = "carpark/carpark.txt"
    carpark = Carpark(file)
    while True:
        Carpark.display()
        userInput = input(": ")
        print("-" * 20 + "\n")

        if userInput.upper() == "D":
            CarparkHelper.layoutFileReader(file)
            print("-" * 20 + "\n")
        elif userInput.upper() == "R":
            reserver = carpark.reserve()
            if reserver[0] != None:
                rowColumnInterpreter = CarparkHelper.interpreter(reserver)
                print(
                    f"The nearest available slot to the entrance is {rowColumnInterpreter}"
                )
                default = ""  # default value if the user hits enter on the prompt
                reserveOrNot = (
                    # This is to show "YES" is the default value
                    input("Do you want to reserve this slot[YES/No]: ")
                ) or default
                if reserveOrNot.capitalize() == "Yes" or reserveOrNot == "":
                    sucessOrFail = carpark.assign_slot(rowColumnInterpreter)
                    print(sucessOrFail + "- slot booked")
                    print("-" * 20 + "\n")
                elif reserveOrNot.capitalize() == "No":
                    CarparkHelper.layoutFileReader(file)
                    selectSlot = input("Select a slot. Row and Column(example, 2B): ")
                    sucessOrFail = carpark.assign_slot(selectSlot)
                    print(sucessOrFail + " - slot booked")
            if reserver[0] == None:
                selectSlot = input("Select a slot. Row and Column(example, 2B): ")
                sucessOrFail = carpark.assign_slot(selectSlot)
                print(sucessOrFail + " - slot booked")
                print("-" * 20 + "\n")
        elif userInput.upper() == "S":
            stat = carpark.statistics()
            print(stat)
            print("-" * 20 + "\n")
        elif userInput.upper() == "Q":
            break


if __name__ == "__main__":
    main()
