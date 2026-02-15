"""
Food Scanner - Progress Module
Progress tracking utilities using tqdm
"""
from tqdm import tqdm


class ProgressTracker:
    """Wrapper for tqdm progress bars with custom formatting."""
    
    def __init__(self, total: int, desc: str = "Procesando", unit: str = "img"):
        """
        Initialize progress tracker.
        
        Args:
            total: Total number of items to process
            desc: Description for the progress bar
            unit: Unit name for items
        """
        self.total = total
        self.desc = desc
        self.unit = unit
        self.pbar = None
    
    def __enter__(self):
        """Create progress bar on context entry."""
        self.pbar = tqdm(
            total=self.total,
            desc=self.desc,
            unit=self.unit,
            ncols=80,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close progress bar on context exit."""
        if self.pbar:
            self.pbar.close()
    
    def update(self, n: int = 1):
        """
        Update progress by n steps.
        
        Args:
            n: Number of steps to advance
        """
        if self.pbar:
            self.pbar.update(n)
    
    def set_description(self, desc: str):
        """
        Update the description.
        
        Args:
            desc: New description
        """
        if self.pbar:
            self.pbar.set_description(desc)
    
    def set_postfix(self, **kwargs):
        """
        Set postfix information.
        
        Args:
            **kwargs: Key-value pairs to display
        """
        if self.pbar:
            self.pbar.set_postfix(**kwargs)


def create_progress_bar(total: int, desc: str = "Procesando", unit: str = "img"):
    """
    Factory function to create a progress bar.
    
    Args:
        total: Total number of items
        desc: Description text
        unit: Unit name
        
    Returns:
        tqdm progress bar
    """
    return tqdm(
        total=total,
        desc=desc,
        unit=unit,
        ncols=80,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    )
