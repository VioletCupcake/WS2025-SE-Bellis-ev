## ============================================================================
## ETENSIVE STRUCTURE OVERHAUL - ARCHITECTURE DOCUMENTATION
## ============================================================================

## SO WHAT DID I DO?
## 
## - I restructured the entire codebase to follow a clear, consistent architecture. (or well, i tried to)
## - I created distinct layers for different responsibilities: Data Models, Business Logic, and User Interface. 
## - I defined clear relationships between entities using UML notation for better clarity. 
## - I established coding standards and conventions to ensure consistency across the codebase.(idk its a lot)
##
## SO WHAT IS WHERE?
## - I have organised this whole shit into 3 Seperate folders
## - Each Folder contains:  - A clean, full UML Document with minimal comments
##                          - Visualisation by converting these Things into PlantUML syntax and generating images
## The Folders:
## 1)   Full UML - here you have a full UML, with everything the program should needs
## 2)   MVP UML - here you have just the functions that i think should be part of the MVP
## 3)   UML Mapped to Django - Since we are using Django, a lot of elements can be implemented in much simpler means.
## The goal being that you can understand how which of these functions translate into Django, and how to implement it.



## ============================================================================
## CODING STANDARDS & CONVENTIONS
## ============================================================================
## 
## LANGUAGE STRATEGY 
## - I implemented an approach where domain-specific terms are in German, 
##   while technical and operational terms are in English. This balances clarity when we reference specifically needed
##   fields from the Statistik-Bogen while making the rest of the codebase still work with common english naming conventions.
## NAMING CONVENTIONS
## - Domain Entities & Attributes: German terminology for fields mapping directly to B-EV  
##   domain knowledge (e.g., Beratung, Gewalttat, Folgen). Preserves accuracy when referring to specific words/requirements, where translation might cause issues 
 ## - Technical Components: English for platform-agnostic elements (e.g., User, AuditLog, Session, Manager classes). 
## - Methods: English verb forms for all operations (e.g., save(), edit(), validate()).  
## - Class Names: PascalCase. Attributes: snake_case. Methods: camelCase. 

## ## EXAMPLE: 
## Fall:  ## German domain entity 
## - fall_id : string  ## German attribute 
## - erstellungsdatum : date 
## + save() : boolean  ## English method 
## + addConsultation() : Beratung`


## ============================================================================
## RELATIONSHIP DEFINITIONS
## ============================================================================
## Understanding UML Relationship Notation:
##
## MULTIPLICITY (CARDINALITY):
## - "1" = Exactly one
## - "0..1" = Zero or one (optional)
## - "*" = Zero or many
## - "1..*" = One or many (at least one required)
##
## RELATIONSHIP TYPES:
## - -- (solid line) = Association (general relationship)
## - --> (solid arrow) = Directed association (one-way navigation)
## - <|-- (hollow arrow) = Inheritance/Generalization
## - <>-- (diamond) = Aggregation (weak ownership)
## - <>== (filled diamond) = Composition (strong ownership, lifecycle dependency)
##
## EXAMPLES:
## - User "1" -- "*" Fall = One User relates to many Fälle
## - Fall "1" <>== "*" Beratung = One Fall strongly owns many Beratungen 
##   (deleting Fall cascades to delete all Beratungen)