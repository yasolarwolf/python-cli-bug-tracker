import pytest
from database import add_bug_to_db, get_all_bugs, init_db, delete_bug_from_db, update_bug_status, update_bug_priority
from models import Bug
from engine_oop import show_dashboard

@pytest.fixture
def memory_db(tmp_path):
  db_path = str(tmp_path /"test_bugs.db")
  init_db(db_path)
  return db_path

def test_add_bug_to_database(memory_db):
  title = "Test bug"
  priority = "High"
  status = "New"
  created_at = "03-09-2026 18:00"

  add_bug_to_db(title, priority, status, created_at, db_name = memory_db)
  bugs = get_all_bugs(db_name = memory_db)

  assert len(bugs) == 1
  assert bugs[0][1] == title
  assert bugs [0][2] == priority
  assert bugs [0][3] == status

def test_delete_bug_from_database(memory_db):
  add_bug_to_db("Bug_to_delete", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  bugs_before = get_all_bugs(db_name=memory_db)
  assert len(bugs_before) == 1

  bug_id = bugs_before [0][0]
  delete_bug_from_db(bug_id, db_name=memory_db)

  bugs_after = get_all_bugs(db_name=memory_db)
  assert len(bugs_after) == 0

def test_update_bug_status(memory_db):
  add_bug_to_db("Bug_to_delete", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  bugs = get_all_bugs(db_name=memory_db)
  bug_id = bugs[0][0]
  update_bug_status("In Progress", bug_id, db_name=memory_db)
  updated_bugs = get_all_bugs(db_name = memory_db)
  assert updated_bugs [0][3] == "In Progress"

def test_update_bug_priority(memory_db):
  add_bug_to_db("Bug_to_delete", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  bugs = get_all_bugs(db_name=memory_db)
  bug_id = bugs[0][0]
  update_bug_priority("Medium", bug_id, db_name=memory_db)
  updated_bugs = get_all_bugs(db_name = memory_db)
  assert updated_bugs [0][2] == "Medium"

def test_update_unexisting_bug_id(memory_db):
  add_bug_to_db("Control_bug", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  delete_bug_from_db(9999, db_name=memory_db)
  updated_bugs = get_all_bugs(db_name= memory_db)
  assert len(updated_bugs) == 1
  assert updated_bugs [0][1] == "Control_bug"

def test_get_empty_bug_list(memory_db):
  bugs = get_all_bugs(db_name=memory_db)
  assert bugs == []

def test_add_many_bugs(memory_db):
   add_bug_to_db("Control_bug_one", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
   add_bug_to_db("Control_bug_two", "Medium", "Open", "10-09-2026 22:12", db_name=memory_db)
   add_bug_to_db("Control_bug_three", "High", "Open", "10-09-2026 22:12", db_name=memory_db)
   bugs = get_all_bugs(db_name=memory_db)
   assert len(bugs) == 3
   assert bugs [0][1] == "Control_bug_one"
   assert bugs [1][1] == "Control_bug_two"
   assert bugs [2][1] == "Control_bug_three"

def test_bug_filter_with_key_word(memory_db):
  add_bug_to_db("Control_bug_one", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  add_bug_to_db("User gets wrong password when logging in", "Medium", "Open", "10-09-2026 22:12", db_name=memory_db)
  add_bug_to_db("Control_bug_three", "High", "Open", "10-09-2026 22:12", db_name=memory_db)
  raw_bugs = get_all_bugs(db_name=memory_db)
  bugs = [Bug(raw[0], raw[1], raw[2], raw[3], raw[4]) for raw in raw_bugs]
  keyword = "wrong password"
  search_list = [bug for bug in bugs if bug.matches_keyword(keyword)]
  assert len(search_list) == 1
  assert search_list[0].matches_keyword(keyword) == True
  assert "wrong password" in search_list[0].title

def test_bug_filter_with_bugs_no_results(memory_db):
  add_bug_to_db("Control_bug_one", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  add_bug_to_db("User gets wrong password when logging in", "High", "Open", "10-09-2026 22:12", db_name=memory_db)
  raw_bugs = get_all_bugs(db_name=memory_db)
  bugs = [Bug(raw[0], raw[1], raw[2], raw[3], raw[4]) for raw in raw_bugs]
  keyword = "seven hills"
  search_list = [bug for bug in bugs if bug.matches_keyword(keyword)]
  assert len(search_list) == 0
  assert bugs [0].matches_keyword(keyword) == False
  assert bugs [1].matches_keyword(keyword) == False

def test_bug_filter_without_bugs_no_results(memory_db):
  raw_bugs = get_all_bugs(db_name=memory_db)
  keyword = "login"
  bugs = [Bug(raw[0], raw[1], raw[2], raw[3], raw[4]) for raw in raw_bugs]
  search_list = [bug for bug in bugs if bug.matches_keyword(keyword)]
  assert len(search_list) == 0

def test_dashboard_empty(capsys, memory_db):
  show_dashboard(db_name=memory_db)
  captured = capsys.readouterr()
  assert "You choose to show bug-tracker metrics & dashboard" in captured.out
  assert "The list is empty" in captured.out

def test_dashboard_with_metrics(capsys, memory_db):
  add_bug_to_db("Control_bug_one", "Low", "Open", "10-09-2026 22:12", db_name=memory_db)
  add_bug_to_db("Control_bug_two", "Medium", "Open", "10-09-2026 22:12", db_name=memory_db)
  show_dashboard(db_name=memory_db)
  captured = capsys.readouterr()
  assert "Total bugs : 2" in captured.out
  assert "Open bugs: 2" in captured.out
  assert "Resolution rate: 0.0%" in captured.out
  assert "Latest activity: Control_bug_two at 10-09-2026 22:12"

  




  


 



