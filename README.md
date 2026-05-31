# fantasy-draft-lottery-randomizer

[![Link Check](https://github.com/hihipy/fantasy-draft-lottery-randomizer/actions/workflows/links.yml/badge.svg)](https://github.com/hihipy/fantasy-draft-lottery-randomizer/actions/workflows/links.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Built with**

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Tkinter](https://img.shields.io/badge/Tkinter-FFD43B?style=flat&logo=python&logoColor=black)](https://docs.python.org/3/library/tkinter.html)
[![tabulate](https://img.shields.io/badge/tabulate-626E7B?style=flat&logoColor=white)](https://pypi.org/project/tabulate/)

A GUI application for conducting fantasy sports draft lotteries. Supports multiple leagues, different lottery distribution types, and saves detailed results for transparency.

## Features

- **Multiple Leagues:** Create, edit, and delete leagues.
- **Distribution Types:** Straight (random), weighted, or custom.
- **Gradual Reveal:** Dramatic draft order reveal with option to skip to results.
- **Results File:** Saves draft order, odds calculations, league info, and source code for auditing.
- **Logging:** Event and error logging for troubleshooting.

## Requirements

Python 3.7+ and the following libraries:

```bash
pip install tabulate
```

Note: `tkinter` and `asyncio` are included with Python.

## Usage

1. Run the script:
   ```bash
   python fantasy_draft_lottery_randomizer.py
   ```

2. **Add or manage leagues:** Create new leagues or edit existing ones.

3. **Set up lottery distribution:** Choose between straight, weighted, or custom distribution.

4. **Run the lottery:** Conduct the draft lottery for the selected league.

5. **View and save results:** Review the draft order and save to a file.

## Customization

- Number of teams per league
- League names and team managers
- Lottery distribution types and weights
- Results file save location

## Acknowledgments

Inspired by the Draft Pick Lottery Generator at [draftpicklottery.com](https://draftpicklottery.com/index.php).

## Disclaimer

League managers are responsible for ensuring compliance with their league rules. The developers are not responsible for disputes arising from use of this tool.

## License

This project is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

You are free to:
- Use, share, and adapt this work
- Use it at your job

Under these terms:
- **Attribution** — Credit the original author
- **NonCommercial** — No selling or commercial products
- **ShareAlike** — Derivatives must use the same license
