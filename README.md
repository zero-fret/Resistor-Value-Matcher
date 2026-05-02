# Resistor Value Matcher

A resistor value matching tool that finds the closest approximation to a target resistance using single resistors or series/parallel combinations from standard E24, E96, or custom resistor series.

## Features

- **Multiple resistor series support**: E24 (5% tolerance), E96 (1% tolerance), or custom user-defined values
- **Combination types**: Single resistor, series combination, parallel combination
- **CLI version**: Fast batch processing for multiple target values
- **GUI version**: User-friendly graphical interface for interactive use
- **Error calculation**: Shows percentage error for each match

## Requirements

**No external dependencies required** – This project uses only the Python standard library.

- Python 3.6 or higher

## Installation

```bash
# Clone the repository
git clone https://github.com/zero-fret/Resistor-Value-Matcher.git

# Navigate to the project directory
cd Resistor-Value-Matcher

File Structure

Resistor-Value-Matcher/
├── README.md
├── resistor-value-matcher-mini.py    # Mini version
└── Resistor_Value_Matcher.py    # Graphical version
```
## Usage
### GUI Version (Recommended for most users)
- **Run the graphical interface:**
```bash
   python Resistor_Value_Matcher.py
```
- **The GUI window will open with the following options:**
1. Select resistor set - Choose E24, E96, or Custom
2. Enter custom resistors (if Custom selected) - Comma-separated values, e.g., 100, 220, 470, 1000
3. Enter target resistors - Comma-separated values, e.g., 1000, 2200, 4700
4. Click Calculate to see results

### Mini Version (Recommended for developers)
**Configuration is done by editing the source code directly.**
This minimal version has zero external dependencies and is designed for:
- Quick prototyping
- Integration as a library
- Custom algorithm tweaks
```python
# Edit these lines in resistor_matcher_cli.py
RESISTOR_SET = "CUSTOM"   # Change to "E24", "E96", or "CUSTOM"
targets = [
    144700,   # Replace with your target values
    72300,
    36200,
]
```
