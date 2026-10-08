from datetime import datetime


def calculator(expression: str):
    """
    Calculate a mathematical expression.

    Args:
        expression: Mathematical expression to calculate.
    """

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return {
            "result": result,
            "tool_used": "calculator"
        }

    except Exception as e:
        return {
            "error": str(e),
            "tool_used": "calculator"
        }


def mark_attendance(
    student_id: str,
    date: str,
    subject: str,
    status: str
):
    """
    Mark attendance for a student.

    Args:
        student_id: Student ID.
        date: Attendance date in YYYY-MM-DD format.
        subject: Subject name.
        status: present or absent.
    """

    return {
        "student_id": student_id,
        "date": date,
        "subject": subject,
        "status": status,
        "message": f"Attendance marked {status} for {subject} on {date}.",
        "tool_used": "attendance"
    }


def timetable_analysis(question: str, document_text: str):
    """
    Analyze an uploaded college timetable.

    Args:
        question: Student's timetable question.
        document_text: Extracted timetable text.
    """

    return {
        "question": question,
        "timetable": document_text,
        "tool_used": "timetable_analysis"
    }