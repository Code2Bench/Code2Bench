from typing import List

from typing import List, Optional

def get_required_actions(step_number: int, confidence: str, findings: str, total_steps: int, request=None) -> List[str]:
    actions = []

    if step_number == 1:
        actions.extend(
            [
                "Begin systematic thinking analysis",
                "Identify key aspects and assumptions to explore",
                "Establish initial investigation approach",
            ]
        )
    elif confidence == "low":
        actions.extend(
            [
                "Continue gathering evidence and insights",
                "Test initial hypotheses",
                "Explore alternative perspectives",
            ]
        )
    elif confidence == "medium":
        actions.extend(
            [
                "Deepen analysis of promising approaches",
                "Validate key assumptions",
                "Consider implementation challenges",
            ]
        )
    elif confidence == "high":
        actions.extend(
            [
                "Refine and validate key findings",
                "Explore edge cases and limitations",
                "Document assumptions and trade-offs",
            ]
        )
    elif confidence == "very_high":
        actions.extend(
            [
                "Synthesize findings into cohesive recommendations",
                "Validate conclusions against all evidence",
                "Prepare comprehensive implementation guidance",
            ]
        )
    elif confidence == "almost_certain":
        actions.extend(
            [
                "Finalize recommendations with high confidence",
                "Document any remaining minor uncertainties",
                "Prepare for expert analysis or implementation",
            ]
        )
    else:  # certain
        actions.append("Analysis complete - ready for implementation")

    return actions