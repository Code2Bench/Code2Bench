from typing import Any

def _build_command_line_options(test_options: dict[str, Any]) -> list:
    """Helper function to build command-line options from the test options dictionary."""
    additional_options = []

    for key, value in test_options.items():
        if isinstance(value, bool):
            # Default behavior expecting argparse.BooleanOptionalAction support
            additional_options.append(f"--{'no-' if not value else ''}{key.replace('_', '-')}")
        elif isinstance(value, list):
            additional_options.extend([f"--{key.replace('_', '-')}"] + [str(v) for v in value])
        else:
            # Just add --key value
            additional_options.extend(["--" + key.replace("_", "-"), str(value)])

    return additional_options