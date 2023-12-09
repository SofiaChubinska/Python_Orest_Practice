import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

id_count = 0

def sort_key_by_salary(row):
    return float(row['salary'])

def sort_decorator(sort_key):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            self.collection = func(self.collection)
            self.collection = self.collection.sort_values(by='salary', key=sort_key)
        return wrapper
    return decorator



def search_key_by_name(row, name):
    return row['name'].lower() == name.lower()

def search_decorator(search_key):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = self.collection[self.collection.apply(lambda row: search_key(row, *args, **kwargs), axis=1)]
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
        try:
            self.collection = pd.read_csv(filename)
            self.collection["id"] = np.arange(1, len(self.collection) + 1) 

            print("Collection after reading from CSV file:")
            print(self.collection)
        except pd.errors.EmptyDataError:
            print("Error: CSV file is empty.")
        except Exception as e:
            print(f"Error: {e}")

    def write_to_file(self, filename):
        with open(filename, 'w', newline='') as csv_file:
            fieldnames = ["id", "name", "surname", "department", "salary"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for _, row in self.collection.iterrows():
                writer.writerow({"id": row['id'], "name": row['name'], "surname": row['surname'],
                             "department": row['department'], "salary": row['salary']})


    def add(self):
        worker_data = {
            "name": input("name: "),
            "surname": input("surname: "),
            "department": input("department: "),
            "salary": input("salary: ")
        }
        new_worker = pd.DataFrame([worker_data])
        new_worker["id"] = np.max(self.collection["id"]) + 1 if not self.collection.empty else 1
        self.collection = pd.concat([self.collection, new_worker], ignore_index=True)

    def edit(self, id):
        self.collection.loc[self.collection['id'] == id, 'name'] = input("Enter new name: ")
        self.collection.loc[self.collection['id'] == id, 'surname'] = input("Enter new surname: ")
        self.collection.loc[self.collection['id'] == id, 'department'] = input("Enter new department: ")
        self.collection.loc[self.collection['id'] == id, 'salary'] = input("Enter new salary: ")

    def delete(self, id):
        self.collection = self.collection[self.collection['id'] != id]

    def display(self):
        print(self.collection)

    @sort_decorator(sort_key_by_salary)
    def sort_by_salary(self):
        print("Sorting by salary:")
        self.collection['salary'] = self.collection['salary'].astype(float)
        print(self.collection)

    @search_decorator(search_key_by_name)
    def search_by_name(self, result, name):
        print(f"Search results for '{name}':")
        print(result)

    def show_department_pie_chart(self):
        departments = self.collection["department"].tolist()
        print("Departments:", departments)

        department_counts = pd.Series(departments).value_counts()
        print("Department Counts:", department_counts)

        plt.figure(figsize=(8, 8))
        plt.pie(department_counts, labels=department_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of Workers by Department')
        plt.show()

def main():
    filename = r'C:\Users\User\OneDrive - lnu.edu.ua\Робочий стіл\зав_прога\Programming_Practice\small.csv'
    collection = WorkerDB()
    choice = input("Press 1 to read from file: ")
    collection.read_from_csv_file(filename)
    while choice != '0':
        print(" 1 - add worker", "\n", "2 - edit worker", "\n", "3 - delete worker", "\n", "4 - display list of workers",
            "\n", "5 - write list to file", "\n", "6 - exit", "\n", "7 - sort", "\n", "8 - search","\n", "9 - show department pie chart","\n")
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
        elif choice == "8":
            name_to_search = input("enter the name to search for: ")
            collection.search_by_name(name_to_search)
        elif choice == "9":
            collection.show_department_pie_chart()

if __name__ == "__main__":
    main()
