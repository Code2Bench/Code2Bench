
import urllib

def parse_specific_attributes(specific_attributes):
    assert isinstance(specific_attributes, str), "Specific attributes must be a string"
    parsed_specific_attributes = urllib.parse.parse_qsl(specific_attributes)
    return (
        {key: value for (key, value) in parsed_specific_attributes}
        if parsed_specific_attributes
        else dict()
    )