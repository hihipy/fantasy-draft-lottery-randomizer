# Fantasy-Draft-Lottery-Randomizer

This repository contains a comprehensive Fantasy Draft Lottery Randomizer application. It is designed to help fantasy sports league managers conduct fair and transparent draft lotteries by providing a customizable, GUI-based tool for managing leagues, setting lottery distributions, and running draft order simulations.

## Features

- Manage multiple fantasy sports leagues
- Support for various lottery distribution types:
  - Straight (Random)
  - Weighted
  - Custom
- Interactive GUI for easy league management and lottery execution
- Gradual reveal of draft order with skip option
- Detailed lottery results saved to file, including:
  - Draft order
  - Odds calculations
  - League information
  - Runtime details
- Full transparency with included source code in results file

## Contents

- League management system
- Distribution management interface
- Lottery simulation algorithm
- GUI implementation using tkinter
- Asynchronous draft order reveal
- Logging system for debugging and tracking
- Error handling and input validation
- Results saving with tabulated data

## Usage

This application is intended for use by fantasy sports league managers to conduct fair draft lotteries. It can be used for various types of fantasy sports leagues and accommodates different lottery systems.

## How to Run

To run the Fantasy Draft Lottery Randomizer:

1. Ensure you have Python 3.7+ installed on your system.
2. Install the required dependencies:
   ```
   pip install tkinter asyncio tabulate
   ```
3. Run the main script:
   ```
   python fantasy_draft_lottery.py
   ```

## Application Flow

1. Start the application
2. Add or manage leagues
3. Set up lottery distribution for a league
4. Run the lottery simulation
5. View and save the results

## Customization

The application allows for customization of:
- Number of teams in a league
- League names and team managers
- Lottery distribution types and weights
- Results file save location

## Acknowledgements

This application was developed as a tool for fantasy sports enthusiasts. Special thanks to the Python community for the libraries and tools that made this project possible.

This project was inspired by the Draft Pick Lottery Generator at [https://draftpicklottery.com](https://draftpicklottery.com/index.php). We would like to acknowledge the creator of this tool for their innovative approach to draft lottery simulations.

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. 

### Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

#### You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

The licensor cannot revoke these freedoms as long as you follow the license terms.

#### Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

#### No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

#### Notices:
You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.

No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.

For more details, see the [LICENSE](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode) file.

## Disclaimer

While this application strives for fairness and randomness in lottery simulations, it is the responsibility of league managers to ensure compliance with their league rules and regulations. The developers are not responsible for any disputes arising from the use of this tool.
