from models import Bug
from datetime import datetime

def test_add_bug_success():
  bug = Bug(bug_id=None,title="Wrong symbol",priority="High",status="New")
  
  assert bug.bug_id is None
  current_date = datetime.now().strftime("%d-%m-%Y")
  assert bug.created_at.startswith(current_date)
