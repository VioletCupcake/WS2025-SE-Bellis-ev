from core.models import Case
from datetime import date 

    #Funktion zum erstellen eines Cases mithilfe einer übergebenen Case ID, andere Parameter müssten noch hinzugefügt werden
def create_case(case_id):
    new_case = Case.objects.create(
        case_id = case_id,
        date_creation = date.today(),
        edit_date = date.today(), 
        edited_by_employee = "not yet implemeted",
        status = "open"
    )
    return new_case

def delete_case(case_id):
    try: 
        case = Case.objects.get(case_id=case_id)
        case.delete()
        return True
    except ObjectDoesNotExist: # type: ignore
        return False