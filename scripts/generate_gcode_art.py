#!/usr/bin/env python3
"""
G-Code Generator Utility
1. Generates GitHub Markdown 'gcode' syntax-highlighted ASCII text banners for README.md.
2. Converts SVG vector shapes into CNC / Pen Plotter G-code toolpath files (.gcode).

Usage:
  # Generate ASCII gcode banner for text (default: "1pvq1")
  python scripts/generate_gcode_art.py banner "1pvq1"

  # Convert an SVG file into a plotter G-code file
  python scripts/generate_gcode_art.py svg assets/activity-radar.svg output.gcode
"""

import sys
import os
import re
import xml.etree.ElementTree as ET

# Built-in ASCII Font dictionary (5-line high block characters)
FONT_ASCII = {
    '1': ["  __ ", " /  |", " |  |", " |  |", " |__|"],
    'p': ["  ____  ", " |  _ \\ ", " | |_) |", " |  __/ ", " |_|    "],
    'v': [" __     __", " \\ \\   / /", "  \\ \\ / / ", "   \\ V /  ", "    \\_/   "],
    'q': ["   ___  ", "  / _ \\ ", " | | | |", " | |_| |", "  \\__\\_\\"],
    'a': ["   ___  ", "  / _ \\ ", " / /_\\ \\", "/ /_  _\\", "\\_/ \\_/ "],
    'b': ["  ____  ", " |  _ \\ ", " | _ <  ", " | |_) |", " |____/ "],
    'c': ["   ___  ", "  / _ \\ ", " | | | |", " | |_| |", "  \\___/ "],
    'd': ["  ____  ", " |  _ \\ ", " | | | |", " | |_| |", " |____/ "],
    'e': ["  _____ ", " |  ___|", " | |___ ", " |  ___|", " |_____|"],
    'f': ["  _____ ", " |  ___|", " | |_   ", " |  _|  ", " |_|    "],
    'g': ["   ___  ", "  / _ \\ ", " | | _  ", " | |_| |", "  \\___/ "],
    'h': ["  _   _ ", " | | | |", " | |_| |", " |  _  |", " |_| |_|"],
    'i': ["  ___ ", " |_ _|", "  | | ", "  | | ", " |___|"],
    'j': ["     _ ", "    | |", " _  | |", "| |_| |", " \\___/ "],
    'k': ["  _  __", " | |/ /", " | ' < ", " | .  \\\\", " |_|\\_\\\\"],
    'l': ["  _    ", " | |   ", " | |   ", " | |___", " |_____|"],
    'm': ["  __  __ ", " |  \\/  |", " | |\\/| |", " | |  | |", " |_|  |_|"],
    'n': ["  _   _ ", " | \\ | |", " |  \\| |", " | |\\  |", " |_| \\_|"],
    'o': ["   ___  ", "  / _ \\ ", " | | | |", " | |_| |", "  \\___/ "],
    'r': ["  ____  ", " |  _ \\ ", " | |_) |", " |  _ < ", " |_| \\_\\\\"],
    's': ["  ____  ", " / ___| ", " \\___ \\ ", "  ___) |", " |____/ "],
    't': ["  _____ ", " |_   _|", "   | |  ", "   | |  ", "   |_|  "],
    'u': ["  _   _ ", " | | | |", " | | | |", " | |_| |", "  \\___/ "],
    'w': [" __   __", " \\ \\ / /", "  \\ V / ", "   | |  ", "   |_|  "],
    'x': [" __  __ ", " \\ \\/ / ", "  >  <  ", " / /\\ \\ ", " /_/ \\_\\\\"],
    'y': [" __   __", " \\ \\ / /", "  \\ V / ", "   | |  ", "   |_|  "],
    'z': ["  _____ ", " |__  / ", "   / /  ", "  / /_  ", " /____| "],
    ' ': ["   ", "   ", "   ", "   ", "   "],
    '-': ["      ", "      ", " -----", "      ", "      "],
    '_': ["      ", "      ", "      ", "      ", " ______"],
}


def text_to_ascii_lines(text):
    """Convert a string into a list of 5 ASCII art lines."""
    text = text.lower()
    lines = ["", "", "", "", ""]
    for char in text:
        glyph = FONT_ASCII.get(char, FONT_ASCII[' '])
        for i in range(5):
            lines[i] += glyph[i]
    return lines


def generate_gcode_banner(text="1pvq1", border_pattern="1010101010101010101010101010101010"):
    """
    Generate GitHub Markdown 'gcode' syntax-highlighted ASCII banner block.
    """
    ascii_lines = text_to_ascii_lines(text)
    max_len = max(len(line) for line in ascii_lines)
    padded_border = (border_pattern * ((max_len // len(border_pattern)) + 2))[:max_len + 6]
    
    gcode_lines = []
    gcode_lines.append("```gcode")
    gcode_lines.append(padded_border)
    for line in ascii_lines:
        padded_line = line.ljust(max_len)
        gcode_lines.append(f"01 {padded_line} 10")
    gcode_lines.append(padded_border)
    gcode_lines.append("```")
    
    return "\n".join(gcode_lines)


def svg_to_gcode(svg_filepath, output_gcode_filepath, scale=1.0, feed_rate=1000):
    """
    Convert basic SVG paths/lines/polygons into CNC / Pen Plotter G-code instructions.
    G-Code Commands used:
      - G21 (metric mm)
      - G90 (absolute positioning)
      - G0 Z5 (pen up)
      - G0 X.. Y.. (rapid move)
      - G1 Z0 (pen down)
      - G1 X.. Y.. F1000 (draw move)
      - M3 / M5 (spindle / laser state)
    """
    if not os.path.exists(svg_filepath):
        raise FileNotFoundError(f"SVG file not found: {svg_filepath}")

    tree = ET.parse(svg_filepath)
    root = tree.getroot()
    
    gcode = [
        "(Header: Generated G-Code Toolpath)",
        "(Source: " + os.path.basename(svg_filepath) + ")",
        "G21 (Unit: Metric mm)",
        "G90 (Absolute coordinates)",
        "G0 Z5.000 F2000 (Pen up)",
        f"M3 S1000 (Laser/Spindle ON)",
        ""
    ]

    # Find line elements
    lines_found = 0
    for elem in root.iter():
        tag = elem.tag.split('}')[-1]
        
        if tag == 'line':
            x1 = float(elem.attrib.get('x1', 0)) * scale
            y1 = float(elem.attrib.get('y1', 0)) * scale
            x2 = float(elem.attrib.get('x2', 0)) * scale
            y2 = float(elem.attrib.get('y2', 0)) * scale

            gcode.append(f"(Draw Line)")
            gcode.append(f"G0 X{x1:.3f} Y{y1:.3f} Z5.000 (Rapid move to start)")
            gcode.append(f"G1 Z0.000 F500 (Pen down)")
            gcode.append(f"G1 X{x2:.3f} Y{y2:.3f} F{feed_rate} (Draw segment)")
            gcode.append(f"G0 Z5.000 (Pen up)")
            lines_found += 1

        elif tag == 'rect':
            x = float(elem.attrib.get('x', 0)) * scale
            y = float(elem.attrib.get('y', 0)) * scale
            w = float(elem.attrib.get('width', 0)) * scale
            h = float(elem.attrib.get('height', 0)) * scale
            
            gcode.append(f"(Draw Rectangle)")
            gcode.append(f"G0 X{x:.3f} Y{y:.3f} Z5.000")
            gcode.append(f"G1 Z0.000 F500")
            gcode.append(f"G1 X{x+w:.3f} Y{y:.3f} F{feed_rate}")
            gcode.append(f"G1 X{x+w:.3f} Y{y+h:.3f} F{feed_rate}")
            gcode.append(f"G1 X{x:.3f} Y{y+h:.3f} F{feed_rate}")
            gcode.append(f"G1 X{x:.3f} Y{y:.3f} F{feed_rate}")
            gcode.append(f"G0 Z5.000")
            lines_found += 1

        elif tag in ('polygon', 'polyline'):
            pts_str = elem.attrib.get('points', '').strip()
            if pts_str:
                pts = [p.split(',') for p in pts_str.split() if ',' in p]
                if pts:
                    gcode.append(f"(Draw Polygon/Polyline)")
                    x0, y0 = float(pts[0][0]) * scale, float(pts[0][1]) * scale
                    gcode.append(f"G0 X{x0:.3f} Y{y0:.3f} Z5.000")
                    gcode.append(f"G1 Z0.000 F500")
                    for pt in pts[1:]:
                        px, py = float(pt[0]) * scale, float(pt[1]) * scale
                        gcode.append(f"G1 X{px:.3f} Y{py:.3f} F{feed_rate}")
                    if tag == 'polygon':
                        gcode.append(f"G1 X{x0:.3f} Y{y0:.3f} F{feed_rate}")
                    gcode.append(f"G0 Z5.000")
                    lines_found += 1

    gcode.extend([
        "",
        "M5 (Laser/Spindle OFF)",
        "G0 X0.000 Y0.000 Z10.000 (Return home)",
        "M30 (End of program)"
    ])

    gcode_str = "\n".join(gcode)
    if output_gcode_filepath:
        with open(output_gcode_filepath, 'w', encoding='utf-8') as f:
            f.write(gcode_str)
        print(f"Wrote G-Code file: {output_gcode_filepath} ({lines_found} elements converted)")
    
    return gcode_str


def main():
    args = sys.argv[1:]
    mode = args[0] if args else "banner"

    if mode == "banner":
        text = args[1] if len(args) > 1 else "1pvq1"
        banner = generate_gcode_banner(text)
        print("\n--- Generated G-Code ASCII Banner ---\n")
        print(banner)
        print("\n-------------------------------------\n")
        
        # Save output banner to assets/banner.gcode.md if requested
        out_file = "assets/banner.gcode.md"
        os.makedirs("assets", exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(banner)
        print(f"Saved banner to {out_file}")

    elif mode == "svg":
        if len(args) < 2:
            print("Usage: python scripts/generate_gcode_art.py svg <input.svg> [output.gcode]")
            sys.exit(1)
        svg_file = args[1]
        out_gcode = args[2] if len(args) > 2 else "assets/toolpath.gcode"
        svg_to_gcode(svg_file, out_gcode)

    else:
        print(f"Unknown mode: {mode}. Use 'banner' or 'svg'.")


if __name__ == '__main__':
    main()
