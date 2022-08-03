from __future__ import annotations

from typing import ClassVar

class Setup:
    DCR_VERSION: ClassVar[str]
    ENVIRONMENT_TYPE_DEV: ClassVar[str]
    ENVIRONMENT_TYPE_PROD: ClassVar[str]
    ENVIRONMENT_TYPE_TEST: ClassVar[str]
    PDF2IMAGE_TYPE_JPEG: ClassVar[str]
    PDF2IMAGE_TYPE_PNG: ClassVar[str]

    pdf2image_type: ClassVar[str]

    def __init__(self) -> None:
        self.is_irregular_footer = None
        ...
    def exists(self) -> bool: ...
