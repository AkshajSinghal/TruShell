import datetime

# CS50.DEV

class Todo:
    def __init__(self, task, category, date_added=None, date_completed=None, status=1, position=None):
        self.task = task
        self.category = category
        self.position = position
        
        # Status- 1 is open, 2 is done
        self.status = status
        
        if date_added:
            self.date_added = date_added
        else:
            self.date_added = datetime.datetime.now().isoformat()
            
        self.date_completed = date_completed

    def __repr__(self):
        return f"Todo({self.task}, {self.category}, pos={self.position}, status={self.status})"

# Example check
if __name__ == "__main__":
    try:
        t = Todo("Buy Milk", "Groceries")
        print(t)
    except Exception as e:
        print(f"Error initializing task: {e}")