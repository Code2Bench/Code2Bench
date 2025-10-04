from typing import Dict, Optional, Tuple


from typing import Dict, Optional, Tuple

def get_contest_data_from_cache(contest_id: int, cached_data: Dict) -> Tuple[Optional[Dict], Optional[Dict]]:
    contest_id_str = str(contest_id)

    if contest_id_str not in cached_data:
        print(f"Warning: Contest {contest_id} data not found in cache")
        return None, None

    contest_data = cached_data[contest_id_str]

    try:
        standings = contest_data["standings"]
        rating_changes = contest_data["rating_changes"]

        if standings.get("status") != "OK" or rating_changes.get("status") != "OK":
            print(f"Warning: Contest {contest_id} cached data status abnormal")
            return None, None

        return standings, rating_changes

    except KeyError as e:
        print(f"Warning: Contest {contest_id} cached data structure abnormal: {e}")
        return None, None