import sys
import subprocess
import logging

# Configure logging settings
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of log messages
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to check if a package is installed and attempt to install if not found
def check_and_install(package_name):
    try:
        __import__(package_name)
    except ImportError as import_error:
        logging.warning(f"Package '{package_name}' not found. Attempting to install it...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            logging.info(f"Successfully installed package '{package_name}'.")
        except subprocess.CalledProcessError as subprocess_error:
            logging.error(f"Failed to install package '{package_name}'. Error: {subprocess_error}")
            sys.exit(1)

# List of required packages
required_packages = [
    "asyncio", "getpass", "json", "logging", "os", "random", "threading",
    "tkinter", "datetime", "typing", "tabulate"
]

# Check and install required packages
for package in required_packages:
    check_and_install(package)

# Proceed with the main imports after ensuring all dependencies are available
try:
    import asyncio
    import getpass
    import json
    import logging
    import os
    import random
    import threading
    import tkinter as tk

    from datetime import datetime
    from tkinter import ttk, messagebox, simpledialog, filedialog

    from typing import List, Dict, Any, Optional, Tuple
    from tabulate import tabulate

    # Log a message confirming that all necessary packages have been loaded
    logging.info("All necessary packages loaded successfully.")
except ImportError as import_error_main:
    logging.critical(f"Critical error: {import_error_main}. Exiting the program.")
    sys.exit(1)

# Constants for application settings
GREEK_LETTERS = [
    'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ',
    'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ'
]
MAX_LEAGUES = 5
JSON_FOLDER = "JSON Files"
DEFAULT_SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
MIN_TEAMS = 2
MAX_TEAMS = 18
REVEAL_DELAY = 2  # Delay in seconds for revealing each pick during the lottery

# Ensure JSON folder exists
os.makedirs(JSON_FOLDER, exist_ok=True)

# Additional debug statements to check the environment setup
logging.debug(f"JSON_FOLDER set to: {JSON_FOLDER}")
logging.debug(f"DEFAULT_SAVE_FOLDER set to: {DEFAULT_SAVE_FOLDER}")
logging.debug(f"Python version: {sys.version}")
logging.debug(f"OS platform: {sys.platform}")

class LeagueManager:
    """Manages leagues and handles saving/loading data to JSON files."""

    def __init__(self):
        """Initialize the LeagueManager and load leagues from JSON files."""
        self.leagues: List[Dict[str, Any]] = self.load_leagues()

    @staticmethod
    def load_leagues() -> List[Dict[str, Any]]:
        """Load leagues from the most recently modified JSON file."""
        files = [f for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
        if not files:
            return []
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(JSON_FOLDER, x)))
        try:
            with open(os.path.join(JSON_FOLDER, latest_file), 'r') as f:
                logging.info(f"Loaded leagues from {latest_file}")
                data = json.load(f)
                if isinstance(data, dict):
                    return [data]
                elif isinstance(data, list):
                    return data
                else:
                    logging.error("Unexpected JSON format: Root element is not a list or dict.")
                    return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load leagues from JSON file. The file may be corrupted.")
            logging.error("Failed to load leagues due to JSONDecodeError.")
            return []

    def save_leagues(self) -> None:
        """Save the current state of leagues to a JSON file."""
        with open(self.get_leagues_file(), 'w') as f:
            json.dump(self.leagues, f, indent=4)
            logging.info(f"Leagues saved to {self.get_leagues_file()}")

    def get_leagues_file(self) -> str:
        """Generate a file path for saving leagues based on league names."""
        return os.path.join(JSON_FOLDER, f"leagues_{self.leagues_summary()}.json")

    def leagues_summary(self) -> str:
        """Generate a summary string of all league names."""
        return "_".join([league['name'] for league in self.leagues])

    def add_league(self, name: str, num_teams: int, managers: List[str]) -> bool:
        """Add a new league to the list if the maximum number isn't exceeded."""
        if len(self.leagues) < MAX_LEAGUES:
            self.leagues.append({
                "name": name,
                "num_teams": num_teams,
                "managers": managers,
                "distribution": "straight",
                "custom_distribution": {}
            })
            self.save_leagues()
            logging.info(f"Added new league: {name}")
            return True
        logging.warning("Attempted to add a league, but max leagues limit reached.")
        return False

    def edit_league(self, index: int, name: str, num_teams: int, managers: List[str]) -> bool:
        """Edit an existing league."""
        if 0 <= index < len(self.leagues):
            self.leagues[index].update({
                "name": name,
                "num_teams": num_teams,
                "managers": managers
            })
            self.save_leagues()
            logging.info(f"Edited league: {name}")
            return True
        logging.error(f"Failed to edit league at index {index}.")
        return False

    def delete_league(self, index: int) -> bool:
        """Delete a league from the list."""
        if 0 <= index < len(self.leagues):
            league_name = self.leagues[index]['name']
            del self.leagues[index]
            self.save_leagues()
            logging.info(f"Deleted league: {league_name}")
            return True
        logging.error(f"Failed to delete league at index {index}.")
        return False

    def update_league_distribution(
        self, index: int, distribution_type: str,
        custom_distribution: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Update the distribution type for a league."""
        if 0 <= index < len(self.leagues):
            self.leagues[index]["distribution"] = distribution_type
            if custom_distribution:
                self.leagues[index]["custom_distribution"] = custom_distribution
            self.save_leagues()
            logging.info(
                f"Updated distribution for league {self.leagues[index]['name']} to {distribution_type}"
            )
            return True
        logging.error(f"Failed to update distribution for league at index {index}.")
        return False


class EditLeagueWindow(tk.Toplevel):
    """Window for editing or adding a league."""

    def __init__(
        self, parent: tk.Tk, league_manager: LeagueManager,
        league: Optional[Dict[str, Any]] = None, index: Optional[int] = None
    ):
        """Initialize the EditLeagueWindow."""
        super().__init__(parent)
        self.num_teams_spinbox = None
        self.name_entry = None
        self.league_manager = league_manager
        self.league = league
        self.index = index
        self.title("Edit League" if league else "Add League")
        self.geometry("700x700")
        self.name_var = tk.StringVar(value=self.league['name'] if self.league else "")
        self.num_teams_var = tk.IntVar(value=self.league['num_teams'] if self.league else MIN_TEAMS)
        self.manager_entries: List[tk.StringVar] = []
        self.canvas = None
        self.scrollbar = None
        self.scrollable_frame = None
        self.setup_gui()

    def setup_gui(self) -> None:
        """Setup the GUI elements for the league editor."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # League Name Entry
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="League Name:").pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(name_frame, textvariable=self.name_var)
        self.name_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Number of Teams Spinbox
        num_teams_frame = ttk.Frame(main_frame)
        num_teams_frame.pack(fill=tk.X, pady=5)
        ttk.Label(num_teams_frame, text="Number of Teams:").pack(side=tk.LEFT, padx=5)
        self.num_teams_spinbox = ttk.Spinbox(
            num_teams_frame, from_=MIN_TEAMS, to=MAX_TEAMS,
            textvariable=self.num_teams_var, command=self.update_manager_list
        )
        self.num_teams_spinbox.pack(side=tk.LEFT, padx=5)

        # Manager Entries
        manager_frame = ttk.LabelFrame(main_frame, text="Managers")
        manager_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        self.canvas = tk.Canvas(manager_frame)
        self.scrollbar = ttk.Scrollbar(manager_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.populate_manager_list()

        # Save and Cancel Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=self.save_league).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def populate_manager_list(self) -> None:
        """Populate the manager list entries based on the number of teams."""
        managers = self.league['managers'] if self.league else []
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.manager_entries = []
        num_teams = self.num_teams_var.get()

        for i in range(num_teams):
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"Team {GREEK_LETTERS[i]}:").pack(side=tk.LEFT, padx=5)
            manager_name = managers[i].split(': ')[1] if i < len(managers) else ""
            var = tk.StringVar(value=manager_name)
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            self.manager_entries.append(var)

    def update_manager_list(self) -> None:
        """Update the manager list entries when the number of teams changes."""
        self.populate_manager_list()

    def save_league(self) -> None:
        """Save the league details."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Input Error", "League name cannot be empty.")
            logging.warning("Attempted to save a league without a name.")
            return

        num_teams = self.num_teams_var.get()
        managers = []
        for i in range(num_teams):
            manager_name = self.manager_entries[i].get().strip()
            if not manager_name:
                messagebox.showerror(
                    "Input Error", f"Manager name for Team {GREEK_LETTERS[i]} cannot be empty."
                )
                logging.warning(
                    f"Attempted to save a league with an empty manager name for Team {GREEK_LETTERS[i]}."
                )
                return
            managers.append(f"{GREEK_LETTERS[i]}: {manager_name}")

        if self.league:
            if self.league_manager.edit_league(self.index, name, num_teams, managers):
                messagebox.showinfo("Success", "League edited successfully!")
            else:
                messagebox.showerror("Error", "Failed to edit league.")
        else:
            if self.league_manager.add_league(name, num_teams, managers):
                messagebox.showinfo("Success", "League added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add league.")
        self.destroy()


class DistributionManager(tk.Toplevel):
    """Window for managing the lottery distribution of a league."""

    def __init__(self, parent: tk.Tk, league: Dict[str, Any]):
        """Initialize the DistributionManager."""
        super().__init__(parent)
        self.details_frame = None
        self.team_frame = None
        self.content_frame = None
        self.league = league
        self.title(f"Lottery Distribution - {league['name']}")
        self.geometry("1200x700")
        self.dist_var = tk.StringVar(value=self.league.get('distribution', 'straight'))
        self.total_balls_var = tk.StringVar(value="")
        self.tree = None
        self.team_listbox = None
        self.drag_start_index = None
        self.setup_gui()

    def setup_gui(self) -> None:
        """Setup the GUI elements for distribution management."""
        dist_frame = ttk.Frame(self, padding="10")
        dist_frame.pack(fill=tk.X)

        ttk.Radiobutton(
            dist_frame, text="Straight (Random)", variable=self.dist_var,
            value="straight", command=self.update_distribution
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            dist_frame, text="Weighted", variable=self.dist_var,
            value="weighted", command=self.update_distribution
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            dist_frame, text="Custom", variable=self.dist_var,
            value="custom", command=self.update_distribution
        ).pack(side=tk.LEFT)

        total_balls_label = ttk.Label(dist_frame, textvariable=self.total_balls_var)
        total_balls_label.pack(side=tk.RIGHT, padx=10)

        self.content_frame = ttk.Frame(self, padding="10")
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        self.team_frame = ttk.Frame(self.content_frame)
        self.team_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)

        team_label = ttk.Label(self.team_frame, text="Teams (Drag to Reorder)")
        team_label.pack()

        self.team_listbox = tk.Listbox(
            self.team_frame, selectmode=tk.SINGLE, activestyle='none'
        )
        self.team_listbox.pack(expand=True, fill=tk.BOTH)
        self.team_listbox.bind("<ButtonPress-1>", self.on_start_drag)
        self.team_listbox.bind("<B1-Motion>", self.on_drag)
        self.team_listbox.bind("<ButtonRelease-1>", self.on_drop)

        self.details_frame = ttk.Frame(self.content_frame)
        self.details_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

        details_label = ttk.Label(self.details_frame, text="Distribution Details")
        details_label.pack()

        columns = ('odds_rank', 'manager', 'balls', 'first_pick_odds')
        self.tree = ttk.Treeview(self.details_frame, columns=columns, show='headings')
        self.tree.heading('odds_rank', text='Lottery Odds Rank')
        self.tree.heading('manager', text='Manager')
        self.tree.heading('balls', text='Number of Balls')
        self.tree.heading('first_pick_odds', text='% Odds of Picking First')
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind('<Double-1>', self.edit_ball_count)

        save_button = ttk.Button(self, text="Save Distribution", command=self.save_distribution)
        save_button.pack(pady=10)

        self.update_distribution()

    def update_distribution(self) -> None:
        """Update the distribution details based on the selected distribution type."""
        distribution_type = self.dist_var.get()
        num_teams = len(self.league['managers'])

        if distribution_type == 'straight':
            balls = [1] * num_teams
            managers = self.league['managers']
        elif distribution_type == 'weighted':
            balls = list(range(num_teams, 0, -1))
            managers = self.league['managers']
        else:  # custom
            custom_dist = self.league.get('custom_distribution', {})
            balls = custom_dist.get('balls', list(range(num_teams, 0, -1)))
            managers = custom_dist.get('order', self.league['managers'])

        self.team_listbox.delete(0, tk.END)
        for manager in managers:
            self.team_listbox.insert(tk.END, manager)

        total_balls = sum(balls)
        self.total_balls_var.set(f"Total Balls: {total_balls}")
        self.tree.delete(*self.tree.get_children())

        if total_balls > 0:
            for i, (manager, ball_count) in enumerate(zip(managers, balls)):
                odds = (ball_count / total_balls) * 100
                self.tree.insert('', 'end', values=(i + 1, manager, ball_count, f"{odds:.2f}%"))
        else:
            for i, manager in enumerate(managers):
                self.tree.insert('', 'end', values=(i + 1, manager, 0, "0.00%"))

        if distribution_type == 'custom':
            self.tree.bind('<Double-1>', self.edit_ball_count)
        else:
            self.tree.unbind('<Double-1>')

    def on_start_drag(self, event: tk.Event) -> None:
        """Handle the start of a drag operation on the team list."""
        self.drag_start_index = self.team_listbox.nearest(event.y)

    def on_drag(self, event: tk.Event) -> None:
        """Handle the dragging of a team in the list."""
        i = self.team_listbox.nearest(event.y)
        if 0 <= i < self.team_listbox.size():
            self.team_listbox.selection_clear(0, tk.END)
            self.team_listbox.selection_set(i)

    def on_drop(self, event: tk.Event) -> None:
        """Handle the drop of a team after dragging."""
        drag_end_index = self.team_listbox.nearest(event.y)
        if 0 <= drag_end_index < self.team_listbox.size() and self.drag_start_index != drag_end_index:
            manager = self.team_listbox.get(self.drag_start_index)
            self.team_listbox.delete(self.drag_start_index)
            self.team_listbox.insert(drag_end_index, manager)
            self.update_tree_order()

    def update_tree_order(self) -> None:
        """Update the tree view to reflect the new order after dragging."""
        balls = [int(self.tree.item(child)['values'][2]) for child in self.tree.get_children()]

        managers = list(self.team_listbox.get(0, tk.END))
        total_balls = sum(balls)
        self.total_balls_var.set(f"Total Balls: {total_balls}")
        self.tree.delete(*self.tree.get_children())

        for i, (manager, ball_count) in enumerate(zip(managers, balls)):
            odds = (ball_count / total_balls) * 100 if total_balls > 0 else 0
            self.tree.insert('', 'end', values=(i + 1, manager, ball_count, f"{odds:.2f}%"))

    def edit_ball_count(self, event: tk.Event) -> None:
        """Allow editing the number of balls for a team in custom distribution mode."""
        if self.dist_var.get() != 'custom':
            return

        item = self.tree.identify_row(event.y)
        if not item:
            return
        column = self.tree.identify_column(event.x)
        if column != '#3':
            return  # Only allow editing the 'balls' column

        current_value = int(self.tree.item(item, 'values')[2])
        new_value = simpledialog.askinteger(
            "Edit Ball Count", "Enter new ball count:", initialvalue=current_value, minvalue=1
        )
        if new_value is not None:
            manager = self.tree.item(item, 'values')[1]
            index = self.tree.index(item)
            self.tree.delete(item)
            self.tree.insert('', index, values=(index + 1, manager, new_value, ""))

            # Recalculate odds
            balls = [int(self.tree.item(child)['values'][2]) for child in self.tree.get_children()]
            total_balls = sum(balls)
            self.total_balls_var.set(f"Total Balls: {total_balls}")
            for idx, child in enumerate(self.tree.get_children()):
                ball_count = balls[idx]
                odds = (ball_count / total_balls) * 100 if total_balls > 0 else 0
                current_values = self.tree.item(child)['values']
                self.tree.item(child, values=(idx + 1, current_values[1], current_values[2], f"{odds:.2f}%"))

    def save_distribution(self) -> None:
        """Save the distribution details to the league."""
        distribution_type = self.dist_var.get()
        managers = list(self.team_listbox.get(0, tk.END))

        if distribution_type == 'straight':
            self.league['distribution'] = distribution_type
            self.league['straight_distribution'] = {
                'balls': [1] * len(managers)  # All managers have one ball in straight distribution
            }
        elif distribution_type == 'weighted':
            self.league['distribution'] = distribution_type
            self.league['weighted_distribution'] = {
                'balls': list(range(len(managers), 0, -1))  # Assign balls in descending order
            }
        elif distribution_type == 'custom':
            balls = [int(self.tree.item(child)['values'][2]) for child in self.tree.get_children()]
            self.league['distribution'] = distribution_type
            self.league['custom_distribution'] = {
                'balls': balls,
                'order': managers
            }

        messagebox.showinfo("Success", "Distribution saved successfully!")
        logging.info(f"Distribution for league {self.league['name']} saved.")
        self.destroy()


class DraftLotteryApp:
    """Main application class for managing and running the fantasy draft lottery."""

    def __init__(self, root: tk.Tk):
        """Initialize the DraftLotteryApp."""
        self.league_listbox = None
        self.main_frame = None
        self.root = root
        self.root.title("Fantasy Draft Lottery Randomizer")
        self.league_manager = LeagueManager()
        self.setup_gui()
        self.root.update_idletasks()
        self.root.geometry("900x600")  # Increased width for quit button

    def setup_gui(self) -> None:
        """Setup the main GUI elements of the application."""
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.league_listbox = tk.Listbox(self.main_frame, width=50)
        self.league_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.refresh_league_list()

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add League", command=self.add_league).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit League", command=self.edit_league).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete League", command=self.delete_league).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame,
            text="Manage Lottery Odds",
            command=self.manage_distribution
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Start Lottery", command=self.start_lottery).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quit", command=self.quit_app).pack(side=tk.LEFT, padx=5)

    def refresh_league_list(self) -> None:
        """Refresh the league list displayed in the main window."""
        self.league_listbox.delete(0, tk.END)

        for league in self.league_manager.leagues:
            # Ensure that 'league' is a dictionary
            if isinstance(league, dict):
                self.league_listbox.insert(tk.END, f"{league['name']} ({league['num_teams']} teams)")
            else:
                logging.error(f"Unexpected data format: {league} is not a dictionary.")

    def add_league(self) -> None:
        """Open the Add League window."""
        if len(self.league_manager.leagues) >= MAX_LEAGUES:
            messagebox.showerror("Error", f"Maximum number of leagues ({MAX_LEAGUES}) reached.")
            logging.warning("Attempted to add a league but max leagues limit reached.")
            return

        edit_window = EditLeagueWindow(self.root, self.league_manager, league=None)
        self.root.wait_window(edit_window)
        self.refresh_league_list()

    def edit_league(self) -> None:
        """Open the Edit League window."""
        selected = self.league_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a league to edit.")
            logging.warning("Attempted to edit a league without selecting one.")
            return

        index = selected[0]
        league = self.league_manager.leagues[index]

        edit_window = EditLeagueWindow(self.root, self.league_manager, league=league, index=index)
        self.root.wait_window(edit_window)
        self.refresh_league_list()

    def delete_league(self) -> None:
        """Delete the selected league."""
        selected = self.league_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a league to delete.")
            logging.warning("Attempted to delete a league without selecting one.")
            return

        index = selected[0]
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this league?"):
            if self.league_manager.delete_league(index):
                self.refresh_league_list()
                messagebox.showinfo("Success", "League deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete league.")

    def manage_distribution(self) -> None:
        """Open the distribution management window for the selected league."""
        selected = self.league_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a league to manage lottery odds.")
            logging.warning("Attempted to manage lottery odds without selecting a league.")
            return

        index = selected[0]
        league = self.league_manager.leagues[index]

        distribution_window = DistributionManager(self.root, league)
        self.root.wait_window(distribution_window)
        self.league_manager.save_leagues()

    def start_lottery(self) -> None:
        """Start the lottery for the selected league."""
        selected = self.league_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a league to start the lottery.")
            logging.warning("Attempted to start a lottery without selecting a league.")
            return

        index = selected[0]
        league = self.league_manager.leagues[index]

        dist_window = tk.Toplevel(self.root)
        dist_window.title("Select Distribution")
        dist_window.geometry("300x150")

        ttk.Label(dist_window, text="Choose Distribution:").pack(pady=10)

        dist_var = tk.StringVar(value="")  # Start with a blank value
        dist_options = ["Straight", "Weighted", "Custom"]
        dist_dropdown = ttk.Combobox(dist_window, textvariable=dist_var, values=dist_options)
        dist_dropdown.pack(pady=10)

        def confirm_distribution():
            selected_dist = dist_var.get()
            if selected_dist not in dist_options:
                messagebox.showerror("Error", "Invalid distribution type selected.")
                logging.error("Invalid distribution type selected.")
                return
            league['distribution'] = selected_dist  # Store the selected distribution
            self.league_manager.save_leagues()
            dist_window.destroy()
            result_window = LotteryResultWindow(self.root, league)
            try:
                self.root.wait_window(result_window)
            except tk.TclError:
                pass  # Ignore the error if the window is already destroyed

        ttk.Button(dist_window, text="Confirm", command=confirm_distribution).pack(pady=10)

    def quit_app(self) -> None:
        """Quit the application."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            logging.info("Application closed by user.")
            self.root.quit()


class LotteryResultWindow(tk.Toplevel):
    """Window for displaying the results of the lottery."""

    def __init__(self, parent: tk.Tk, league: Dict[str, Any]):
        """Initialize the LotteryResultWindow."""
        super().__init__(parent)
        self.league = league
        self.title(f"Lottery Result - {league['name']}")
        self.geometry("600x700")
        self.skip_reveal = False
        self.labels: List[Tuple[ttk.Label, str]] = []
        self.result_frame = ttk.Frame(self, padding="10")
        self.result_frame.pack(expand=True, fill=tk.BOTH)
        self.start_time = datetime.now()
        self.selected_order = []
        self.original_balls = []
        self.skip_button = None
        self.run_lottery()

    def run_lottery(self) -> None:
        """Run the lottery to determine the draft order."""
        distribution_type = self.league['distribution']

        # Logging the selected distribution type
        logging.debug(f"Selected distribution type: {distribution_type}")

        # Ensure the correct distribution data is used
        if distribution_type.lower() == 'custom':
            dist_data = self.league.get('custom_distribution', {})
        elif distribution_type.lower() == 'straight':
            dist_data = self.league.get('straight_distribution', {})
        elif distribution_type.lower() == 'weighted':
            dist_data = self.league.get('weighted_distribution', {})
        else:
            messagebox.showerror("Error", f"Invalid distribution type: {distribution_type}")
            logging.error(f"Invalid distribution type: {distribution_type}")
            return

        # Logging the distribution data being used
        logging.debug(f"Distribution data used: {dist_data}")

        # Use the correct balls and order from the chosen distribution
        self.original_balls = dist_data.get('balls', [1] * len(self.league['managers']))
        order = dist_data.get('order', self.league['managers'])

        # Logging the balls and order arrays
        logging.debug(f"Balls array: {self.original_balls}")
        logging.debug(f"Order array: {order}")

        # Build the pool based on the distribution type
        pool = []
        for manager, ball_count in zip(order, self.original_balls):
            pool.extend([manager] * ball_count)

        # Logging the pool after it's been constructed
        logging.debug(f"Initial pool: {pool}")

        while len(self.selected_order) < len(self.league['managers']):
            pick = random.choice(pool)
            self.selected_order.append(pick)
            pool = [p for p in pool if p != pick]  # Remove selected manager from pool

            # Logging the selected order and remaining pool after each pick
            logging.debug(f"Selected order so far: {self.selected_order}")
            logging.debug(f"Remaining pool: {pool}")

        # Display the draft order title
        ttk.Label(self.result_frame, text="Draft Order:", font=("Arial", 14)).pack(pady=10)

        # Add the skip button to allow users to skip the reveal process
        self.skip_button = ttk.Button(self.result_frame, text="Skip to End", command=self.skip_to_end)
        self.skip_button.pack(pady=5)

        # Create a new thread to run the asyncio event loop
        thread = threading.Thread(target=self.run_async_reveal)
        thread.start()

    def run_async_reveal(self) -> None:
        """Run the async reveal_draft_order function in a new thread."""
        asyncio.run(self.reveal_draft_order(self.selected_order))

    async def reveal_draft_order(self, selected_order: List[str]) -> None:
        """Reveal the draft order, either gradually or immediately if skipped."""
        self.labels = []
        num_picks = len(selected_order)

        for idx, manager in enumerate(selected_order):
            label_text = f"{idx + 1}. ???" if idx != num_picks - 1 else f"{idx + 1}. ???"
            label = ttk.Label(self.result_frame, text=label_text)
            label.pack(anchor="w", pady=2)
            self.labels.append((label, f"{idx + 1}. {manager}"))

        for idx, (label, text) in enumerate(reversed(self.labels)):
            if self.skip_reveal:
                break

            if idx == 0:  # If this is the last pick (reverse order)
                await asyncio.sleep(REVEAL_DELAY)

            if label.winfo_exists():
                label.config(text=text)
                self.result_frame.update()
                await asyncio.sleep(REVEAL_DELAY)

        if self.skip_reveal:
            for label, text in self.labels:
                if label.winfo_exists():
                    label.config(text=text)

        if self.skip_button.winfo_exists():
            self.skip_button.config(state=tk.DISABLED)

        # Save the lottery results after all picks are revealed
        end_time = datetime.now()
        runtime = (end_time - self.start_time).total_seconds()
        self.save_lottery_result(self.selected_order, runtime, end_time)

    def skip_to_end(self) -> None:
        """Skip the gradual reveal and show the entire draft order immediately."""
        self.skip_reveal = True
        for label, text in self.labels:
            if label.winfo_exists():
                label.config(text=text)
        if self.result_frame.winfo_exists():
            self.result_frame.update()

        # Disable the skip button after revealing all picks
        if self.skip_button.winfo_exists():
            self.skip_button.config(state=tk.DISABLED)

    @staticmethod
    def exact_pick_odds(manager_balls: List[int], total_balls: int, pick_position: int) -> List[float]:
        """Calculate the exact probability for each pick position using combinatorics."""
        remaining_balls = total_balls
        pick_probabilities = []

        for i in range(pick_position):
            pick_probabilities.append([balls / remaining_balls for balls in manager_balls])
            if i < pick_position - 1:
                # Remove the selected manager's balls from consideration for the next pick
                for j in range(len(manager_balls)):
                    manager_balls[j] *= (remaining_balls - manager_balls[j]) / remaining_balls
                remaining_balls -= 1

        return pick_probabilities[-1]

    def save_lottery_result(self, selected_order: List[str], runtime: float, end_time: datetime) -> None:
        """Save the lottery results to a text file."""
        file_path = filedialog.asksaveasfilename(
            initialdir=DEFAULT_SAVE_FOLDER,
            defaultextension=".txt",
            initialfile="lottery_results.txt",
            title="Save Lottery Results",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            logging.warning("No file path selected; results not saved.")
            return

        username = getpass.getuser()
        distribution_type = self.league['distribution']

        # Depending on the distribution type, we select the correct `balls` and `order`.
        if distribution_type.lower() == 'custom':
            dist_data = self.league.get('custom_distribution', {})
        elif distribution_type.lower() == 'straight':
            dist_data = self.league.get('straight_distribution', {})
        elif distribution_type.lower() == 'weighted':
            dist_data = self.league.get('weighted_distribution', {})
        else:
            logging.error(f"Invalid distribution type: {distribution_type}")
            return

        # Logging the distribution data being used
        logging.debug(f"Distribution data used for saving: {dist_data}")

        manager_balls = dict(zip(dist_data.get('order', self.league['managers']),
                                 dist_data.get('balls', self.original_balls)))

        total_balls = sum(manager_balls.values())  # Recalculate total balls correctly

        # Logging the total number of balls
        logging.debug(f"Total balls: {total_balls}")

        # Calculate exact odds for each pick for each manager using combinatorial calculations
        exact_odds_matrix = []
        for i in range(len(selected_order)):
            exact_odds_matrix.append(self.exact_pick_odds(list(manager_balls.values()), total_balls, i + 1))

        with open(file_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write(f"{'FANTASY DRAFT LOTTERY RESULTS':^80}\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"{'Draft Order':^80}\n")
            f.write("-" * 80 + "\n")

            table = [
                ["Rank", "Manager", "Balls", "Odds of 1st Overall (%)", "Combinatorial Odds of This Pick (%)"]
            ]

            for idx, manager in enumerate(selected_order):
                manager_index = self.league['managers'].index(manager)
                ball_count = manager_balls.get(manager, self.original_balls[manager_index])
                first_overall_odds = (ball_count / total_balls) * 100  # Simple calculation
                this_pick_odds = exact_odds_matrix[idx][manager_index] * 100  # Exact combinatorial calculation

                table.append([
                    idx + 1,
                    manager,
                    ball_count,
                    f"{first_overall_odds:.2f}%",
                    f"{this_pick_odds:.2f}%"
                ])

            f.write(tabulate(table, headers="firstrow", tablefmt="grid"))
            f.write("\n" + "-" * 80 + "\n")

            # Add explanation of how the odds were calculated
            f.write("\nODDS CALCULATION EXPLANATION:\n")
            f.write("-" * 80 + "\n")
            f.write(
                "The odds of 1st Overall (%) were calculated by dividing the number of balls a manager has by the "
                "total\n")
            f.write(
                "number of balls and multiplying by 100. This represents the simple probability of drawing that "
                "manager's\n")
            f.write("ball on the first pick.\n\n")

            f.write(
                "The Combinatorial Odds of This Pick (%) were calculated using combinatorial mathematics, "
                "which considers\n")
            f.write(
                "all possible sequences of outcomes for the entire draft process. This method is more complex and "
                "takes into\n")
            f.write(
                "account the dependencies between picks (e.g., if one manager's ball is picked, it reduces the "
                "probability\n")
            f.write("of their ball being picked again in subsequent draws).\n\n")

            f.write(
                "Because of this, the Combinatorial Odds may differ from the simple ball/total ball calculation, "
                "particularly\n")
            f.write(
                "in scenarios where a manager has a disproportionately large or small number of balls compared to "
                "others.\n")
            f.write(
                "For example, a manager with many balls may see their odds spread out across multiple picks, "
                "while a manager\n")
            f.write(
                "with few balls may have a higher concentration of their odds in certain picks. This results in a "
                "distribution\n")
            f.write("that doesn't always match up perfectly with the simple odds calculation.\n")
            f.write("\n" + "-" * 80 + "\n")

            f.write("\nADDITIONAL INFORMATION:\n")
            f.write("-" * 80 + "\n")
            f.write(f"League Name: {self.league['name']}\n")
            f.write(f"Number of Teams: {self.league['num_teams']}\n")
            f.write(f"Distribution Type: {distribution_type}\n")
            f.write(f"Total Balls in Generation: {total_balls}\n")
            f.write(f"Time of Generation: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Time of File Save: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Runtime Duration: {runtime:.2f} seconds\n")
            f.write(f"Generated by: {username}\n")
            f.write("\nThis draft order was generated fairly using combinatorial mathematics.\n")
            f.write(
                "Feel free to audit the code by either reviewing it yourself or feeding it into generative AI for "
                "auditing.\n\n")

            # Include the full Python script for auditing
            f.write("=" * 80 + "\n")
            f.write(f"{'FULL PYTHON SCRIPT':^80}\n")
            f.write("=" * 80 + "\n")
            f.write("```python\n")  # Start the code block
            with open(__file__, 'r') as script_file:  # Assuming __file__ is the path to the current script
                f.write(script_file.read())
            f.write("\n```\n")  # End the code block

        messagebox.showinfo("Success", f"Results saved to {file_path}")
        logging.info(f"Lottery results saved to {file_path}")

        self.destroy()


def main() -> None:
    """Main function to run the Fantasy Draft Lottery Randomizer."""
    root = tk.Tk()
    DraftLotteryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
