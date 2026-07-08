"""
একটা TodoList class বানাও:

__init__: tasks=[] (খালি list)
methods:
    add_task(task)      → list এ যোগ করো
    complete_task(task) → list থেকে বাদ দাও
                          না থাকলে → "Error: task নেই!"
    show_tasks()        → সব task দেখাও
    task_count()        → কতটা task আছে

todo = TodoList()
todo.add_task("Python শেখো")
todo.add_task("API শেখো")
todo.complete_task("Python শেখো")
todo.show_tasks()
print(todo.task_count())
"""
class TodoList:
    def __init__(self):
        self.tasks=[]
        self.total_tasks=0
    
    def add_task(self,task):
        self.tasks.append(task)
        self.total_tasks+=1
        return f"Your Task Added: {task}"
    
    def complete_task(self,task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.total_tasks-=1
            return f"Completed taks: {task}"
        else:
            return "Task not found!"
        
    def show_tasks(self):
        print(f"Your Task is {self.tasks}")
    
    def task_count(self):
        return f"Total Task: {self.total_tasks}"


todo = TodoList()
print(todo.add_task("Python শেখো"))
print(todo.add_task("API শেখো"))
print(todo.complete_task("Python শেখো"))
todo.show_tasks()
print(todo.task_count())
