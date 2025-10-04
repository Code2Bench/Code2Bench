

def _parse_ethtool_unprefixed_queue_num(stat_name):
    """
    Extract the queue and the metric name from ethtool stat name:
    tx0_bytes -> (queue:0, tx_bytes)
    rx1_packets -> (queue:1, rx_packets)
    """
    if 'rx' not in stat_name and 'tx' not in stat_name:
        return None, None
    parts = stat_name.split('_')
    queue_num = None
    queue_index = None
    for i, part in enumerate(parts):
        if not part.startswith('tx') and not part.startswith('rx'):
            continue
        if part[2:].isdigit():
            queue_num = part[2:]
            queue_index = i
            break
    if queue_num is None or not queue_num.isdigit():
        return None, None
    parts[queue_index] = parts[queue_index][:2]
    return 'queue:{}'.format(queue_num), '_'.join(parts)