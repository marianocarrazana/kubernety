import json
from typing import Any, Literal
from rich.console import Console
from rich.syntax import Syntax
import yaml

console = Console()


def var_dump(obj: Any, syntax: Literal["json", "yaml"] = "yaml"):
    if syntax == "yaml":
        text_obj = yaml.safe_dump(obj, indent=2)
    elif syntax == "json":
        text_obj = json.dumps(obj, default=str, indent=2)
    out = Syntax(text_obj, syntax, theme="ansi_dark")
    console.print(out)
