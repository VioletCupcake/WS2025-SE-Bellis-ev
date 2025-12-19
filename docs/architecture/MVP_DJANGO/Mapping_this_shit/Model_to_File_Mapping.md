# MODELS ORGANIZATION (based on MVP UML, the clean version)

Core/models/user_models.py
├── User                      # UML Section 01 - User entity
├── Session                   # UML Section 01 - Session entity
├── Role                      # UML Section 01 - Role entity
└── PermissionSet             # UML Section 01 - PermissionSet entity

Core/models/fall_models.py
├── Fall                      # UML Section 02 - Core case record
├── PersonenbezogeneDaten     # UML Section 02 - Demographic data (1:1 with Fall)
└── Beratung                  # UML Section 02 - Counseling session

Core/models/gewalttat_models.py
├── Gewalttat                 # UML Section 02 - Violence incident
└── Gewalttat_GewalttatArt    # UML Section 03 - Junction table (many-to-many)

Core/models/reference_models.py
├── GewalttatArt              # UML Section 03 - Violence type reference (hierarchical)
├── FolgenDerGewalt           # UML Section 03 - Consequences reference (hierarchical)
└── Fall_FolgenDerGewalt      # UML Section 03 - Junction table (many-to-many)

Core/managers/fall_manager.py
└── FallManager               # UML Section 05 - Business logic for Fall lifecycle

Core/managers/session_manager.py
└── SessionManager            # UML Section 05 - Session handling

Core/services/validation_service.py
└── ValidationService         # UML Section 04 - Input validation
