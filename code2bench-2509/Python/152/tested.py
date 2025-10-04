def _parse_ethtool_unprefixed_queue_num(stat_name: str) -> tuple[str | None, str | None]:
    # Check if the stat name contains 'tx' or 'rx'
    if 'tx' in stat_name or 'rx' in stat_name:
        # Extract the queue number
        if 'tx' in stat_name:
            queue_prefix = 'tx'
        else:
            queue_prefix = 'rx'
        
        # Find the queue number
        queue_num = stat_name.split(queue_prefix)[1].split('_')[0]
        
        # Check if queue number is valid (only digits)
        if queue_num.isdigit():
            return f'queue:{queue_num}', stat_name.replace(queue_prefix, '').replace('_', '')
        else:
            return None, None
    else:
        return None, None