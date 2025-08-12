"""Prompt template for an optional LLM hook.

This file defines a Jinja2 template that can be used to generate a
prompt for a Large Language Model (LLM) based on the student profile
and preliminary recommendations produced by the rule‑based engine.  The
current application does **not** call any external LLM; the prompt
template is provided purely for future extension.
"""
from jinja2 import Template


PROMPT_TEMPLATE = Template(
    """Student Profile:\n"
    "  Name: {{ student.name }}\n"
    "  Year Level: {{ student.yearLevel }}\n"
    "  Interests: {{ student.interests | join(', ') }}\n"
    "  Strengths: {{ student.strengths | join(', ') }}\n"
    "  Academic Performance: {{ student.academicPerformance }}\n\n"
    "Preliminary Recommendations:\n"
    "{% for rec in recommendations %}"
    "  - {{ rec.name }} (confidence: {{ '%.2f' % rec.confidence }})\n"
    "    Why: {{ rec.why }}\n"
    "    Suggested Subjects: {{ rec.suggestedSubjects | join(', ') }}\n"
    "    VET Options: {{ rec.vetOptions | join(', ') }}\n"
    "{% endfor %}\n\n"
    "Task:\n"
    "Based on the student's profile and the preliminary recommendations, "
    "suggest refined career pathways and personalised next steps. "
    "Provide a short paragraph explaining the reasoning for each suggestion "
    "and highlight any potential subject areas or extracurricular activities "
    "that could enhance the student's preparation."
)