import tkinter as tk
from tkinter import simpledialog
from worker import WorkerDB, Worker

class WorkerMenuGUI:
    def __init__(self, master, worker_menu):
        self.master = master
        self.worker_menu = worker_menu

        self.add_button = tk.Button(master, text="Add Worker", command=self.add_worker)
        self.add_button.pack()

        self.edit_button = tk.Button(master, text="Edit Worker", command=self.edit_worker)
        self.edit_button.pack()

        self.delete_button = tk.Button(master, text="Delete Worker", command=self.delete_worker)
        self.delete_button.pack()

        self.show_chart_button = tk.Button(master, text="Show Department Pie Chart", command=self.show_chart)
        self.show_chart_button.pack()

        self.display_button = tk.Button(master, text="Display Workers", command=self.display_workers)
        self.display_button.pack()

        self.write_to_file_button = tk.Button(master, text="Write to File", command=self.write_to_file)
        self.write_to_file_button.pack()

        self.sort_by_salary_button = tk.Button(master, text="Sort by Salary", command=self.sort_by_salary)
        self.sort_by_salary_button.pack()

        self.search_by_name_button = tk.Button(master, text="Search by Name", command=self.search_by_name)
        self.search_by_name_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack()

    def add_worker(self):
        name = simpledialog.askstring("Add Worker", "Enter name:")
        surname = simpledialog.askstring("Add Worker", "Enter surname:")
        department = simpledialog.askstring("Add Worker", "Enter department:")
        salary = simpledialog.askstring("Add Worker", "Enter salary:")

        worker = Worker(name=name, surname=surname, department=department, salary=salary)
        self.worker_menu.worker.add(worker)

    def edit_worker(self):
        id_num = simpledialog.askinteger("Edit Worker", "Enter ID of worker to edit:")
        self.worker_menu.edit(id_num)

    def delete_worker(self):
        id_num = simpledialog.askinteger("Delete Worker", "Enter ID of worker to delete:")
        self.worker_menu.delete(id_num)

    def show_chart(self):
        self.worker_menu.show_department_pie_chart()

    def display_workers(self):
        self.worker_menu.display()

    def write_to_file(self):
        filename = simpledialog.askstring("Write to File", "Enter the filename:")
        if filename:
            self.worker_menu.write_to_file(filename)

    def sort_by_salary(self):
        self.worker_menu.sort_by_salary()

    def search_by_name(self):
        name_to_search = simpledialog.askstring("Search by Name", "Enter the name to search for:")
        self.worker_menu.search_by_name(name_to_search)

    def exit_application(self):
        self.master.destroy()


class WorkerMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Worker")
        self.worker = WorkerDB()
        self.worker.read_from_csv_file(r'C:\Users\User\OneDrive - lnu.edu.ua\Робочий стіл\PANDAS\small.csv')
        self.worker_menu_gui = WorkerMenuGUI(root, self)

    def show_department_pie_chart(self):
        self.worker.show_department_pie_chart()

    def display(self):
        self.worker.display()

    def write_to_file(self, filename):
        self.worker.write_to_file(filename)

    def sort_by_salary(self):
        self.worker.sort_by_salary()

    def search_by_name(self, name):
        self.worker.search_by_name(name)

    def delete(self, id_num):
        self.worker.delete(id_num)

    def edit(self, id_num):
        self.worker.edit(id_num)

    def add_worker(self):
        self.worker.add()


if __name__ == "__main__":
    root = tk.Tk()
    menu = WorkerMenu(root)
    root.mainloop()
