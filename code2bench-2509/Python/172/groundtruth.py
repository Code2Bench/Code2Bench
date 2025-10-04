from typing import List, Tuple

def _parse_n_check_triples(triples_str: str) -> List[Tuple[str, str, str]]:
    # use pythonic checks for triples
    processed = []
    split_by_newline = triples_str.split("\n")
    # sometimes LLM fails to obey the prompt
    if len(split_by_newline) > 1:
        split_triples = split_by_newline
        llm_obeyed = True
    else:
        # handles form "(e, r, e) (e, r, e) ... (e, r, e)""
        split_triples = triples_str[1:-1].split(") (")
        llm_obeyed = False
    for triple_str in split_triples:
        try:
            if llm_obeyed:
                # remove parenthesis and single quotes for parsing
                triple_str = triple_str.replace("(", "").replace(")",
                                                                 "").replace(
                                                                     "'", "")
            split_trip = triple_str.split(',')
            # remove blank space at beginning or end
            split_trip = [(i[1:] if i[0] == " " else i) for i in split_trip]
            split_trip = [(i[:-1].lower() if i[-1] == " " else i)
                          for i in split_trip]
            potential_trip = tuple(split_trip)
        except:  # noqa
            continue
        if 'tuple' in str(type(potential_trip)) and len(
                potential_trip
        ) == 3 and "note:" not in potential_trip[0].lower():
            # additional check for empty node/edge attrs
            if potential_trip[0] != '' and potential_trip[
                    1] != '' and potential_trip[2] != '':
                processed.append(potential_trip)
    return processed