# Style Guidelines for the Python Project

| Category | Style |
| :---- | :---- |
| Variables and Parameters | snake_case (e.g., user_name, total_count) |
| Functions / Methods | PascalCase (e.g., ComputeResult(), ProcessData()). Exception: getters/setters can also use snake_case |
| Types / Classes / Enums / Aliases | PascalCase (e.g., MyClass, UserProfile) |
| Constants / Globally Visible Constants | kPascalCase |
| File / Module Name | snake_case |

---

## Code Organization & Structure

**Modular Structure:**  
Divide code into manageable modules/files, where each module has a clearly defined content. Avoid unnecessarily large files to maintain readability.

**Logical Grouping:**  
Within a module, related elements (e.g., classes, functions, constants) should be grouped logically.

**Clear Interfaces:**  
For public/exported functions and classes, it should be clear what belongs to the API and what is internal (e.g., private helper functions or helper classes).

**Minimal Dependencies:**  
Each file/module should import only the dependencies it actually needs — avoid “transitive imports” just because another file might use them. This improves clarity and reduces side effects during refactoring.

---

## Comments & Documentation

**Self-documenting code over excessive comments:**  
Good names for variables, functions, etc., are often more helpful than long comments.

**Comments where they add value:**  
Especially for complex behavior, unexpected quirks, or side-effect-heavy operations — document what the code does and why.

**Consistent comment style:**  
Choose one type of comment (`# …` for Python) and use it consistently. Comments should be written in complete, readable sentences with standard capitalization.