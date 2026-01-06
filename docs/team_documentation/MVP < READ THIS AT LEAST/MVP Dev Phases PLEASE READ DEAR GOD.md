## HOW DO WE DEVELOP THE MVP

READ THE FUCKING DOCUMENT OR I SWEAR TO GOD ILL HAND THIS SHIT IN MYSELF

Okay? Good. So since people are apparently confused on what we're doing, heres a minimal rundown.

### WHAT TO DO FIRST (now, if you didnt do it yet)

1. READ THE MVP_DEFINITION
Found under:
/home/violet/repos/WS2025-SE-Bellis-ev/docs/architecture/MVP_Definition.md
- There is NO point in working on stuff we dont even have in the MVP
- We will waste time while others (me) are overworked

2. SWITCH TO ANOTHER BRANCH AND PULL THE CURRENT REPO
- as i said multiple times, you should NOT be working on /main
- Go to the mvp branch. Pull the current sub-branch (/core_implementation/Gewalttat-Beratung)
- only then you can see what is being worked on

Here is a short tutorial. Just copy paste.
A) check your branch:               git branch -v
B) go to the branch you want:       git checkout mvp/core_implementation
c) pull the repo                    git pull origin cleanupmvp/core_implementation

3. READ and COMMUNICATE
- if you dont know where we are, or what you can do: Ask
- for real, we have a group chat

### DEVELOPMENT PHASES
Idk, i have roughly divided the process into the following phases (they changed over time)

Phase 1	    Data models (backend)    <------------ WE ARE HERE, ALMOST FINISHED
Phase 2	    Business logic (managers, validation)	
Phase 3A	Django Forms	                                    Edit forms here
Phase 3B	Views (CRUD operations)	                            Edit function here
Phase 3C	Templates (UI)	

These usually have sub-phases, but thats the general idea. I'll be taking Phase 1 and possible 2, but we neeeeeeed people for the UI


# NOTE: Current Phase 2 Planning

Phase 2A: Validation foundation -> needed so the rest can run smooth and safe
Phase 2B : FallManager -> core MVP functionality

