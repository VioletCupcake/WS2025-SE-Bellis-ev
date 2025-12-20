============================================
### HOW TO PROPERLY USE GITHUB IN VSCODE ###
============================================

I am pretty sure i explained some of this in /architecture/MVP_DJANGO/Cheatsheets_And_Guides
But to be honest, i can not be bothered to check, so for anyone still unsure, here is a Step-By-Step guide.

### VIA CMD ###

## 01 - BEFORE WORK - PULL CURRENT STATE
Since we dont usually work on main, but on branches, and multiple people on one, you shoudl always pull first, so you avoid missing any updates other did.

git pull origin [BRANCH] 

# So for me it would be "git pull origin cleanup"

## 02 - AS YOU WORK 
Ideally you push and commit frequently when working a lot.
We will go through this, assuming you made multiple changes

# First Check what changed

git status

That will show you what changes are currently pending. 
New files will be listed as untracked, usually.

# Staging changes
There are multiple ways to stage changes you made. All involve the "git add" command.

Usually it makes sense to commit in stages. The following Options can be done in whatever order you think makes sense. But i did order them.

Option A: Commit internal changes, no new files

git add -u 

This updates the existing index, 

### VIA VSCODE ###