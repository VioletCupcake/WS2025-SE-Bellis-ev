SUMMARY: DJANGO DOES HALF OF OUR WORK OKAY? OKAY.

GO TO TEAM_DOCUMENTATION/MVP 
READ THE PHASES
SEE WHAT PHASE WE ARE IN
ASK WHAT YOU CAN DO
DO IT

You write (Python):
    Settings, .env's and so on

    Model class definition

    Field types and relationships

    Custom validation in forms

    Business logic in managers

Django generates (SQL):

    CREATE TABLE statements

    ALTER TABLE statements

    Foreign key constraints

    Indexes on foreign keys

    CASCADE DELETE triggers

    SELECT/INSERT/UPDATE/DELETE queries

You never write:

    SQL schemas manually

    Foreign key constraint SQL

    Join queries (Django does: fall.beratungen.all())

    Transaction management code (Django's @transaction.atomic)

The database is an implementation detail that Django handles for you!

### SO WHAT CAN WE DO NOW???
YOU GO TO THE TOO LONG DIDNT READ FOLDER.
AND YOU READ IT: 
AND YOU CAN ENSURE EVERYTHING IS SET UP (Postgres, Settings, .env files)
## REGARDING THE .env files and never commiting passwords - YES BUUUUT its a private repo and we COOOOULD create a user for building this shit but we HAVE to clean up the repo later. Or we dont. And share the file like. Via some other platform.