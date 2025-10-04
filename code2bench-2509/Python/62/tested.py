from typing import List, Dict, Any

def get_messages_summary(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not messages:
        return {'total': 0, 'by_type': {}, 'by_model': {}, 'total_tokens': 0}

    total = len(messages)
    by_type = {}
    by_model = {}
    total_tokens = 0

    for message in messages:
        type_key = message['type']
        model_key = message['model']
        tokens = message['tokens']

        by_type[type_key] = by_type.get(type_key, 0) + 1
        by_model[model_key] = by_model.get(model_key, 0) + 1

        total_tokens += tokens['input'] + tokens['output']

    return {
        'total': total,
        'by_type': by_type,
        'by_model': by_model,
        'total_tokens': total_tokens
    }