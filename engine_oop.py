import json
from models import Bug
from database import init_db, add_bug_to_db, get_all_bugs, delete_bug_from_db, update_bug_priority, update_bug_status


MENU_VARIANTS = [
    "Add a new bug", 
    "Show all bugs", 
    "Delete the bug", 
    "Update the bug", 
    "Search the bug",
    "Metrics & Dashboard",
    "Exit"
]

def save_bugs_to_file(bugs_list):
  data_to_save = []
  for bug in bugs_list:
    data_to_save.append({
      'bug_id' : bug.bug_id,
      'title' : bug.title,
      'priority' : bug.priority,
      'status' : bug.status,
      'created_at' : bug.created_at
       })
    
  with open("issue_tracker_data.json", "w", encoding="utf-8") as file:
    json.dump(data_to_save, file, indent=4, ensure_ascii=False)
    print("___Sucessfully saved data to 'issue_tracker_data.json'___")

def load_bugs_registry():
  raw_bugs = get_all_bugs()
  bugs_list = []

  for row in raw_bugs:
     bug = Bug(
        bug_id = row[0],
        title  = row[1],
        priority = row[2],
        status = row[3],
        created_at = row[4]
     )
     bugs_list.append(bug)

  return bugs_list

def show_dashboard(db_name):
      print("You choose to show bug-tracker metrics & dashboard")
      raw_bugs = get_all_bugs(db_name=db_name)
      all_bugs = [Bug(raw[0], raw[1], raw[2], raw[3], raw[4]) for raw in raw_bugs]

      if not all_bugs:
        print("The list is empty")
      else:
        print(f"Total bugs : {len(all_bugs)}")

        open_bugs = 0
        closed_bugs = 0
        for bug in all_bugs:
          if bug.status == "Closed":
            closed_bugs += 1
          else:
            open_bugs += 1
        last_bug = all_bugs[-1]
        print(f"Open bugs: {open_bugs}")
        print(f"Closed bugs: {closed_bugs}")
        resolution_rate = closed_bugs / len(all_bugs) 
        print(f"Resolution rate: {resolution_rate:.1%} \n Latest activity: {last_bug.title} at {last_bug.created_at}")

   
   
  
if __name__ == "__main__":
  init_db()
  all_bugs = load_bugs_registry()
  if not all_bugs:
      try:
          with open("issue_tracker_data.json", "r", encoding="utf-8") as file:
              json_data = json.load(file)
              for item in json_data:
                  add_bug_to_db(
                      title=item['title'],
                      priority=item['priority'],
                      status=item['status'],
                      created_at=item['created_at']
                  )
          # Перезагружаем список уже из базы данных
          all_bugs = load_bugs_registry()
          print(f"___Migrated {len(all_bugs)} bugs from JSON to SQLite database___")
      except FileNotFoundError:
          pass

  while True:
    print("___BUG TRACKER MENU___")
    for index, variant in enumerate(MENU_VARIANTS, 1):
      print(f"{index} - {variant}")

    choice = input("Select an option: ")

    if choice == "1":
      print("You choose to add a bug")
      bug_title = input("Please enter the name of a bug: ")

      while True:
        for i,name in enumerate(Bug.PRIORITY_VARIANTS, 1):
          print(f"{i} - {name}")
        bug_priority_input = input("Please, enter the bug priority number: ")

        if bug_priority_input.isdigit() and 1 <= int(bug_priority_input) <= len(Bug.PRIORITY_VARIANTS):
         selected_priority = Bug.PRIORITY_VARIANTS[int(bug_priority_input) - 1]
         break
        else:
           print("Error: Invalid priority level")

      while True:
                for i, name in enumerate(Bug.STATUS_VARIANTS, 1):
                    print(f"{i}. {name}")
                bug_status_input = input("Please enter the valid status number, or press ENTER to choose 'New': ")

                if not bug_status_input:
                    selected_status = Bug.STATUS_VARIANTS[0]
                    break
                elif bug_status_input.isdigit() and 1 <= int(bug_status_input) <= len(Bug.STATUS_VARIANTS):
                    selected_status = Bug.STATUS_VARIANTS[int(bug_status_input) - 1]
                    break
                else:
                    print("Invalid status")

      try:
         new_bug = Bug(bug_id = None, title = bug_title, priority=selected_priority, status=selected_status)

         add_bug_to_db(
            title = new_bug.title,
            status = new_bug.status,
            priority = new_bug.priority,
            created_at = new_bug.created_at
         )
         all_bugs = load_bugs_registry()
         print("Bug successfully added to Database")
      except ValueError as e:
         print(f"\n BUG CREATION ERROR : {e} \n Please try to adding the bug again with valid data ")
      
    elif choice == "2":
       print("You choose to show all bugs")
       if not all_bugs:
          print("The list is empty")
       else:
          for bug in all_bugs:
           print(bug)
          print(f"{'*' * 120} \n Amount of bugs : {len(all_bugs)} \n")

    elif choice == "3":
        print("You choose to delete a bug")
        if not all_bugs:
            print("The list is empty")
        else:
            for bug in all_bugs:
                print(bug)

            bug_to_delete_id = input("Please, enter the valid bug number to delete or press Enter to exit: ")
            if bug_to_delete_id == "":
                print("You choose to exit")
                continue
            elif bug_to_delete_id.isdigit(): 
                bug_id = int(bug_to_delete_id)

                target_bug = None
                for bug in all_bugs:
                    if bug.bug_id == bug_id:
                        target_bug = bug
                        break
                
                if target_bug:
                    delete_bug_from_db(bug_id)
                    all_bugs = load_bugs_registry()   
                    print(f"The bug '{target_bug.title}' with ID {bug_id} is successfully deleted")
                else:
                    print("Error: Invalid Bug ID")
            else:
                print("Error: Please enter a valid number")

    elif choice == "4":
       print("You choose to update the bug")
       if not all_bugs:
          print("The list is empty")
       else:
          for numb, bug in enumerate(all_bugs, 1):
             print(f"{numb} - {bug}")
        
          selected_bug = input("Please, enter the valid bug number to update or press Enter to exit: ")
          if selected_bug == "":
             print("You choose to exit")
             continue
          elif selected_bug.isdigit() and 1 <= int(selected_bug) <= len(all_bugs):
             index = int(selected_bug) - 1
             selected_bug = all_bugs[index]
          else:
              print("Error: Invalid bug number")
              continue
          
          select_update_parameter = input(f"Choose the parameter for the update - '1' for PRIORITY, '2' for STATUS: ")
          if select_update_parameter == "1":
             print("You choose the priority update")
             for numb, priority in enumerate(Bug.PRIORITY_VARIANTS, 1):
                print(f"{numb} - {priority}")
             select_update_priority_variant = input(f"Please enter a valid priority number for the bug  you want update: ")
             if select_update_priority_variant.isdigit():
                val = int(select_update_priority_variant)
                if 1 <= val <= len(Bug.PRIORITY_VARIANTS):
                   result_of_index_priority_to_update = val - 1
                   new_priority = Bug.PRIORITY_VARIANTS[result_of_index_priority_to_update]
                   update_bug_priority(new_priority, selected_bug.bug_id)
                   selected_bug.update_priority(new_priority)
                   print(f"Priority updated to: {selected_bug.priority}")
                else:
                   print("Error: Invalid priority variant")
          
          elif select_update_parameter == "2":
             print("You choose the status update")
             for number, status in enumerate(Bug.STATUS_VARIANTS, 1):
                print(f"{number} - {status}")
             select_update_status_variant = input("Please enter a valid status number for the bug you want update: ")
             
             if select_update_status_variant.isdigit():
                val = int(select_update_status_variant)
                if 1 <= val <= len(Bug.STATUS_VARIANTS):
                   result_of_index_status_to_update = val - 1
                   new_status = Bug.STATUS_VARIANTS[result_of_index_status_to_update]
                   update_bug_status(new_status, selected_bug.bug_id)
                   selected_bug.update_status(new_status)
                   
                   print(f"Status updated to: {selected_bug.status}")
                else:
                   print("Error: Invalid status variant")
             else:
                print("Error: Invalid status variant")

    elif choice == "5":
       print("You choose to search the bug/bugs")
       if not all_bugs:
          print("The list is empty")
       else:
          bug_search_variant = input("Please, enter keyword to search or press Enter to exit: " )
          if bug_search_variant == "":
            print("You choose to exit")
            continue

          search_list = [bug for bug in all_bugs if bug.matches_keyword(bug_search_variant)]
          print(f"Amount of bugs found: {len(search_list)}")
          for number, bug in enumerate(search_list, 1):
              print(f"{number} - {bug}")
    
    elif choice == "6":
       show_dashboard(db_name= "bugs.db")

    elif choice == "7":
       print("You choose to exit")
       break
    
    else:
       print("[Notice] This feature is currently being refactored to OOP")





      







            
  
