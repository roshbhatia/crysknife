import copy
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


root = Path(__file__).resolve().parents[1]
source = root / "build/layout/outlines/key_preview.svg"
output = root / "build/layout/split_preview.svg"
ns = "http://www.w3.org/2000/svg"
ET.register_namespace("", ns)
layout = ET.parse(source).getroot()
x, y, width, height = map(float, layout.attrib["viewBox"].split())
padding = 10
gap = 30
canvas_width = 2 * width + gap + 2 * padding
canvas_height = height + 2 * padding
preview = ET.Element(f"{{{ns}}}svg", {
    "width": f"{canvas_width}mm",
    "height": f"{canvas_height}mm",
    "viewBox": f"0 0 {canvas_width} {canvas_height}",
})
ET.SubElement(preview, f"{{{ns}}}title").text = (
    "fridakeys: 42 wireless MX keys"
)
ET.SubElement(preview, f"{{{ns}}}rect", {
    "width": str(canvas_width), "height": str(canvas_height), "fill": "white",
})
transforms = [
    f"translate({padding - x} {padding - y})",
    f"translate({padding + 2 * width + gap + x} {padding - y}) scale(-1 1)",
]
for side, transform in zip(("left", "right"), transforms):
    group = ET.SubElement(preview, f"{{{ns}}}g", {"id": side, "transform": transform})
    for element in layout:
        item = copy.deepcopy(element)
        for child in item.iter():
            if "id" in child.attrib:
                child.attrib["id"] = f"{side}_{child.attrib['id']}"
        group.append(item)
ET.ElementTree(preview).write(output, encoding="unicode", xml_declaration=True)
print(f"Wrote {output.relative_to(root)}")
subprocess.run([
    "rsvg-convert", "--width", "1600", "--background-color", "white",
    "--output", str(output.with_suffix(".png")), str(output),
], check=True)
print(f"Wrote {output.with_suffix('.png').relative_to(root)}")
