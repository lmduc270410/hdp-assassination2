#!/usr/bin/env python3
"""
obsidian_graph_exporter.py

Read a graph JSON file and export an Obsidian Canvas (.canvas) file.

Input JSON format:
{
  "nodes": [
    {
      "id": "p1314",
      "label": "P1314",
      "type": "note",              // "note" or "text"
      "file": "Problems/P1314.md", // required for type="note"
      "x": 0, "y": 0,
      "width": 320, "height": 140
    }
  ],
  "edges": [
    {
      "from": "p1314",
      "to": "p4552",
      "label": "same idea"
    }
  ]
}

Run:
  python3 obsidian_graph_exporter.py graph.json output.canvas
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def canvas_node_id(kind: str, node_id: str) -> str:
    return f"{kind}:{node_id}"


def build_canvas(graph: Dict[str, Any]) -> Dict[str, Any]:
    canvas_nodes: List[Dict[str, Any]] = []
    canvas_edges: List[Dict[str, Any]] = []

    # Helpful default layout
    x_cursor = 0
    y_cursor = 0
    col = 0

    for n in graph.get("nodes", []):
        node_id = str(n["id"])
        label = n.get("label", node_id)
        kind = n.get("type", "note")
        x = n.get("x")
        y = n.get("y")
        width = n.get("width", 320)
        height = n.get("height", 140)

        if x is None or y is None:
            x = x_cursor
            y = y_cursor
            col += 1
            x_cursor += 420
            if col % 4 == 0:
                x_cursor = 0
                y_cursor += 220

        if kind == "text":
            canvas_nodes.append({
                "id": canvas_node_id("text", node_id),
                "type": "text",
                "text": label,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
            })
        else:
            file_path = n.get("file")
            if not file_path:
                raise ValueError(f"Node {node_id} has type='note' but no 'file' field.")
            canvas_nodes.append({
                "id": canvas_node_id("file", node_id),
                "type": "file",
                "file": file_path,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
            })

    for e in graph.get("edges", []):
        src = str(e["from"])
        dst = str(e["to"])
        edge_id = e.get("id", f"{src}__{dst}")
        canvas_edges.append({
            "id": canvas_node_id("edge", str(edge_id)),
            "type": "edge",
            "fromNode": canvas_node_id("file", src) if not str(src).startswith("text:") else src,
            "toNode": canvas_node_id("file", dst) if not str(dst).startswith("text:") else dst,
            "label": e.get("label", ""),
            "labelStyle": "inline",
            "color": e.get("color", "default"),
        })

    return {
        "nodes": canvas_nodes + canvas_edges
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 obsidian_graph_exporter.py input.json output.canvas", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    graph = json.loads(input_path.read_text(encoding="utf-8"))
    canvas = build_canvas(graph)
    output_path.write_text(json.dumps(canvas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
