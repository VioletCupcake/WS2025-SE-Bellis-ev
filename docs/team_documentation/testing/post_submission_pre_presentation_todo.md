IMMEDIATE for Core Functionality

Priority #1: FIX LOGOUT
Allow GET on LogoutView OR Add POST form to navigation

Priority #2: FIX GEWALTTAT DISPLAY 
Review case_detail.html template
Ensure {{ gewalttat.zahl_der_vorfaelle }} etc. are in template
Test display of all Gewalttat fields

Priority #3: ASSESS FOLGEN DER GEWALT 
Check Phase 3B spec: Required or post-MVP?
If required: Implement M2M field in form 
If not: Document as "model ready, UI post-MVP"

Checkpoint: Can now test with all users, data displays correctly

========================

HIGH PRIORITY - Quality

Priority #4: PREVENT EMPTY GEWALTTAT
Add clean() validation to GewalttatForm

Priority #5: FIX DATE FORMATS
Add type="date" widget to all date fields
Set input_formats=['%d.%m.%Y', '%Y-%m-%d']
Test in Beratung + Gewalttat forms

Priority #6: APPLY CLEAN() FIX
Add auto-clear logic for conditional fields

Checkpoint: Forms validate properly, dates work correctly

Priotity #6.5: FIX .JSON TÄTER

=================================

CONDITIONAL (If Time Remains, polishing)

Priority #7: CONDITIONAL FIELD VISIBILITY
└─ Only if presentation requires UX demo
    ├─ Add JavaScript to hide/show fields
    └─ Apply to 4+ forms

Priority #8: EXPAND FALL EDIT FIELDS
└─ Add informationsquelle_andere_details to edit view

Priority #9-13: DEFER TO POST-MVP
└─ Document as known limitations or future improvements