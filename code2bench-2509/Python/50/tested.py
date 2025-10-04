from typing import Dict, List, Any

def default_get_group_data_meta_info(temp_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    total_samples = 0
    num_groups = 0
    avg_group_size = 0.0
    avg_reward = 0.0

    for group in temp_data.values():
        total_samples += len(group)
        num_groups += 1
        avg_group_size = total_samples / num_groups if num_groups > 0 else 0.0

        # Calculate average reward
        reward_sum = 0.0
        for sample in group:
            reward_sum += sample.get('reward', 0)
        avg_reward = reward_sum / total_samples if total_samples > 0 else 0.0

    # If input is empty, return all values set to 0
    if not temp_data:
        return {
            'total_samples': 0,
            'num_groups': 0,
            'avg_group_size': 0.0,
            'avg_reward': 0.0
        }

    return {
        'total_samples': total_samples,
        'num_groups': num_groups,
        'avg_group_size': avg_group_size,
        'avg_reward': avg_reward
    }