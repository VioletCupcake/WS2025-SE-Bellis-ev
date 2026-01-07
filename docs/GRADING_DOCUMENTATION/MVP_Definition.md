# MVP Rationale Document - SE_B-EV_2025

So we got together today (11.12.2025) and, among other things, began to define what consists as our MVP. 
After that, and after overhauling the original UML into a fully functional system design, i went through a few iterations of trying to cut things down based on our decisions. 

This Documents serves as a summary and is open to be discussed and refined

## MVP Definition

`early, most basic version of the product, showcasing the fundamental functionality of our core systems while meeting as many base requirements as possible.` 

While some definitions count minimal necessary requirements under an MVP, we excluded some core features from the final specification. We were tasked to define it ourselves, and reasoning will be given below.

To us, the main priority is to demonstrate that our system is feasible and works, as well as having the option to adjust it based off of feedback before committing to more complex implementations. 
We're also a learning-focused team with mixed experience levels - the MVP needs to teach us Django, database design, and software architecture fundamentals before we tackle advanced features.

## Short Version - What we want:

-  Functioning Users with the ability to create and delete accounts
-  Working Permission Structure with 3 Roles: Basis, Erweitert, Administrator (3 demo users, one  per role)
-  Case management functions: create, edit, search for, and archive cases (alternatively hard delete?)
-  Working cases with all (or some) statistical data fields from the Statistik-Bogen
-  Forms with validation (format checks, required fields, type safety)
-  the ability to track Beratungen without requiring new case data
-  the ability to track violence incidents (Gewalttaten) with multi-selectable violence types (Actually i think i should rename this to gewaltvorfall, i just couldnt be bothered to implement it)
- Reference data management (GewalttatArt, FolgenDerGewalt) - ERWEITERT role can add entries (Maybe rename GewalttatArt to GewaltArt for clarity, tbd)

## Short Version - What we don't want:

-  The entire Export system (PDF/XLSX/CSV generation)
-  Automated anonymization service (manual alias entry for MVP)
-  User-extensible form system (FormularTemplate/FormularFeld/FormularWert)
-  Request intake system (Anfrage entity - start directly at Fall creation)
-  Accompaniments and Referrals tracking (Begleitung/Verweis entities)
-  Advanced statistics engine (Filter, Preset, saved filter combinations)
-  Long-term statistics storage (StatistikErgebnis)
-  Full audit trails (AuditLog)
-  Automated 6-month retention and deletion (DatenRetentionsManager)
-  Any CI/CD pipelines
- Dashboards or advanced UI beyond basic CRUD forms (CRUD = Create, read, update, delete, in case anyone doesn't know the acronym)
- Performance optimization, pagination, complex search

## What we did not include, and why:

## Anfrage
 Pre-counseling contact record with appointment scheduling and wait-time tracking.
 **What we lose:** Can't demonstrate wait-time statistics (datum_eingang → termin_datum) and can't show the full user journey from initial contact to end.
**Why we cut it:**  It would add complexity (8+ enum fields, wait-time-calculations) without really proving out core case management capabilities. Anfrage will be frequently used, but it exists rather isolated. Starting directly at Fall creation simplifies things and reduces the number of entities we need to build and test. The capability to implement whats needed is covered by the existing parts.
**Technical learning impact:** We still learn Django models, foreign keys, and CRUD operations. just with fewer entities.

## User-Extensible Forms (FormularTemplate/FormularFeld/FormularWert)
Our Meta-level system where users with ERWEITERT permissions can add custom fields to forms via UI without code changes.
**What we lose:** ERWEITERT role loses its primary differentiator. Can't add new fields without code changes. 
**What we gain:** Our Team learns basic databse skills + Django forms and validation first. 
We can add dynamic forms once fundamentals are solid, because right now we wont be able to do it well. So we'd rather not do it at all. 
**Why we cut it:** This is the most complex part of the original architecture. It requires:
- Three interconnected entities (template versioning, field definitions, value storage)
- Polymorphic relationships (FormularWert links to ANY entity type via discriminator)
- Manual orphan cleanup (no referential integrity, so deletion logic is fragile)
- Dynamic form rendering on the frontend
- Field dependency logic (show/hide based on values)
- Honestly just skillsets and understanding we don't currently have
This eliminates an entire class of potential bugs (orphaned FormularWert records, validation bypasses, version conflicts), the saved capacities aside.
**Our MVP alternative:** Hardcode all forms in Django templates. The fields from the Statistik-Bogen are built into the Fall/PersonenbezogeneDaten/Beratung/Gewalttat models directly. Users fill out forms, but can't customize them.
**Technical learning impact:** We avoid premature abstraction. Lets master concrete implementations before building meta-systems.

## Accompaniments & Referrals (Begleitung/Verweis)
 Tracking when B-EV staff accompany clients to institutions (courts, police, doctors) or refer them to other services.
**What we lose:** Mainly tracking and filtering / statistics capabilities, which we reduced anyways (see below)
**Why we cut it:** These are valuable for ministry reporting but not core to demonstrating case management. Each adds a separate entity, repository, manager methods, and UI forms.
**MVP alternative:** Simple text fields on Fall for notes about accompaniments/referrals. Proves we can store the information without full entity modeling.
**Technical learning impact:** Nothing besides pratice.

## Statistics Engine (Statistik, Filter, Preset, + junctions)
A Modular filtering system where users build complex queries, save filter combinations as presets, and generate reports with reproducible configurations.
**What we lose:** Can't demonstrate modular architecture (for exmaple for ministry reports). Also can't save/share filter combinations. No reproducible report configurations. These are Major features needed in the End product.
**Why we cut it:**  6 entities (Statistik, Filter, Preset, StatistikErgebnis, Statistik_Filter, Preset_Filter) just to support flexible reporting. Thats just a bit much. Part of defining an MVP is making cuts where it is necessary. The architecture is solid, but building it requires understanding many-to-many relationships, junction tables, query builders, and JSON serialization.
**MVP alternative:** If we need to show statistics at all, hardcode 1-2 simple queries (e.g., "Total cases this month" or "Cases by Beratungsstelle"). Output raw numbers or simple HTML tables. No saved filters, no presets. Its not good. But its something.
**What we gain:** More room to focus on getting the core data model right. Statistics queries are easier once we have real case data to work with. Post-MVP can add filtering incrementally.
**Technical learning impact:** We prove we can query the database and aggregate results. Building a full engine can wait until we understand Django better.

## Export System (PDFExport, CSVExport, XLSXExport, templates)
 Polymorphic export services that render statistics into PDF/Excel/CSV formats using stored templates.
**What we lose:** Can't demonstrate ministry report generation in proper formats. Or well, any Statistic/Export. 
**Why we cut it:** While exports are listed in the base requirements, they're a presentation layer feature that doesn't affect core data management. This stuff requires learning PDF generation libraries, Excel formatting, template engines, and so on. Not the Priority. We want a solid core system. Also, one of our team members is currently working a job where they need to understand these, which could help.
**MVP alternative:** Display (limited) statistics in the web UI only. If hard-copy is absolutely needed for demo, we can screenshot or browser-print.
**What we gain:** 5+ entities cut (PDFTemplate, XLSXTemplate, ExportConfiguration, service classes) and signiiiificant complexity reduction.
**Technical learning impact:** Exports are mostly library integration work. Better to nail the data model first, then add presentation formats.

## Anonymization Service
Service that auto-generates unique aliases from names (e.g., "Maria Schmidt" → "MS_001"), with hash-based reverse lookup table for legal compliance.
**What we lose:** Can't demonstrate (optional) auto-generation. No reverse lookup capability.
**Why we cut it:** The core concept (alias-based pseudonymization) is important for GDPR compliance, but the service implementation is straightforward string manipulation. The AliasMapping reverse-lookup table with SHA-256 hashing and expiration logic adds complexity we don't need to prove the concept works. Currently, Aliases are created manually. An automization was only included after asking about it. Furthermore, we don't have details on how exactly they want these to be done.
**MVP alternative:** Manual alias entry. User types "MS_001" into a text field when creating Fall. System validates uniqueness.
**What we gain:** One less service class, one less entity (AliasMapping). Still proves the architecture supports pseudonymization.
**Technical learning impact:** Shows we understand the _why_ (anonymization requirement) even if we defer the _how_ (auto-generation logic).

## Audit Trail & Retention (AuditLog, DatenRetentionsManager)
Append-only log of every data change (who, when, what field, old/new values) plus automated deletion of cases after 6 months with statistical data preservation.
**What we lose:** Security. Can't demonstrate GDPR compliance mechanisms.
**Why we cut it:** Audit logging is a GDPR requirement and necessary to be able to follow work processes with multiple employees, but MVP won't process real survivor data - only test cases. 
Building a production-grade audit system requires trigger design, log storage strategy, retention policy enforcement, and careful cascade deletion handling. The 6-month retention manager needs scheduled jobs, StatistikErgebnis preservation logic, and manual FormularWert cleanup coordination. 
**MVP alternative:** None. We simply don't log changes or auto-delete. It's just a test.
**What we gain:** 2 entities cut (AuditLog, DatenRetentionsManager conceptually), elimination of scheduled job infrastructure, no need for statistics preservation logic. Overall just A LOT of work.
**Technical learning impact:** Django signals and middleware (for audit logging) are advanced topics. Retention/deletion is post-deployment concern. Like literally one of the last things to do.
**Post-MVP note:** Might be able to add Audit loggin via Django middleware without changing models. Retention manager can be built once we've tested the cascade delete chains.

## What we did include, and why:
We don't only want to show what we chose to keep, but also what abilities in terms of technique, methods, and implementation capabilities it demonstrates, and how they relate to the parts we did not include yet.

## User Management & Three-Tier Permissions
**Kept:** User, Session, Role, PermissionSet
**Why essential:** Role-based access control is fundamental to any multi-user system handling sensitive data. This proves we can:
- Hash passwords securely (Django's bcrypt)
- Manage session state (authentication persistence)
- Implement permission checks (authorization)
- Use one-to-one relationships (Role ↔ PermissionSet)
- Use one-to-many relationships (Role → User)

**Demonstration value:** Three demo users (one per role) showcase different permission levels. BASIS can view/edit cases, ERWEITERT can also manage reference data (add GewalttatArt entries), ADMINISTRATOR can manage users and assign roles. Overall it also demonstrates our ability to utilize Framework features to by mapping usually complex and timeintensive features to them.
**Technical foundation for cut features:** Once we master basic permissions, we can extend PermissionSet with flags for custom forms, audit log access, export permissions, etc.

## Core Case Management (Fall + PersonenbezogeneDaten)
**Kept:** Fall, PersonenbezogeneDaten (1:1 relationship)
**Why essential:** This IS the product. Everything else supports case management. Proves we can:
- Handle one-to-one relationships with CASCADE DELETE
- Separate sensitive data for privacy (architectural concept)
- Validate complex enums (geschlechtsidentitaet, berufliche_situation, etc.)
- Handle nullable fields (alter, wohnort_details)
- Implement soft delete (status = ARCHIVIERT)
- Track aggregate data (beratungsanzahl, letzte_beratung)
- Search by unique identifiers (alias) and date ranges

**MVP decision:** Manual alias entry instead of auto-generation. Still proves pseudonymization concept works.
**Demonstration:** Create a case, edit demographic data, close it, search for it. Core CRUD operations that every subsequent feature builds on.
**Technical foundation for cut features:** Once Fall CRUD is solid, adding Anfrage (pre-case intake) uses identical patterns. Audit logging hooks into Fall.save() method. Retention manager targets Fall.loeschdatum field.

## Nested Case Data (Beratung, Gewalttat)
 Beratung, Gewalttat with one-to-many relationships to Fall
**Why essential:** Proves we can model hierarchical data (case → sessions, case → incidents). Demonstrates:
- One-to-many relationships with CASCADE DELETE
- JSON field usage (taeterinnen_details in Gewalttat)
- Aggregate counter updates (Fall.beratungsanzahl increments when Beratung created)
- Complex multi-field entities (Gewalttat has 15+ attributes)
**Why Beratung specifically:** Shows we can track multiple counseling sessions per case, even if no new case data is entered. 
**Why Gewalttat:** Most complex entity in MVP (violence details, perpetrator tracking, incident counts). If we can build this, we can build anything. (Also again, maybe rename this to Gewaltvorfall)
**Technical foundation for cut features:** Begleitung and Verweis would use identical one-to-many patterns. Anfrage uses simpler structure than Gewalttat, so if Gewalttat works, Anfrage is trivial.

## Reference Data with Hierarchies (GewalttatArt, FolgenDerGewalt)
Kept GewalttatArt, FolgenDerGewalt with self-referential hierarchies and junction tables

**Why essential:** Proves we can:
- Implement self-referential foreign keys (hierarchies)
- Build many-to-many relationships via junction tables
- Seed fixed reference data at deployment
- Handle RESTRICT cascade (can't delete types that are in use)
- Allow ERWEITERT role to extend data (adds unique capability)

**Demonstration:** User selects multiple violence types for one incident (multi-select checkboxes → multiple Gewalttat_GewalttatArt rows). User with ERWEITERT role adds a new violence subcategory.

**Technical foundation for cut features:** This proves we understand junction tables and hierarchical data. The Statistics Filter ↔ Preset many-to-many would use identical patterns.

## Validation System
ValidationService, ValidationResult
**Why essential:** Data integrity is critical. Proves we can:
- Validate input before database commit
- Check data types, formats, ranges
- Validate enums against allowed values
- Return structured error messages
- Integrate with Django forms (form.is_valid())

**MVP scope:** Format validation only (is this a number? is this date valid? is this value in the enum list?). No complex business rules yet (e.g., "closed case must have abschlussdatum").
**Demonstration:** Try to create a case with invalid data (alter = "abc", geschlechtsidentitaet = "invalid_value"). System rejects it with clear error message.

**Technical foundation for cut features:** Once format validation works, we can add business rule validation. Audit logging can hook into validation failures. Dynamic forms (FormularWert) would use the same ValidationService.

## Business Logic Managers (FallManager, SessionManager)
 FallManager, SessionManager as service layer coordinators

**Why essential:** Separates business logic from data models (Django best practice). 
Proves we can:
- Coordinate multi-entity operations (createFall makes Fall + PersonenbezogeneDaten atomically)
- Use database transactions (rollback if either fails)
- Implement search logic (by alias, by date range)
- Manage session lifecycle (create, validate, expire)

**FallManager demonstrates:**
- Creating one-to-one relationships correctly
- Updating aggregate counters (beratungsanzahl)
- Soft delete implementation (status = ARCHIVIERT)
- Search by exact/partial match

**SessionManager demonstrates:**
- In-memory session storage (sufficient for MVP)
- Timeout handling (30-minute inactivity)
- Session validation on each request

**Technical foundation for cut features:** AnfrageManager would follow identical patterns. StatistikManager would coordinate query building. DatenRetentionsManager would orchestrate cascade deletion.

## Technical Foundations Proven by MVP

Even with aggressive feature cuts, the MVP demonstrates:

**Database Design:**
- One-to-one relationships (Fall ↔ PersonenbezogeneDaten, Role ↔ PermissionSet)
- One-to-many relationships (Fall → Beratung, Fall → Gewalttat)
- Many-to-many via junctions (Gewalttat ↔ GewalttatArt, Fall ↔ FolgenDerGewalt)
- Self-referential hierarchies (GewalttatArt, FolgenDerGewalt)
- CASCADE DELETE chains
- RESTRICT on reference data
- UNIQUE constraints (Fall.alias)
- JSON field usage (Gewalttat.taeterinnen_details)

**Django/Python Skills:**
- Models with proper field types and constraints
- Foreign keys with on_delete behavior
- Managers for business logic
- Forms with custom validation
- Template rendering
- Basic authentication/authorization
- Password hashing
- Session management
- Query building (filter, search, aggregate)

**Software Architecture:**
- Separation of concerns (models vs. managers vs. services)
- Service layer pattern (ValidationService, FallManager)
- Repository pattern (implied by managers)
- Enum-based configuration
- Soft delete strategy
- Aggregate denormalization (beratungsanzahl)

## Post-MVP Expansion Path

The MVP is intentionally designed so cut features can be added incrementally without redesign:

**Phase 2 additions (low complexity):**

- Begleitung/Verweis entities (copy Beratung pattern)
- Anfrage entity (simpler than Gewalttat)
- Basic CSV export (Django queryset → csv.writer)
- Simple statistics query (hardcoded report)

**Phase 3 additions (medium complexity):**

- AnonymisierungsService.generateAlias() (20 lines of code)
- AuditLog via Django signals
- PDF export using reportlab
- More complex search (filter by Beratungsstelle, status, date ranges)

**Phase 4 additions (high complexity):**

- Statistics engine (Filter, Preset, query builder)
- User-extensible forms (FormularTemplate system)
- DatenRetentionsManager with scheduled jobs
- Dashboard visualizations
- Full CI/CD pipeline

## Goals for demonstration
Rough outline / idea for prensation demo

- Create 3 users (Basis, Erweitert, Administrator)
- Log in as Basis user, create a case with demographic data
- Add 2 counseling sessions to the case
- Add 1 violence incident with multiple violence types selected
- Search for the case by alias
- Log in as Erweitert user, add a new GewalttatArt entry
- Log in as Administrator, create a new user account
- Close a case (soft delete to ARCHIVIERT status)

**Technical Achievement:**

- 13 entities fully implemented with proper relationships
- Seed data populated (3 users, 5-10 violence types, 8-12 consequence types)
- All forms validate input correctly
- Database CASCADE DELETE tested
- No hardcoded passwords, proper hashing
- Session timeout works
- Permission checks prevent unauthorized actions

**Learning Achievement:**

- Team understands Django models, views, forms, templates
- Team can design normalized databases
- Team can implement multi-tier relationships
- Team can separate business logic from data access
- Team has working development environment
- Team has tested deployment via Docker (basic container, no CI/CD)

This MVP proves the system is feasible and gives us a foundation to iterate on based on feedback before committing to the complex features we deferred.