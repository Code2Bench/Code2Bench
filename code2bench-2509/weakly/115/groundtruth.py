
import re
import copy

def SubstituteTemplate(template, values_base):
    """ """
    values = copy.deepcopy(values_base)
    if values.get("KernelSchedule") is not None and "Auto" in values["KernelSchedule"]:
        values["KernelSchedule"] = "collective::" + values["KernelSchedule"]
    if values.get("EpilogueSchedule") is not None and "Auto" in values["EpilogueSchedule"]:
        values["EpilogueSchedule"] = "collective::" + values["EpilogueSchedule"]
    text = template
    changed = True
    while changed:
        changed = False
        for key, value in values.items():
            regex = f"\\{{{key}\\}}"
            newtext = re.sub(regex, value, text)
            if newtext != text:
                changed = True
            text = newtext
    return text