# app/services/mock_database.py

# This is our local, in-memory "database" of questions.
# It mimics the structure of our Supabase table.
mock_questions = [
    {
        "id": 1,
        "category": "Foundations & Shortcuts",
        "question_text": "What is the keyboard shortcut to lock a cell reference in a formula (e.g., from A1 to $A$1)?",
        "question_type": "mcq",
        "options": ["F2", "F4", "F9", "Ctrl+L"],
        "correct_answer": "F4",
        "ideal_answer": "The correct shortcut is F4. Pressing it cycles through relative, absolute, and mixed references ($A$1, A$1, $A1, A1).",
        "difficulty": 1,
        "marks": 2
    },
    {
        "id": 2,
        "category": "Foundations & Shortcuts",
        "question_text": "Which function would you use to count cells that meet a single, specific criterion?",
        "question_type": "mcq",
        "options": ["COUNT", "COUNTA", "COUNTIF", "COUNTIFS"],
        "correct_answer": "COUNTIF",
        "ideal_answer": "The COUNTIF function is used to count cells within a range that meet a single given condition. COUNTIFS is used for multiple criteria.",
        "difficulty": 1,
        "marks": 2
    },
    {
        "id": 3,
        "category": "Formulas & Functions",
        "question_text": "Explain the main difference between the SUMIF and SUMIFS functions.",
        "question_type": "open_ended",
        "options": None,
        "correct_answer": None,
        "ideal_answer": "The main difference is the number of conditions they handle. SUMIF sums values based on a single criterion, while SUMIFS can handle multiple criteria across different ranges. Their argument syntax is also different; in SUMIFS, the sum range comes first, which is more logical and consistent.",
        "difficulty": 2,
        "marks": 5
    },
    {
        "id": 4,
        "category": "Data Management",
        "question_text": "I have a large table of sales data. What is the best feature in Excel to quickly summarize this data, for example, to see total sales per region and per product category?",
        "question_type": "open_ended",
        "options": None,
        "correct_answer": None,
        "ideal_answer": "The best feature for this task is a PivotTable. A PivotTable is an interactive tool that allows you to quickly summarize, group, and analyze large datasets. You can drag and drop fields into the Rows, Columns, and Values areas to create a dynamic summary report without writing any formulas.",
        "difficulty": 3,
        "marks": 5
    }
]

def get_question(question_id: int):
    """Fetches a single question by its ID from the mock list."""
    for q in mock_questions:
        if q['id'] == question_id:
            return q
    return None

def get_questions_by_stage(stage: int):
    """Fetches all question IDs for a specific stage from the mock list."""
    question_type = 'mcq' if stage == 1 else 'open_ended'
    return [q['id'] for q in mock_questions if q['question_type'] == question_type]