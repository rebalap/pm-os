Activate the Researcher agent to create a validation plan for: $ARGUMENTS

Before planning, confirm:
1. Which product and feature are we validating?
2. What is the core assumption we need to test? (Be specific)
3. What would "validated" look like — what evidence would give us confidence to proceed?
4. What is the consequence of being wrong? (Informs how rigorous to be)

Then produce a Validation Plan using the template at @docs/templates/validation-plan-template.md.

The plan must include:
- The specific hypothesis being tested (falsifiable)
- The chosen validation method with rationale
- Recruitment criteria for participants
- Success/failure criteria defined in advance
- What we will do if the assumption is invalidated

Rules:
- Validation must happen before significant engineering investment
- A hypothesis must be falsifiable — if you can't define failure, it's not a hypothesis
- Prefer lightweight methods (5 user interviews, prototype test) over surveys for qualitative unknowns
- If the argument is vague, ask what assumption needs validating before proceeding
