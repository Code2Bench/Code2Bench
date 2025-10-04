from datetime import datetime

def ds_format(ds: str, input_format: str, output_format: str) -> str:
    dt = datetime.strptime(ds, input_format)
    return dt.strftime(output_format)