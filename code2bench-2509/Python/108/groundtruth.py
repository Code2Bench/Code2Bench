

def validate_and_extract_accelerator_classifiers(classifiers: list) -> list:
    accelerator_classifiers = [c for c in classifiers if c.startswith("Environment ::")]
    if not accelerator_classifiers:
        return []

    accelerator_values = [c[len("Environment :: ") :] for c in accelerator_classifiers]

    valid_accelerators = {
        "GPU :: NVIDIA CUDA",
        "GPU :: AMD ROCm",
        "GPU :: Intel Arc",
        "NPU :: Huawei Ascend",
        "GPU :: Apple Metal",
    }

    for accelerator_value in accelerator_values:
        if accelerator_value not in valid_accelerators:
            return []

    return accelerator_values