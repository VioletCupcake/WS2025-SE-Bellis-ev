
# KEY STRUCTURAL DECISIONS

## Why Split models.py? I like things together
- Current: All models in single file (acceptable for MVP start)
- Future: Split into domain modules when >500 lines or >8 models
- Trigger point: Either from the start or after Phase 2 completion

## Foreign Key Cascade Rules (from UML Section 07)
Fall → PersonenbezogeneDaten: CASCADE (always delete together)
Fall → Beratung: CASCADE (delete sessions with case)
Fall → Gewalttat: CASCADE (delete incidents with case)
User → Fall: SET_NULL (preserve case if user deactivated)
Role → User: RESTRICT (cannot delete role if users exist)

## Manager vs View Logic
Managers: Database operations, business rules, data integrity
Views: HTTP handling, authentication, response formatting
Rule: If Frontend doesn't trigger it, it belongs in a Manager

