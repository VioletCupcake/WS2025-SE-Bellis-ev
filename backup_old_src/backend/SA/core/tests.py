from datetime import date
from django.test import TestCase
from core.models import Case
from core.case_actions import create_case, delete_case, edit_case
# Create your tests here.

class CaseActionsTest(TestCase):

    def test_create_and_delete_case(self):
        # CREATE
        create_case("TEST-1")
        self.assertEqual(Case.objects.count(), 1)

        case = Case.objects.first()
        self.assertEqual(case.case_id, "TEST-1")

        #EDIT
        self.assertEqual(case.status, "OPEN")
        edit_case("TEST-1", status = "CLOSED", edited_by_employee = "TESTER")
        case.refresh_from_db()
        self.assertIsNotNone(case.status)
        self.assertEqual(case.edited_by_employee, "TESTER")
        self.assertEqual(case.status, "CLOSED")
        self.assertEqual(case.edit_date, date.today())

        # DELETE
        delete_result = delete_case("TEST-1")
        self.assertTrue(delete_result)
        self.assertEqual(Case.objects.count(), 0)

        # DELETE AGAIN (should fail gracefully)
        delete_result_again = delete_case("TEST-1")
        self.assertFalse(delete_result_again)

        
