def get_gpu_num(model_name: str) -> int:
    # Convert model name to lowercase for case-insensitive matching
    model_name = model_name.lower()
    
    # Predefined mapping of GPU counts to keywords
    gpu_mapping = {
        8: ["gpu", "gpus", "gpu8", "gpus8"],
        16: ["gpu2", "gpus2", "gpu16", "gpus16"],
        32: ["gpu4", "gpus4", "gpu32", "gpus32"],
        64: ["gpu8", "gpus8", "gpu64", "gpus64"]
    }
    
    # Iterate through the mapping in descending order of GPU counts
    for count, keywords in gpu_mapping.items():
        for keyword in keywords:
            if keyword in model_name:
                return count
    
    # Default to 8 GPUs if no match is found
    return 8