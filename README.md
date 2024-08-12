# Fantasy Draft Lottery Randomizer

This repository contains a comprehensive Fantasy Draft Lottery Randomizer application. It is designed to help fantasy sports league managers conduct fair and transparent draft lotteries by providing a customizable, GUI-based tool for managing leagues, setting lottery distributions, and running draft order simulations.

## Features

- **Manage multiple fantasy sports leagues**: Easily create, edit, and delete leagues.
- **Support for various lottery distribution types**:
  - Straight (Random)
  - Weighted
  - Custom
- **Interactive GUI** for easy league management and lottery execution, built using `tkinter`.
- **Gradual reveal** of draft order with an option to skip directly to the results.
- **Detailed lottery results saved to a file**:
  - Draft order
  - Odds calculations
  - League information
  - Runtime details
- **Full transparency**: The generated results file includes the source code for auditing purposes.
- **Asynchronous reveal**: The draft order is revealed asynchronously, allowing for a dramatic reveal experience.
- **Logging system**: Comprehensive logging for debugging and tracking.
- **Error handling**: Robust error handling and input validation.

## Contents

- **League Management System**: Create and manage fantasy sports leagues with ease.
- **Distribution Management Interface**: Customize and manage the lottery distribution for each league.
- **Lottery Simulation Algorithm**: Ensures fair and transparent draft order generation.
- **GUI Implementation**: User-friendly interface for managing leagues and running lotteries.
- **Asynchronous Draft Order Reveal**: Experience a suspenseful reveal of draft picks.
- **Logging System**: Logs events and errors for easy troubleshooting.
- **Error Handling and Input Validation**: Ensures smooth operation and prevents common issues.
- **Results Saving with Tabulated Data**: Saves detailed lottery results with clear, tabulated data.

## Usage

This application is intended for use by fantasy sports league managers to conduct fair draft lotteries. It can be used for various types of fantasy sports leagues and accommodates different lottery systems.

## How to Run

To run the Fantasy Draft Lottery Randomizer:

1. Ensure you have Python 3.7+ installed on your system.
2. Install the required dependencies:
   ```sh
   pip install tkinter asyncio tabulate
   ```
3. Run the main script:
   ```sh
   python fantasy_draft_lottery.py
   ```

## Application Flow

1. **Start the application**: Launch the app and open the main window.
2. **Add or manage leagues**: Create new leagues or edit existing ones.
3. **Set up lottery distribution for a league**: Choose between straight, weighted, or custom distribution.
4. **Run the lottery simulation**: Conduct the draft lottery for the selected league.
5. **View and save the results**: Review the draft order and save the results to a file.

## Customization

The application allows for customization of:
- **Number of teams in a league**: Set the number of teams in each league.
- **League names and team managers**: Customize the names of leagues and managers.
- **Lottery distribution types and weights**: Choose from predefined or custom lottery distributions.
- **Results file save location**: Choose where to save the detailed results file.

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
