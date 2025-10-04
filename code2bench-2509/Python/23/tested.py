def normalize_model_name(model: str) -> str:
    # Convert to lowercase
    model = model.lower()
    
    # Replace spaces with hyphens
    model = model.replace(" ", "-")
    
    # Handle specific normalization rules
    if "-" in model and model.endswith("-20240229"):
        model = model[:-10]  # Remove the date part
    
    return model