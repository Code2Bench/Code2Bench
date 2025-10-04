import re
import copy

def SubstituteTemplate(template: str, values_base: dict) -> str:
    values = copy.deepcopy(values_base)
    for key in list(values.keys()):
        if key in ["KernelSchedule", "EpilogueSchedule"] and "Auto" in key:
            values[key] = "collective::" + key
    while True:
        match = re.search(r'\{([^{}]+)\}', template)
        if not match:
            break
        placeholder = match.group(1)
        if placeholder in values:
            template = template.replace(f'{{{placeholder}}}', str(values[placeholder]))
    return template