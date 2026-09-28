from datetime import datetime

class Bug:
    PRIORITY_VARIANTS = ["Low", "Medium", "High", "Critical"]
    STATUS_VARIANTS = ["New", "In Progress", "Resolved", "Closed"]

    def __init__(self, bug_id, title, priority, status="New", created_at=None):
        self.bug_id = bug_id
        self.title = title
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%d-%m-%Y %H:%M")


    def  __str__(self):
        return f"[{self.bug_id}] {self.title} | Priority: {self.priority} | Status: {self.status}"
    
    def update_priority(self, new_priority):
     if new_priority in self.PRIORITY_VARIANTS:
       self.priority = new_priority

    def update_status(self, new_status):
     if new_status in self.STATUS_VARIANTS:
       self.status = new_status
    
    def matches_keyword(self, keyword):
       return keyword.lower() in self.title.lower()
        

    