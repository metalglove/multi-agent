# Helper function to generate timestamped output folder
from datetime import datetime
import os


class ArtifactOutput:
    """Class to manage artifact output paths."""
    def __init__(self, base_folder: str = "outputs"):
        # Normalize and make absolute the base folder path
        self.base_folder = os.path.abspath(os.path.normpath(base_folder))
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def get_base_output_path(self) -> str:
        """Get full output path for a given relative path."""
        path = os.path.join(self.base_folder, self.timestamp)
        return os.path.normpath(path)


