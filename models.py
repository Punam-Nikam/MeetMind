# models.py

class ActionItem:
    """This class represents a single action item from a meeting."""
    
    def __init__(self, description, assignee=None, due_date=None):
        """
        The __init__ method is the constructor. It runs when you create a new ActionItem.
        'self' refers to the object itself.
        'description' is the task text.
        'assignee' is the person assigned (default is None if not found).
        'due_date' is the due date (default is None if not found).
        """
        self.description = description
        self.assignee = assignee
        self.due_date = due_date
        self.is_completed = False  # Step 5: Track completion status
        
    def mark_complete(self):
        """Mark this action item as completed."""
        self.is_completed = True
    
    def __str__(self):
        """This defines how the object looks when you print it."""
        # Status symbol
        status = "✅" if self.is_completed else "⏳"
        
        # Assignee text
        assignee_text = self.assignee if self.assignee else "Unassigned"
        
        # Due date text
        due_text = self.due_date if self.due_date else "No due date"
        
        # Format as a clean line
        return f"{status} | {assignee_text:12} | {due_text:15} | {self.description}"
    
    def to_dict(self):
        """Convert the object to a dictionary (useful for MongoDB later)."""
        return {
            "description": self.description,
            "assignee": self.assignee,
            "due_date": self.due_date,
            "is_completed": self.is_completed
        }