

def group_metrics_with_subprefixes(metrics: list[str]) -> dict:
    """
    Group metrics with simple 2-level nested structure detection.

    Returns a dictionary where each prefix group can have:
    - direct_metrics: list of metrics at this level (e.g., "train/acc")
    - subgroups: dict of subgroup name -> list of metrics (e.g., "loss" -> ["train/loss/norm", "train/loss/unnorm"])

    Example:
        Input: ["loss", "train/acc", "train/loss/normalized", "train/loss/unnormalized", "val/loss"]
        Output: {
            "charts": {
                "direct_metrics": ["loss"],
                "subgroups": {}
            },
            "train": {
                "direct_metrics": ["train/acc"],
                "subgroups": {
                    "loss": ["train/loss/normalized", "train/loss/unnormalized"]
                }
            },
            "val": {
                "direct_metrics": ["val/loss"],
                "subgroups": {}
            }
        }
    """
    result = {}

    for metric in metrics:
        if "/" not in metric:
            if "charts" not in result:
                result["charts"] = {"direct_metrics": [], "subgroups": {}}
            result["charts"]["direct_metrics"].append(metric)
        else:
            parts = metric.split("/")
            main_prefix = parts[0]

            if main_prefix not in result:
                result[main_prefix] = {"direct_metrics": [], "subgroups": {}}

            if len(parts) == 2:
                result[main_prefix]["direct_metrics"].append(metric)
            else:
                subprefix = parts[1]
                if subprefix not in result[main_prefix]["subgroups"]:
                    result[main_prefix]["subgroups"][subprefix] = []
                result[main_prefix]["subgroups"][subprefix].append(metric)

    for group_data in result.values():
        group_data["direct_metrics"].sort()
        for subgroup_metrics in group_data["subgroups"].values():
            subgroup_metrics.sort()

    if "charts" in result and not result["charts"]["direct_metrics"]:
        del result["charts"]

    return result