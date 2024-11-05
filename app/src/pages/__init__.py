from .page1 import Page1
from .page2 import Page2
from .page3 import Page3
from ..utils.utils import Page

from typing import Dict, Type


PAGE_MAP: Dict[str, Type[Page]] = {
    "Black Scholes": Page1,
    "Monte Carlo": Page2,
    "Binominal": Page3
}

__all__ = ["PAGE_MAP"]