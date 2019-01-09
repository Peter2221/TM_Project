""" klasa trzymająca dane użytkownika """
""" imię, wiek, masa, wzrost """

import csv

class UserData:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.dict_of_data = {self.name : "", self.age : 0, self.weight : 0, self.height : 0}


    def write_to_file(self):
        with open('user_data.csv', mode='w', newline="") as csv_file:
            fieldnames = ['name', 'age', 'weight', 'height']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'name': self.name, 'age': self.age, 'weight': self.weight, 'height' : self.height})

    def read_from_file(self):
        with open('user_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            header = []
            dict_of_data = {}
            is_something = False
            for row in csv_reader:
                if line_count == 0:
                    for piece_of_data in row:
                        header.append(piece_of_data)
                    line_count += 1
                else:
                    for num in range(0, len(header) - 1):
                        # podaje klucz oraz wartość
                        dict_of_data[header[num]] = row[num]
                    is_something = True
                    line_count += 1
            return dict_of_data, is_something

    def remove_data_from_file(self):
        f = open("user_data.csv", "w")
        f.truncate()
        f.close()


def main():
    usrData = UserData("Piotrek", 21, 82, 185)
    usrData.write_to_file()
    #usrData.remove_data_from_file()
    b = usrData.read_from_file()
    a = 1

if __name__ == "__main__":
    main()