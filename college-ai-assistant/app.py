import os
import json

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from tools import (
    calculator,
    mark_attendance,
    timetable_analysis
)

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

MODEL = "openai/gpt-oss-120b"

tools = [

    {
        "type": "function",

        "function": {
            "name": "calculator",

            "description":
                "Calculate mathematical expressions "
                "including attendance percentages.",

            "parameters": {
                "type": "object",

                "properties": {
                    "expression": {
                        "type": "string",
                        "description":
                            "Mathematical expression to calculate."
                    }
                },

                "required": ["expression"]
            }
        }
    },


    {
        "type": "function",

        "function": {
            "name": "mark_attendance",

            "description":
                "Mark a student's attendance for a "
                "particular date and subject.",

            "parameters": {
                "type": "object",

                "properties": {

                    "student_id": {
                        "type": "string"
                    },

                    "date": {
                        "type": "string",
                        "description":
                            "Date in YYYY-MM-DD format."
                    },

                    "subject": {
                        "type": "string"
                    },

                    "status": {
                        "type": "string",
                        "enum": [
                            "present",
                            "absent"
                        ]
                    }
                },

                "required": [
                    "student_id",
                    "date",
                    "subject",
                    "status"
                ]
            }
        }
    },


    {
        "type": "function",

        "function": {
            "name": "timetable_analysis",

            "description":
                "Analyze an uploaded college timetable "
                "and answer timetable questions.",

            "parameters": {
                "type": "object",

                "properties": {

                    "question": {
                        "type": "string"
                    },

                    "document_text": {
                        "type": "string"
                    }
                },

                "required": [
                    "question",
                    "document_text"
                ]
            }
        }
    }
]

SYSTEM_PROMPT = """
You are a College AI Assistant.

Your responsibilities are:

1. Analyze college timetables.
2. Calculate mathematical values.
3. Calculate attendance percentages.
4. Mark student attendance.

Tool rules:

- If the student asks for an attendance percentage,
  ALWAYS use the calculator tool.

- If the student asks to calculate any mathematical value,
  use the calculator tool.

- If the student asks to mark attendance for a particular
  day and subject, use the attendance tool.

- If the student asks about their timetable and a timetable
  document is available, use the timetable_analysis tool.

- Never claim that attendance was marked unless the
  attendance tool was successfully executed.

- Always mention the tool used in the final response.

Be concise and helpful.
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },

    {
        "role": "user",
        "content": "What is my attendance percentage if I attended 45 out of 60 classes?"
    }
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

print(message)

if message.tool_calls:

    for tool_call in message.tool_calls:

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        if function_name == "calculator":

            result = calculator(
                arguments["expression"]
            )

        elif function_name == "mark_attendance":

            result = mark_attendance(
                arguments["student_id"],
                arguments["date"],
                arguments["subject"],
                arguments["status"]
            )

        elif function_name == "timetable_analysis":

            result = timetable_analysis(
                arguments["question"],
                arguments["document_text"]
            )

        print("Tool used:", function_name)
        print("Tool result:", result)

