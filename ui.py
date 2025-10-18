import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from manager import TournamentManager
from models import Match


class TournamentUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎮 Esports Tournament Manager Pro")
        self.geometry("1200x800")
        self.configure(bg='#2c3e50')
        self.manager = TournamentManager()

        # Custom fonts
        self.title_font = tkFont.Font(
            family="Helvetica", size=16, weight="bold")
        self.header_font = tkFont.Font(
            family="Helvetica", size=12, weight="bold")
        self.normal_font = tkFont.Font(family="Helvetica", size=10)

        # Color scheme
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'success': '#27ae60'
        }

        self._setup_styles()
        self._build_layout()
        self.bind_dynamic()

    def _setup_styles(self):
        """Configure custom ttk styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure custom progress bar styles
        style.configure('Primary.Horizontal.TProgressbar',
                        background=self.colors['primary'],
                        troughcolor=self.colors['light'])
        style.configure('Warning.Horizontal.TProgressbar',
                        background=self.colors['warning'],
                        troughcolor=self.colors['light'])
        style.configure('Success.Horizontal.TProgressbar',
                        background=self.colors['success'],
                        troughcolor=self.colors['light'])

        # Configure frame styles
        style.configure('Primary.TFrame', background=self.colors['light'])
        style.configure('Dark.TFrame', background=self.colors['dark'])

        # Configure label styles
        style.configure('Primary.TLabel',
                        background=self.colors['light'],
                        font=self.normal_font)
        style.configure('Title.TLabel',
                        background=self.colors['dark'],
                        foreground='white',
                        font=self.title_font)
        style.configure('Header.TLabel',
                        background=self.colors['primary'],
                        foreground='white',
                        font=self.header_font)

        # Configure button styles
        style.configure('Primary.TButton',
                        font=self.normal_font,
                        background=self.colors['primary'])
        style.configure('Success.TButton',
                        font=self.normal_font,
                        background=self.colors['success'])
        style.configure('Warning.TButton',
                        font=self.normal_font,
                        background=self.colors['warning'])

        # Configure treeview styles
        style.configure('Custom.Treeview',
                        font=self.normal_font,
                        rowheight=25,
                        background='white',
                        fieldbackground='white')
        style.configure('Custom.Treeview.Heading',
                        font=self.header_font,
                        background=self.colors['primary'],
                        foreground='white')

    def _build_layout(self):
        # Header
        header_frame = ttk.Frame(self, style='Dark.TFrame')
        header_frame.pack(fill="x", padx=0, pady=0)

        title_label = ttk.Label(
            header_frame, text="🏆 ESPORTS TOURNAMENT MANAGER", style='Title.TLabel')
        title_label.pack(pady=15)

        # Main container
        main_container = ttk.Frame(self, style='Primary.TFrame')
        main_container.pack(fill="both", expand=True, padx=8, pady=8)

        # Left panel
        left_panel = ttk.Frame(main_container, style='Primary.TFrame')
        left_panel.pack(side="left", fill="y", padx=4, pady=4)

        # Setup frame with modern design
        config = ttk.LabelFrame(
            left_panel, text="⚙️ TOURNAMENT SETUP", style='Primary.TFrame')
        config.pack(fill="x", padx=4, pady=6)

        # Bracket type selection with icons
        bracket_frame = ttk.Frame(config, style='Primary.TFrame')
        bracket_frame.pack(fill="x", padx=4, pady=4)

        ttk.Label(bracket_frame, text="🏗️ Bracket Type:",
                  style='Primary.TLabel').pack(side="left", padx=4)
        self.bracket_var = tk.StringVar(value="Single Elimination")
        bracket_combo = ttk.Combobox(bracket_frame, textvariable=self.bracket_var,
                                     values=["Single Elimination",
                                             "Double Elimination", "Round Robin"],
                                     state="readonly", width=20, font=self.normal_font)
        bracket_combo.pack(side="left", padx=4, pady=4)

        # Team count with visual indicator
        team_count_frame = ttk.Frame(config, style='Primary.TFrame')
        team_count_frame.pack(fill="x", padx=4, pady=4)

        ttk.Label(team_count_frame, text="👥 Number of Teams:",
                  style='Primary.TLabel').pack(side="left", padx=4)
        self.num_teams_var = tk.IntVar(value=8)
        team_spin = ttk.Spinbox(team_count_frame, from_=2, to=64, textvariable=self.num_teams_var,
                                width=8, font=self.normal_font)
        team_spin.pack(side="left", padx=4, pady=4)

        # Team entries with scrollable frame
        team_entries_container = ttk.Frame(config, style='Primary.TFrame')
        team_entries_container.pack(fill="x", padx=4, pady=4)

        ttk.Label(team_entries_container, text="🏷️ Team Names:",
                  style='Primary.TLabel').pack(anchor="w")

        # Create a canvas and scrollbar for team entries
        canvas = tk.Canvas(team_entries_container, height=120,
                           bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            team_entries_container, orient="vertical", command=canvas.yview)
        self.team_entries_frame = ttk.Frame(canvas, style='Primary.TFrame')

        self.team_entries_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(
            (0, 0), window=self.team_entries_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(0, 4))
        scrollbar.pack(side="right", fill="y", padx=(0, 4))

        self.team_entries = []
        self._render_team_entries()

        # Generate button with modern style
        generate_btn = ttk.Button(config, text="🚀 Generate Bracket",
                                  command=self.on_generate, style='Success.TButton')
        generate_btn.pack(fill="x", padx=4, pady=8)

        # Teams & Check-in with progress
        teams_frame = ttk.LabelFrame(
            left_panel, text="👥 TEAMS & CHECK-IN", style='Primary.TFrame')
        teams_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Progress bar for check-ins
        self.checkin_progress = ttk.Progressbar(
            teams_frame, mode='determinate', style='Primary.Horizontal.TProgressbar')
        self.checkin_progress.pack(fill="x", padx=4, pady=4)

        self.progress_label = ttk.Label(
            teams_frame, text="0/0 checked in", style='Primary.TLabel')
        self.progress_label.pack(padx=4, pady=2)

        # Teams list with custom styling
        list_frame = ttk.Frame(teams_frame, style='Primary.TFrame')
        list_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.teams_list = tk.Listbox(list_frame, height=12, width=30, font=self.normal_font,
                                     bg='white', selectbackground=self.colors['primary'],
                                     relief='solid', borderwidth=1)
        self.teams_list.pack(fill="both", expand=True, padx=4, pady=4)

        # Check-in button
        self.checkin_btn = ttk.Button(teams_frame, text="✅ Toggle Check-In",
                                      command=self.on_checkin_toggle, style='Primary.TButton')
        self.checkin_btn.pack(fill="x", padx=4, pady=4)

        # Center panel - Matches
        center_panel = ttk.Frame(main_container, style='Primary.TFrame')
        center_panel.pack(side="left", fill="both",
                          expand=True, padx=4, pady=4)

        matches_frame = ttk.LabelFrame(
            center_panel, text="⚔️ MATCHES", style='Primary.TFrame')
        matches_frame.pack(fill="both", expand=True, padx=4, pady=4)

        # Matches treeview with custom styling
        tree_frame = ttk.Frame(matches_frame, style='Primary.TFrame')
        tree_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.matches_tree = ttk.Treeview(tree_frame, columns=("round", "team1", "team2", "status", "score"),
                                         show="headings", height=15, style='Custom.Treeview')

        # Configure columns with better styling
        for col, w in [("round", 100), ("team1", 150), ("team2", 150), ("status", 100), ("score", 80)]:
            self.matches_tree.heading(col, text=col.title())
            self.matches_tree.column(col, width=w, anchor="center")

        # Add scrollbar to treeview
        tree_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.matches_tree.yview)
        self.matches_tree.configure(yscrollcommand=tree_scroll.set)

        self.matches_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Match controls with better layout
        match_controls = ttk.Frame(matches_frame, style='Primary.TFrame')
        match_controls.pack(fill="x", padx=4, pady=8)

        # Selected match info
        match_info_frame = ttk.Frame(match_controls, style='Primary.TFrame')
        match_info_frame.pack(fill="x", padx=4, pady=4)

        self.t1_label = ttk.Label(
            match_info_frame, text="🔴 Team 1: -", style='Header.TLabel')
        self.t1_label.pack(side="left", padx=8)

        self.vs_label = ttk.Label(
            match_info_frame, text="⚔️ VS", style='Header.TLabel')
        self.vs_label.pack(side="left", padx=8)

        self.t2_label = ttk.Label(
            match_info_frame, text="🔵 Team 2: -", style='Header.TLabel')
        self.t2_label.pack(side="left", padx=8)

        # Action buttons
        action_frame = ttk.Frame(match_controls, style='Primary.TFrame')
        action_frame.pack(fill="x", padx=4, pady=4)

        ttk.Button(action_frame, text="▶️ Start Match", command=self.on_start_match,
                   style='Success.TButton').pack(side="left", padx=2)

        # Score input
        score_frame = ttk.Frame(action_frame, style='Primary.TFrame')
        score_frame.pack(side="left", padx=8)

        ttk.Label(score_frame, text="📊 Score:",
                  style='Primary.TLabel').pack(side="left")
        self.score1_var = tk.IntVar(value=0)
        self.score2_var = tk.IntVar(value=0)

        ttk.Entry(score_frame, textvariable=self.score1_var, width=3,
                  font=self.normal_font, justify='center').pack(side="left", padx=2)
        ttk.Label(score_frame, text="-",
                  style='Primary.TLabel').pack(side="left")
        ttk.Entry(score_frame, textvariable=self.score2_var, width=3,
                  font=self.normal_font, justify='center').pack(side="left", padx=2)

        ttk.Button(action_frame, text="📤 Submit Result", command=self.on_submit_result,
                   style='Warning.TButton').pack(side="left", padx=2)

        ttk.Button(action_frame, text="✅ Confirm Team 1",
                   command=lambda: self.on_confirm(1), style='Primary.TButton').pack(side="left", padx=2)
        ttk.Button(action_frame, text="✅ Confirm Team 2",
                   command=lambda: self.on_confirm(2), style='Primary.TButton').pack(side="left", padx=2)

        # Right panel
        right_panel = ttk.Frame(main_container, style='Primary.TFrame')
        right_panel.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        # Bracket display
        bracket_frame = ttk.LabelFrame(
            right_panel, text="📋 BRACKET", style='Primary.TFrame')
        bracket_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.bracket_text = tk.Text(bracket_frame, height=12, font=('Consolas', 9),
                                    bg='#f8f9fa', relief='solid', borderwidth=1)
        bracket_scroll = ttk.Scrollbar(
            bracket_frame, orient="vertical", command=self.bracket_text.yview)
        self.bracket_text.configure(yscrollcommand=bracket_scroll.set)

        self.bracket_text.pack(side="left", fill="both", expand=True)
        bracket_scroll.pack(side="right", fill="y")

        # Scoreboard
        scoreboard_frame = ttk.LabelFrame(
            right_panel, text="🏅 SCOREBOARD", style='Primary.TFrame')
        scoreboard_frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.scoreboard_text = tk.Text(scoreboard_frame, height=8, font=('Consolas', 9),
                                       bg='#fff3cd', relief='solid', borderwidth=1)
        scoreboard_scroll = ttk.Scrollbar(
            scoreboard_frame, orient="vertical", command=self.scoreboard_text.yview)
        self.scoreboard_text.configure(yscrollcommand=scoreboard_scroll.set)

        self.scoreboard_text.pack(side="left", fill="both", expand=True)
        scoreboard_scroll.pack(side="right", fill="y")

        # Event log with modern design
        log_frame = ttk.LabelFrame(
            self, text="📝 EVENT LOG", style='Primary.TFrame')
        log_frame.pack(fill="both", expand=False, padx=8, pady=6)

        self.log_text = tk.Text(log_frame, height=8, font=('Consolas', 8),
                                bg='#1a1a1a', fg='#00ff00', relief='solid', borderwidth=1)
        log_scroll = ttk.Scrollbar(
            log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.pack(side="right", fill="y")

        # Status bar
        status_frame = ttk.Frame(self, style='Dark.TFrame')
        status_frame.pack(fill="x", padx=0, pady=0)

        self.status = ttk.Label(status_frame, text="🚀 Ready to start your tournament!",
                                style='Title.TLabel')
        self.status.pack(fill="x", padx=8, pady=4)

        self.refresh_ui()

    def bind_dynamic(self):
        self.num_teams_var.trace_add(
            "write", lambda *_: self._render_team_entries())

    def _render_team_entries(self):
        for w in self.team_entries:
            w.destroy()
        self.team_entries.clear()

        n = self.num_teams_var.get()
        for i in range(n):
            row = i // 2
            col = i % 2

            if col == 0:
                frame = ttk.Frame(self.team_entries_frame,
                                  style='Primary.TFrame')
                frame.pack(fill="x", padx=2, pady=1)

            e = ttk.Entry(frame, width=20, font=self.normal_font)
            e.pack(side="left", padx=2, pady=1)
            e.insert(0, f"Team {i+1}")
            self.team_entries.append(e)

    def _update_progress(self):
        if self.manager.teams:
            checked_in = sum(1 for t in self.manager.teams if t.checked_in)
            total = len(self.manager.teams)
            progress = (checked_in / total) * 100

            self.checkin_progress['value'] = progress
            self.progress_label.config(
                text=f"{checked_in}/{total} checked in ({progress:.0f}%)")

            # Change color based on progress
            if progress == 100:
                self.checkin_progress.configure(
                    style='Success.Horizontal.TProgressbar')
            elif progress >= 50:
                self.checkin_progress.configure(
                    style='Warning.Horizontal.TProgressbar')
            else:
                self.checkin_progress.configure(
                    style='Primary.Horizontal.TProgressbar')

    # Event Handlers
    def on_generate(self):
        names = [e.get().strip() for e in self.team_entries]
        if any(len(n) == 0 for n in names):
            messagebox.showerror("Validation", "❌ Please fill all team names.")
            return

        self.manager.register_teams(names)
        self.manager.set_bracket(self.bracket_var.get())
        self.status.config(
            text="✅ Brackets generated! Teams are awaiting check-in.")

        # Visual celebration
        self._animate_success()
        self.refresh_ui()

    def on_checkin_toggle(self):
        sel = self.teams_list.curselection()
        if not sel:
            messagebox.showinfo("Selection", "👆 Please select a team first.")
            return

        team = self.manager.teams[sel[0]]
        team.checked_in = not team.checked_in
        status = "checked in" if team.checked_in else "checked out"
        self.manager.log(f"🔔 {team.name} {status}")

        self._update_progress()
        self.refresh_ui()

    def on_start_match(self):
        match = self._selected_match()
        if not match:
            messagebox.showinfo(
                "Select Match", "🎯 Please select a match to start.")
            return

        self.manager.start_match(match)
        self.score1_var.set(0)
        self.score2_var.set(0)

        # Visual feedback
        self._flash_element(self.matches_tree, self.colors['success'])
        self.refresh_ui()

    def on_submit_result(self):
        match = self._selected_match()
        if not match:
            messagebox.showinfo(
                "Select Match", "🎯 Please select a match to submit results.")
            return

        s1, s2 = self.score1_var.get(), self.score2_var.get()
        self.manager.submit_result(match, s1, s2)

        # Enhanced visual feedback
        self._flash_element(self.bracket_text, self.colors['warning'])
        self._flash_element(self.scoreboard_text, self.colors['warning'])
        self.refresh_ui()

    def on_confirm(self, team_index: int):
        match = self._selected_match()
        if not match:
            messagebox.showinfo(
                "Select Match", "🎯 Please select a match to confirm winner.")
            return

        self.manager.confirm_winner(match, team_index)

        # Celebration for match completion
        self._flash_element(self.bracket_text, self.colors['success'])
        self._flash_element(self.scoreboard_text, self.colors['primary'])

        if self.manager.bracket and self.manager.bracket.completed:
            self._celebrate_champion()

        self.refresh_ui()

    def _selected_match(self) -> Match:
        sel = self.matches_tree.selection()
        if not sel:
            return None
        match_id = sel[0]
        for rnd in self.manager.bracket.rounds:
            for m in rnd:
                if m.id == match_id:
                    return m
        return None

    def _animate_success(self):
        original_color = self.status.cget('background')
        for color in [self.colors['success'], original_color]:
            self.status.configure(background=color)
            self.update()
            self.after(200)

    def _flash_element(self, widget, color):
        original_color = widget.cget('bg')
        widget.configure(bg=color)
        self.after(300, lambda: widget.configure(bg=original_color))

    def _celebrate_champion(self):
        if self.manager.bracket.champion:
            champion_name = self.manager.bracket.champion.name
            self.status.config(text=f"🎉 CHAMPION: {champion_name} 🎉")

            # Flash status bar in celebration colors
            for color in [self.colors['success'], self.colors['warning'], self.colors['primary']]:
                self.status.configure(background=color)
                self.update()
                self.after(300)

    def refresh_ui(self):
        # Update teams list with check-in status
        self.teams_list.delete(0, tk.END)
        for t in self.manager.teams:
            status_icon = "✅" if t.checked_in else "❌"
            self.teams_list.insert(tk.END, f"{status_icon} {t.name}")

        self._update_progress()

        # Update selected match info
        match = self._selected_match()
        if match:
            t1_name = match.team1.name if match.team1 else "BYE"
            t2_name = match.team2.name if match.team2 else "BYE"
            self.t1_label.config(text=f"🔴 {t1_name}")
            self.t2_label.config(text=f"🔵 {t2_name}")
        else:
            self.t1_label.config(text="🔴 Team 1: -")
            self.t2_label.config(text="🔵 Team 2: -")

        # Update matches table
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)

        if self.manager.bracket:
            for rnd in self.manager.bracket.rounds:
                for m in rnd:
                    status_icon = {
                        "Scheduled": "⏰",
                        "Ongoing": "🔥",
                        "Completed": "✅",
                        "Disputed": "⚠️"
                    }.get(m.status, "❓")

                    self.matches_tree.insert("", "end", iid=m.id,
                                             values=(f"Round {m.round_index+1}",
                                                     m.team1.name if m.team1 else "BYE",
                                                     m.team2.name if m.team2 else "BYE",
                                                     f"{status_icon} {m.status}",
                                                     f"{m.score[0]}-{m.score[1]}"))

        # Update bracket display
        self.bracket_text.delete("1.0", tk.END)
        if self.manager.bracket:
            self.bracket_text.insert(
                tk.END, f"🏆 {self.manager.bracket.type_name.upper()} BRACKET\n")
            self.bracket_text.insert(tk.END, "=" * 50 + "\n\n")

            for ri, rnd in enumerate(self.manager.bracket.rounds):
                self.bracket_text.insert(tk.END, f"🎯 ROUND {ri+1}:\n")
                for m in rnd:
                    t1 = m.team1.name if m.team1 else "BYE"
                    t2 = m.team2.name if m.team2 else "BYE"

                    if m.status == "Completed" and m.winner:
                        winner_star = "⭐" if m.winner == self.manager.bracket.champion else ""
                        line = f"  {winner_star} {t1} vs {t2} → {m.winner.name} {winner_star}"
                    else:
                        line = f"  {t1} vs {t2}"

                    # Color code based on status
                    status_color = {
                        "Completed": "🟢",
                        "Ongoing": "🟡",
                        "Scheduled": "⚪",
                        "Disputed": "🔴"
                    }.get(m.status, "⚫")

                    self.bracket_text.insert(
                        tk.END, f"{status_color} {line} [{m.score[0]}-{m.score[1]}]\n")
                self.bracket_text.insert(tk.END, "\n")

        # Update scoreboard
        self.scoreboard_text.delete("1.0", tk.END)
        if self.manager.teams:
            standings = sorted(
                self.manager.teams,
                key=lambda t: (t.wins, t.points_for - t.points_against),
                reverse=True
            )

            self.scoreboard_text.insert(tk.END, "🏅 LEADERBOARD\n")
            self.scoreboard_text.insert(tk.END, "=" * 40 + "\n")

            for i, t in enumerate(standings, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                diff = t.points_for - t.points_against
                diff_sign = "+" if diff >= 0 else ""

                self.scoreboard_text.insert(
                    tk.END,
                    f"{medal} {t.name:<15} W:{t.wins} L:{t.losses} Diff:{diff_sign}{diff}\n"
                )

            if self.manager.bracket and self.manager.bracket.completed and self.manager.bracket.champion:
                self.scoreboard_text.insert(
                    tk.END, f"\n🎊 CHAMPION: {self.manager.bracket.champion.name} 🎊\n")

        # Update event log
        self.log_text.delete("1.0", tk.END)
        for entry in self.manager.event_log[-15:]:  # Show only last 15 entries
            self.log_text.insert(tk.END, f"▶ {entry}\n")
        self.log_text.see(tk.END)
