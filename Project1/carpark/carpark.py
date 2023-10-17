from carparkhelperFunctions import CarparkHelper


class Carpark:
    def __init__(self, file: str) -> None:
        self.file = file

    def display() -> str:

        print(
            """
                Select your choice from the menu:
                D to display current status of the car park
                R to reserve an empty slot in the car park
                S to display % occupancy of the car park
                Q to quit
        """
        )

    def statistics(self) -> str:
        slots_counter = 0
        taken_slots_counter = 0
        try:
            openFile = open(self.file, "r")
        except FileNotFoundError as e:
            print(e)
        else:
            for line in openFile:
                stripped = line.rsplit("\n")
                for element in stripped:
                    for individual_row in element:
                        slots_counter += 1
                        if individual_row == "X":
                            taken_slots_counter += 1
        occupancy = taken_slots_counter / slots_counter * 100
        return f"occupancy%: {occupancy:.1f}"

    # The function will search the lines looking for an empty slot if any.
    # The starts by doing a 2x2,3x3,...,8x8 search recursively looking for an empty slot "O".
    # If no slot is found by the end of the 8x8 search, the user is required to manually book.
    # function relies on fnx: fileLineReader() and fnx: read_in_Matrix()
    def reserve(self, matrixStart: int = 2) -> tuple[int, int]:
        if matrixStart == 8:
            return None, None

        linesReader = CarparkHelper.fileLineReader(matrixStart, self.file)
        identified = CarparkHelper.read_in_Matrix(linesReader, matrixStart)
        if identified == None:
            return self.reserve(matrixStart + 1)
        else:
            return identified

    def assign_slot(self, slot: str) -> str:
        select_slot = CarparkHelper.select_slot(slot)
        determiningRow = CarparkHelper.determining_the_row(select_slot, self.file)
        determiningColumn, determiningColumnList = CarparkHelper.determining_the_column(
            select_slot, determiningRow
        )
        determiningAvailability = CarparkHelper.determining_slot_availability(
            determiningColumn, determiningColumnList
        )
        parkingAvailability = CarparkHelper.parking_slot_availability_Check(
            determiningAvailability
        )
        if parkingAvailability == True:
            book_parking = CarparkHelper.book_parking_slot(select_slot, self.file)
            updateSlot = CarparkHelper.update_parking_slot(
                select_slot, book_parking, self.file
            )
            rowToString = CarparkHelper.update_the_row_ToString(updateSlot)
            writeSuccessorFail = CarparkHelper.writing_back_toFile(
                select_slot, rowToString, self.file
            )
            _ = CarparkHelper.file_manipulator(self.file)
            return writeSuccessorFail
