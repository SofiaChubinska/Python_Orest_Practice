import csv

id_count = 0

def sort_key_by_salary(worker):
    return float(worker.salary)

def sort_decorator(sort_key):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.collection = sorted(self.collection, key=sort_key)
            func(self, *args, **kwargs)
        return wrapper
    return decorator

def search_key_by_name(worker, name):
    return worker.name.lower() == name.lower()

def search_decorator(search_key):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = [worker for worker in self.collection if search_key(worker, *args, **kwargs)]
            func(self, result, *args, **kwargs)
        return wrapper
    return decorator

class Worker:
    def __init__(self, name="", surname="", department="", salary=""):
        global id_count
        id_count += 1
        self.__ID = id_count
        self.name = name
        self.surname = surname
        self.department = department
        self.salary = salary

    def read_worker(self):
        self.name = input("name: ")
        self.surname = input("surname: ")
        self.department = input("department: ")
        self.salary = input("salary: ")

    def display_worker(self):
        print("ID:", self.__ID, "\n", "Name:", self.name, "\n", "Surname:", self.surname, "\n", "Department:",
              self.department, "\n","Salary: ",self.salary)

    def get_id(self):
        return self.__ID

class WorkerDB:
    def __init__(self):
        self.collection = []

    def read_from_csv_file(self, filename):
        with open(filename, newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                name, surname, department, salary = row["name"], row["surname"], row["department"], row["salary"]
                worker = Worker(name, surname, department, salary)
                self.collection.append(worker)

    def write_to_file(self, filename):
        with open(filename, 'w', newline='') as csv_file:
            fieldnames = ["id", "name", "surname", "department", "salary"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for i in self.collection:
                writer.writerow({"id": i.get_id(), "name": i.name, "surname": i.surname,
                                 "department": i.department, "salary": i.salary})

    def add(self):
        worker = Worker()
        worker.read_worker()
        self.collection.append(worker)

    def edit(self, id):
        for i in self.collection:
            if i.get_id() == id:
                print("1 - edit name", "\n", "2 - edit surname", "\n", "3 - edit department", "\n", "4 - edit salary",
                      "\n")
                choice = int(input("enter your choice: "))
                if choice == 1:
                    n_name = input("enter new name: ")
                    i.name = n_name
                elif choice == 2:
                    n_surname = input("enter new surname: ")
                    i.surname = n_surname
                elif choice == 3:
                    n_department = input("enter new department: ")
                    i.department = n_department
                elif choice == 4:
                    n_salary =  input("enter new salary: ")
                    i.salary = n_salary

    def delete(self, id):
        for i in self.collection:
            if i.get_id() == id:
                self.collection.remove(i)

    def display(self):
        for i in self.collection:
            i.display_worker()
    
    @sort_decorator(sort_key_by_salary)
    def sort_by_salary(self):
        print("Sorting by salary:")
        self.display()

    @search_decorator(search_key_by_name)
    def search_by_name(self, result, name):
        print(f"Search results for '{name}':")
        for worker in result:
            worker.display_worker()
    

def main():
    filename = r'C:\Users\User\OneDrive - lnu.edu.ua\Робочий стіл\зав_прога\Programming_Practice\small.csv'
    collection = WorkerDB()
    choice = input("Press 1 to read from file: ")
    collection.read_from_csv_file(filename)
    while choice != '0':
        print(" 1 - add worker", "\n", "2 - edit worker", "\n", "3 - delete worker", "\n", "4 - display list of workers",
              "\n", "5 - write list to file", "\n", "6 - exit", "\n", "7 - sort", "\n", "8 - search","\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            collection.add()
        elif choice == "2":
            id_num = int(input("Enter ID of worker you want to be changed: "))
            collection.edit(id_num)
        elif choice == "3":
            id_num = int(input("Enter ID of worker you want to be deleted: "))
            collection.delete(id_num)
        elif choice == "4":
            collection.display()
        elif choice == "5":
            collection.write_to_file('result_file.csv')
        elif choice == "6":
            choice = '0'
        elif choice == "7":
            collection.sort_by_salary()
        elif choice =="8":
            name_to_search = input("enter the name to search for: ")
            collection.search_by_name(name_to_search)
        

if __name__ == "__main__":
    main()
