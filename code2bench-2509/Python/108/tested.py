from typing import List

def validate_and_extract_accelerator_classifiers(classifiers: List[str]) -> List[str]:
    valid_accelerators = {
        "GPU :: NVIDIA CUDA",
        "GPU :: AMD ROCm",
        "GPU :: Intel Arc",
        "NPU :: Huawei Ascend",
        "GPU :: Apple Metal"
    }
    
    result = []
    for classifier in classifiers:
        if classifier.startswith("Environment ::"):
            stripped_classifier = classifier[17:]
            if stripped_classifier in valid_accelerators:
                result.append(stripped_classifier)
    
    return result