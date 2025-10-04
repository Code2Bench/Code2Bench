

def compute_method_ranks(data, selected_models=None, selected_data=None):
    """
    Compute, for each metric, the rank of each model (1 = best accuracy).

    Args:
        data (List[Dict]): your JSON‐like list of dicts.
        selected_models (List[str], optional):
            List of clean model names (with "_temp0_n1_seed2" already stripped)
            whose ranks you care about.  If None, returns ranks for _all_ models.
        selected_data (List[str], optional):
            List of metric names _without_ the "_acc" suffix.  If None,
            defaults to all keys ending in "_acc" except "avg_acc".

    Returns:
        Dict[str, Dict[str,int]]:  
            Outer: metric →  
            Inner: model_name → rank (1 = highest accuracy)
    """
    # 1. Determine which metrics to rank
    if selected_data is None:
        selected_data = sorted(
            k[:-4] for k in data[0].keys()
            if k.endswith("_acc") and k != "avg_acc"
        )

    # 2. Prepare clean model names + parsed accuracies
    models = []
    for item in data:
        clean_name = item["model"].replace("_temp0_n1_seed2", "")
        models.append((clean_name, item))

    # 3. For each metric, sort and assign ranks
    all_ranks = {}
    for metric in selected_data:
        key = f"{metric}_acc"
        # build list of (model, float(acc))
        vals = [
            (name, float(item.get(key, 0.0)))
            for name, item in models
        ]
        # sort desc by accuracy
        vals.sort(key=lambda x: x[1], reverse=True)
        # assign ranks (1-based). Ties get the same rank.
        ranks = {}
        prev_score = None
        prev_rank = 0
        for idx, (name, score) in enumerate(vals, start=1):
            if score == prev_score:
                rank = prev_rank
            else:
                rank = idx
            ranks[name] = rank
            prev_score, prev_rank = score, rank

        # if user only wants a subset, filter
        if selected_models is not None:
            ranks = {m: ranks[m] for m in selected_models if m in ranks}

        all_ranks[metric] = ranks

    return all_ranks