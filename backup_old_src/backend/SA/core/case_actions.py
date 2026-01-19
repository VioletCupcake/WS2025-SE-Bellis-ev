from core.models import Case
from datetime import date 

#Funktion zum erstellen eines Cases mithilfe einer übergebenen Case ID, andere Parameter müssten noch hinzugefügt werden
def create_case(case_id):
    new_case = Case.objects.create(
        case_id = case_id,
        date_creation = date.today(),
        edit_date = date.today(), 
        edited_by_employee = "not yet implemeted",
        status = "OPEN"
    )
    return new_case

def delete_case(case_id):
    try: 
        case = Case.objects.get(case_id=case_id)
        case.delete()
        return True
    except Case.DoesNotExist:
        return False
    
#Änderungung eines beliebigen Attributs, Übergabe mit z.B.: edit_case("CASE-123", status="closed")
#damit das Attribut erkannt werden kann
def edit_case(case_id, **kwargs):
    try:
        case = Case.objects.get(case_id = case_id)
        for field, value in kwargs.items(): 
            if hasattr(case, field):
                setattr(case,field,value) 
        #edited by employee muss noch ergänzt werden wenn wir Nutzer einfügen
        case.edit_date = date.today()
        case.save()

        return case

    except Case.DoesNotExist:
        return None
