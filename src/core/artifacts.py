# Helper function to generate timestamped output folder
import datetime
import os

class ArtifactOutput:
    """Class to manage artifact output paths."""
    def __init__(self, base_folder):
        self.base_folder = base_folder
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def get_base_output_path(self):
        """Get full output path for a given relative path."""
        return os.path.join("outputs", self.timestamp)


