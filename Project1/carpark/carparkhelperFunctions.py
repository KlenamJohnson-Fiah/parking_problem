"""Project 1- Carpark"""

import os
import re
from typing import List


class CarparkHelper:
    # def __init__(self, layoutFile: str) -> None:
    #     self.layoutFile = layoutFile

    # function opens the file
    # escaping all lines that are blank using the isspace
    # uses a counter to print the row numbers next to the slots
    def layoutFileReader(file: str) -> int:
        count = 0
        try:
            openFile = open(file, "r")
        except FileNotFoundError:
            print("No found found")
        else:
            print(f"{'ABCD':>8} {'EFGH'}")
            for line in openFile:
                if not line.isspace():
                    count += 1
                    stripped = line.rstrip("\n")
                    print(f"{str(count):3} {stripped:8}")
        finally:
            openFile.close()
        return count

    # Takes the slot selected by the user eg. 1B
    # splits into a list and validates the entry. Making sure the column between A-H and row number is in the right range
    # "1B" -> ["1","B"]
    # TODO: consider 2 digit
    def select_slot(slot_id: str) -> List[str]:
        # Takes care of row 10 when we will have 3 elements in the list
        r = list(slot_id)
        if len(r) == 3:
            r[0] = r[0] + r[1]
            r.remove(r[1])
        firstArrayMatcher = re.match("[1-9]|1[0]", r[0])
        secondArrayMatcher = re.match("[a-hA-H]", r[1])
        if firstArrayMatcher == None:
            print("The first character of the parking slot has to be 1 to 10")
        elif secondArrayMatcher == None:
            print("The second character of the parking slot has to be A to H")
        return r

    # reads list to find the row selected
    # returns a list
    # ["1","B"] -> ["XXXX","XXXO"]
    def determining_the_row(slot_id: str, file: str) -> List[str]:
        # split_selected_slot = list(self.select_slot(slot_id))
        row = int(slot_id[0])
        stripped = []
        counter = 0

        openFile = open(file, "r")
        for lines in openFile:
            if not lines.isspace() and counter <= row - 1:
                textline_read = lines.rstrip()
                counter += 1
                stripped = textline_read.rsplit()

        return stripped

    # Fnx takes a list of slot(["1","B"]) and parking slots at the row(["XXXX","XOXO"])
    def determining_the_column(slot_id: List[str], parking_on_row: List[str]) -> str:
        column = slot_id[1]
        if column == "A" or column == "B" or column == "C" or column == "D":
            columnList = parking_on_row[0]
            return column, list(columnList)
        else:
            columnList = parking_on_row[1]
            return column, list(columnList)

    # Takes the columnId ("B") and the list of the slot section at the row (["X","X","O","X"])
    # returns a str(["X"])
    def determining_slot_availability(
        column_ID: str, parking_section: List[str]
    ) -> str:
        match column_ID:
            case "A":
                return parking_section[0]
            case "B":
                return parking_section[1]
            case "C":
                return parking_section[2]
            case "D":
                return parking_section[3]
            case "E":
                return parking_section[0]
            case "F":
                return parking_section[1]
            case "G":
                return parking_section[2]
            case "H":
                return parking_section[3]

    # Takes the slot letter "X" or "O"
    # returns false if "X" and True if "0"
    def parking_slot_availability_Check(slot: str) -> bool:
        if slot == "X":
            return False
        elif slot == "O":
            return True

    def book_parking_slot(slot_id: str, file: str) -> str:
        determiningRow = CarparkHelper.determining_the_row(slot_id, file)
        (
            determiningRowColumn,
            determiningRowColumnList,
        ) = CarparkHelper.determining_the_column(slot_id, determiningRow)
        # print(determiningRowColumnList)

        # Determines the array position to change
        if determiningRowColumn == "A" or determiningRowColumn == "E":
            determiningRowColumnList[0] = "X"
        elif determiningRowColumn == "B" or determiningRowColumn == "F":
            determiningRowColumnList[1] = "X"
        elif determiningRowColumn == "C" or determiningRowColumn == "G":
            determiningRowColumnList[2] = "X"
        elif determiningRowColumn == "D" or determiningRowColumn == "H":
            determiningRowColumnList[3] = "X"

        # combines the list into a single string
        combineList = "".join(determiningRowColumnList)
        return combineList

    # Takes the output that has the booked vacant slot and puts it into the
    # the initial read list
    # ['X', 'X', 'X', 'O'] -> booked becomes "XXXX"
    # put this back into the initial array ["XXXX","XXXO"] -> ["XXXX","XXXX"]
    def update_parking_slot(slot_id: str, updated_slot: str, file: str):
        # returns the row read from file
        row_read = CarparkHelper.determining_the_row(slot_id, file)
        # print(updated_slot)
        # print(slot_id)
        # print(row_read)
        if (
            slot_id[1] == "A"
            or slot_id[1] == "B"
            or slot_id[1] == "C"
            or slot_id[1] == "D"
        ):
            row_read[0] = updated_slot
            return row_read
        else:
            row_read[1] = updated_slot
            return row_read

    # Change the list created after booking the slot into a string
    # ["OXOO", "OOOO"] -> "OXOO OOOO"
    def update_the_row_ToString(rowList: List[str]) -> str:
        rowToString = " ".join(rowList)
        return rowToString

    # Write the string generated from fnx update_the_row_ToString() back to temp file
    # Writes the content of the old file into a temp file by writing till the line containing the slot we wish to book is on.
    # The line is updated with and writing from the old file continues from the next line
    def writing_back_toFile(slot_id: List[str], rowLine: str, file) -> str:
        try:
            openOldFile = open(file, "r")
            openNewFile = open("carpark/Temp.txt", "w")
        except FileExistsError as e:
            print("The file doesn't exist {e}")
        else:
            counter_A = 0
            # Writes till the line line just above the line with the parking slot we want.
            # Say we want a slot in line 3, we write to line 2 from the old file to the new file.
            # write our updated line 3 into the new file
            for oldLine in openOldFile:
                if counter_A < int(slot_id[0]) - 1:
                    stripped = oldLine.rstrip("\n")
                    openNewFile.write(stripped + "\n")
                    if not oldLine.isspace():
                        counter_A += 1
            # checks to see if the count is even. If it's even leave a space and write.Else just write below the last line.
            if counter_A % 2 == 0:
                openNewFile.write("\n" + rowLine + "\n")
            else:
                openNewFile.write(rowLine + "\n")
        finally:
            openOldFile.close()
            openNewFile.close()

        try:
            openOldFile = open(file, "r")
            openNewFile = open("carpark/Temp.txt", "a")
        except FileExistsError as e:
            print(f"The file doesn't exist {e}")
        else:
            counter_A = 0
            # continues write to new file just after the line we just updated.
            # Say a slot in line 3 is taken.
            # After updating the line 3 with the new indicator "X", we start writing from line 4 from the old file since that remains unchanged.
            for oldLine in openOldFile:
                stripped = oldLine.rstrip("\n")
                if not oldLine.isspace():
                    counter_A += 1
                    if counter_A > int(slot_id[0]):
                        if counter_A % 2 == 1:
                            openNewFile.write("\n")
                            openNewFile.write(oldLine)
                        else:
                            openNewFile.write(oldLine)
        finally:
            openOldFile.close()
            openNewFile.close()

        return "Success"

    # Removes old file and renames the new file with the name of the old file.
    # This approach was chosen because splitting a file into a list will create memory problems as the file gets larger
    # Using I/O buffer seemed efficient
    @classmethod
    def file_manipulator(cls, oldFile: str, newFile: str = "carpark/Temp.txt") -> bool:
        os.remove(oldFile)
        os.rename(newFile, oldFile)
        return True

    # Helper function to achieve the Nearest Neighbour Search.
    # This function reads a specific number of lines provided by the "lines_to_read" argument from the file.
    # Returns the line as a dictionary with the line number as the Key.
    # if lines_to_read=2, we have {1:"XXXXXXXO", 2:"XXOXXXOO"}
    # if lines_to_read=3, we have {1:"XXXXXXXO", 2:"XXOXXXOO" 3:"XXOXXOXX"} and so on.
    # The function removes all whitespace within the line creating a single string.
    def fileLineReader(lines_to_read: int, file: str) -> dict[int, list[str]]:
        openFile = open(file, "r")
        key = 1
        store = {}
        line_counter = 0
        for line in openFile:
            if not line.isspace():
                if line_counter < lines_to_read:
                    line_items = line.strip().replace(" ", "")
                    store[key] = line_items
                    line_counter += 1
                    key += 1

        return store

    # Helper function to achieve the Nearest Neighbour Search.
    # This function reads a dictionary.
    # Reading the value(str) of each key.
    # given the dict example {1:"XXXXXXXO", 2:"XXOXXXOO"}
    # the function reads the first two elements in the strings for both items in the dict because matrixStart=2.
    # if matrixStart=3. It reads the first 3 elements of the strings in the dict
    # returns the key and element number where an empty slot("O") was found.
    def read_in_Matrix(
        elements: dict[int, str], matrixStart: int = 2
    ) -> tuple[int, int]:
        for k, v in elements.items():
            i = 0
            for value in v:
                if i < matrixStart:
                    if value != "O":
                        i += 1
                    else:
                        return (k, i)

    # This is a helper function that interprets the output tuple from the fnx. reserve() in carpark.py
    # The function is a recursive function that returns a tuple of row and column of a found available within the
    # nearest neighbour search.
    # if a tuple of (2,2) is return it interprets as Row 2 Column C. Hence "2C"
    def interpreter(row_column: tuple[int, int]) -> str:
        match row_column[1]:
            case 0:
                return str(row_column[0]) + "A"
            case 1:
                return str(row_column[0]) + "B"
            case 2:
                return str(row_column[0]) + "C"
            case 3:
                return str(row_column[0]) + "D"
            case 4:
                return str(row_column[0]) + "E"
            case 5:
                return str(row_column[0]) + "F"
            case 6:
                return str(row_column[0]) + "G"
            case 7:
                return str(row_column[0]) + "H"
            case default:
                return "No match here"
