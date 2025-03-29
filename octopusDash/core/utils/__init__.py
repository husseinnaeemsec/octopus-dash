
class DictToObject:
    def __init__(self,data:dict):
        for key,val in data.items():
            if not hasattr(self,key):
                setattr(self,key,val)


def convert_size(size_bytes):
    """
    Convert bytes to MB or GB based on the size.
    """
    if size_bytes < 1024 * 1024:  # Less than 1 MB
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:  # Less than 1 GB
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:  # 1 GB or more
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def convert_size_to_mb(size_str:str):
    """
    Convert size strings like "1.23 MB" or "0.45 GB" to numeric values in MB.
    """
    if 'KB' in size_str:
        return float(size_str.replace(' KB', '')) / 1024
    elif 'MB' in size_str:
        return float(size_str.replace(' MB', ''))
    elif 'GB' in size_str:
        return float(size_str.replace(' GB', '')) * 1024
    return 0.0