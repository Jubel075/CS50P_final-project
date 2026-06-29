# McCabe–Thiele Distillation Calculator

#### Video Demo: <URL HERE>

#### Description

<!-- A short paragraph: what the project does and why. e.g. A command-line tool
that builds a McCabe–Thiele diagram for a binary distillation column, computing
the equilibrium curve, operating lines, and number of theoretical stages from
user-supplied inputs. -->

## Background

<!-- 2–4 sentences of context for a non-expert reader. What is McCabe–Thiele?
What problem does it solve in separation/distillation design? -->

## Features

- <!-- e.g. Validated component selection via the CoolProp fluid database -->
- <!-- e.g. Relative volatility and equilibrium curve from saturation pressures -->
- <!-- e.g. Rectifying and stripping operating lines + feed (q-line) intersection -->
- <!-- e.g. Theoretical stage stepping and count -->
- <!-- e.g. Matplotlib plot of the full diagram -->

## Inputs

| Symbol | Meaning | Constraint |
| ------ | ------- | ---------- |
| `light` / `heavy` | Component names (CoolProp) | Recognized fluid |
| `T`    | Column temperature (K) | `> 0` |
| `xD`   | Distillate purity | `0 < xD < 1` |
| `xB`   | Bottoms purity | `0 < xB < 1` |
| `zF`   | Feed composition | `0 < zF < 1` |
| `R`    | Reflux ratio | `>= 0` |
| `q`    | Feed quality | `q = 1` sat. liquid, `q = 0` sat. vapor |

## Files

- **`project.py`** — <!-- main program: input prompts, logic functions, plotting -->
- **`test_project.py`** — <!-- pytest unit tests for inputs and operating lines -->
- **`requirements.txt`** — <!-- pip-installable dependencies -->

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python project.py
```

<!-- Optionally: a short sample run / expected output, or a screenshot of the
generated diagram. -->

## Testing

```bash
pytest test_project.py -v
```

## Design Notes

<!-- CS50 final projects ask you to reflect on design choices. e.g. Why the
stripping line is built from two points rather than internal flow rates; why
CoolProp is used for thermodynamic properties; assumptions (constant relative
volatility, constant molal overflow). -->

## Dependencies

- [CoolProp](http://www.coolprop.org/) — thermophysical fluid properties
- [Matplotlib](https://matplotlib.org/) — plotting
- [pytest](https://pytest.org/) — testing

## Author

<!-- Your name, edX/GitHub username, city/country, date -->
