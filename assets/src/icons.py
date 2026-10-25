"""Shared helper: inline an icon from icons/ as a data URI (lucide icons recoloured)."""
import base64, pathlib

def icon_uri(name, color="#0f172a"):
    p = next(pathlib.Path(__file__).parent.joinpath("icons").glob(name + ".*"))
    data = p.read_bytes()
    if p.suffix == ".svg":
        return "data:image/svg+xml;base64," + base64.b64encode(data.replace(b"currentColor", color.encode())).decode()
    return "data:image/png;base64," + base64.b64encode(data).decode()
