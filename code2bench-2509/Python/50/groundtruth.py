from typing import Any, Dict, List

def default_get_group_data_meta_info(temp_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Default implementation for getting meta information about the temporary data
    collected between get_batch calls.
    """
    if not temp_data:
        return {
            "total_samples": 0,
            "num_groups": 0,
            "avg_group_size": 0,
            "avg_reward": 0,
        }

    meta_info = {"total_samples": 0, "num_groups": len(temp_data)}

    all_rewards = []
    # Calculate per-group statistics
    for instance_id, samples in temp_data.items():
        group_size = len(samples)
        group_rewards = [s["reward"] for s in samples]  # Calculate group reward standard deviation
        meta_info["total_samples"] += group_size
        all_rewards.extend(group_rewards)
    # Calculate global statistics
    meta_info["avg_group_size"] = meta_info["total_samples"] / meta_info["num_groups"]

    if all_rewards:
        meta_info["avg_reward"] = sum(all_rewards) / len(all_rewards)
    else:
        meta_info["avg_reward"] = 0
    return meta_info