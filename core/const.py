from enum import Enum
from typing import (
    Final,
    List,
)

# Open API parameters
OPEN_API_TITLE: Final = "API Explorer"
OPEN_API_DESCRIPTION: Final = "API for explorer plugin"

# Messages constants
EXPLORER_TAGS: Final[List[str | Enum] | None] = ["AllInOne"]
EXPLORER_URL: Final = "/expl"
