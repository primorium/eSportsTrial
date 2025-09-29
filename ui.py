import tkinter as tk
from tkinter import ttk, messagebox
from manager import TournamentManager
from models import Match


class TournamentUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Esports Tournament Manager")
        self.geometry("1000x700")
        self.manager = TournamentManager()

        self._build_layout()
        self.bind_dynamic()

    def bind_dynamic(self):
        self.num_teams_var.trace_add(
            "write", lambda *_: self._render_team_entries())

    def _build_layout(self):
        # Setup frame
        config = ttk.LabelFrame(self, text="Tournament Setup")
        config.pack(fill="x", padx=8, pady=6)

        ttk.Label(config, text="Bracket Type:").grid(
            row=0, column=0, padx=4, pady=4, sticky="w")
        self.bracket_var = tk.StringVar(value="Single Elimination")
        ttk.Combobox(config, textvariable=self.bracket_var,
                     values=["Single Elimination",
                             "Double Elimination", "Round Robin"],
                     state="readonly", width=24).grid(row=0, column=1, padx=4, pady=4, sticky="w")

        ttk.Label(config, text="Number of Teams:").grid(
            row=0, column=2, padx=4, pady=4, sticky="w")
        self.num_teams_var = tk.IntVar(value=8)
        ttk.Spinbox(config, from_=2, to=64, textvariable=self.num_teams_var, width=6).grid(
            row=0, column=3, padx=4, pady=4, sticky="w")

        self.team_entries_frame = ttk.Frame(config)
        self.team_entries_frame.grid(
            row=1, column=0, columnspan=4, sticky="ew", padx=4, pady=4)
        self.team_entries = []
        self._render_team_entries()

        ttk.Button(config, text="Generate Bracket", command=self.on_generate).grid(
            row=0, column=4, padx=8, pady=4)

        # Teams & Check-in
        left = ttk.LabelFrame(self, text="Teams & Check-In")
        left.pack(side="left", fill="y", padx=4, pady=4)

        self.teams_list = tk.Listbox(left, height=18, width=30)
        self.teams_list.pack(padx=4, pady=4)
        self.checkin_btn = ttk.Button(
            left, text="Toggle Check-In", command=self.on_checkin_toggle)
        self.checkin_btn.pack(padx=4, pady=4)
        self.all_ready_label = ttk.Label(left, text="All Ready: False")
        self.all_ready_label.pack(padx=4, pady=4)

        # Matches
        center = ttk.LabelFrame(self, text="Matches")
        center.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        self.matches_tree = ttk.Treeview(center, columns=("round", "team1", "team2", "status", "score"),
                                         show="headings", height=18)
        for col, w in [("round", 120), ("team1", 160), ("team2", 160), ("status", 120), ("score", 100)]:
            self.matches_tree.heading(col, text=col.title())
            self.matches_tree.column(col, width=w, anchor="center")
        self.matches_tree.pack(fill="both", expand=True, padx=4, pady=4)

        match_controls = ttk.Frame(center)
        match_controls.pack(fill="x", padx=4, pady=4)
        ttk.Button(match_controls, text="Start Match",
                   command=self.on_start_match).pack(side="left", padx=4)
        ttk.Label(match_controls, text="Score T1-T2:").pack(side="left", padx=4)
        self.score1_var = tk.IntVar(value=0)
        self.score2_var = tk.IntVar(value=0)
        ttk.Entry(match_controls, textvariable=self.score1_var,
                  width=5).pack(side="left")
        ttk.Entry(match_controls, textvariable=self.score2_var,
                  width=5).pack(side="left")
        ttk.Button(match_controls, text="Submit Result",
                   command=self.on_submit_result).pack(side="left", padx=4)
        ttk.Button(match_controls, text="Confirm Team 1",
                   command=lambda: self.on_confirm(1)).pack(side="left", padx=4)
        ttk.Button(match_controls, text="Confirm Team 2",
                   command=lambda: self.on_confirm(2)).pack(side="left", padx=4)

        # Bracket & Scoreboard
        right = ttk.LabelFrame(self, text="Bracket & Scoreboard")
        right.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        self.bracket_text = tk.Text(right, height=16)
        self.bracket_text.pack(fill="x", padx=4, pady=4)
        self.scoreboard_text = tk.Text(right, height=10)
        self.scoreboard_text.pack(fill="x", padx=4, pady=4)

        self.t1_label = ttk.Label(match_controls, text="T1: -")
        self.t1_label.pack(side="left", padx=4)
        self.t2_label = ttk.Label(match_controls, text="T2: -")
        self.t2_label.pack(side="left", padx=4)

        # Event log
        log_frame = ttk.LabelFrame(self, text="Event Log")
        log_frame.pack(fill="both", expand=False, padx=8, pady=6)
        self.log_text = tk.Text(log_frame, height=10)
        self.log_text.pack(fill="both", padx=4, pady=4)

        self.status = ttk.Label(self, text="Ready.")
        self.status.pack(fill="x", padx=8, pady=4)

        self.refresh_ui()

    def _render_team_entries(self):
        for w in self.team_entries:
            w.destroy()
        self.team_entries.clear()
        cols = 4
        n = self.num_teams_var.get()
        for i in range(n):
            e = ttk.Entry(self.team_entries_frame, width=24)
            e.grid(row=i // cols, column=i % cols, padx=3, pady=3)
            e.insert(0, f"Team {i+1}")
            self.team_entries.append(e)

    # -----------------------------
    # Event Handlers
    # -----------------------------
    def on_generate(self):
        names = [e.get().strip() for e in self.team_entries]
        if any(len(n) == 0 for n in names):
            messagebox.showerror("Validation", "Please fill all team names.")
            return
        self.manager.register_teams(names)
        self.manager.set_bracket(self.bracket_var.get())
        self.status.config(text="Brackets generated. Awaiting team check-ins.")
        self.refresh_ui()

    def on_checkin_toggle(self):
        sel = self.teams_list.curselection()
        if not sel:
            return
        team = self.manager.teams[sel[0]]
        team.checked_in = not team.checked_in
        self.manager.log(f"Check-In: {team.name} checked_in={team.checked_in}")

        if self.manager.bracket:
            for ri, rnd in enumerate(self.manager.bracket.rounds):
                for mi, m in enumerate(rnd, start=1):
                    if m.team1 and m.team2:
                        if m.team1.checked_in and m.team2.checked_in:
                            self.manager.log(
                                f"Pair {mi} in Round {ri+1} is ready to go.")

        if all(t.checked_in for t in self.manager.teams):
            self.all_ready_label.config(text="All Ready: True")
            self.manager.log("All teams are ready. Tournament can start.")
        self.refresh_ui()

    def on_start_match(self):
        match = self._selected_match()
        if not match:
            messagebox.showinfo("Select Match", "Select a match to start.")
            return
        self.manager.start_match(match)
        self.score1_var.set(0)
        self.score2_var.set(0)
        self.refresh_ui()

    def on_submit_result(self):
        match = self._selected_match()
        if not match:
            messagebox.showinfo(
                "Select Match", "Select a match to submit result.")
            return
        s1, s2 = self.score1_var.get(), self.score2_var.get()
        self.manager.submit_result(match, s1, s2)
        # Flash effect: briefly change background color
        self.bracket_text.config(bg="yellow")
        self.scoreboard_text.config(bg="yellow")
        self.after(300, lambda: self.bracket_text.config(bg="white"))
        self.after(300, lambda: self.scoreboard_text.config(bg="white"))
        self.refresh_ui()

    def on_confirm(self, team_index: int):
        match = self._selected_match()
        if not match:
            messagebox.showinfo("Select Match", "Select a match to confirm.")
            return
        self.manager.confirm_winner(match, team_index)
        self.bracket_text.config(bg="lightgreen")
        self.scoreboard_text.config(bg="lightblue")
        self.after(400, lambda: self.bracket_text.config(bg="white"))
        self.after(400, lambda: self.scoreboard_text.config(bg="white"))
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

    # -----------------------------
    # UI Refresh
    # -----------------------------
    def refresh_ui(self):
        # Teams
        self.teams_list.delete(0, tk.END)
        for t in self.manager.teams:
            self.teams_list.insert(
                tk.END, f"{t.name} | CheckedIn={t.checked_in}")
        self.all_ready_label.config(
            text=f"All Ready: {self.manager.bracket.is_ready_to_start() if self.manager.bracket else False}")

        match = self._selected_match()
        if match:
            self.t1_label.config(
                text=f"T1: {match.team1.name if match.team1 else 'BYE'}")
            self.t2_label.config(
                text=f"T2: {match.team2.name if match.team2 else 'BYE'}")
        else:
            self.t1_label.config(text="T1: -")
            self.t2_label.config(text="T2: -")

        # Matches table
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
        if self.manager.bracket:
            for rnd in self.manager.bracket.rounds:
                for m in rnd:
                    self.matches_tree.insert("", "end", iid=m.id,
                                             values=(f"Round {m.round_index+1}",
                                                     m.team1.name if m.team1 else "BYE",
                                                     m.team2.name if m.team2 else "BYE",
                                                     m.status,
                                                     f"{m.score[0]}-{m.score[1]}"))

        # Bracket text display
        self.bracket_text.delete("1.0", tk.END)
        if self.manager.bracket:
            self.bracket_text.insert(
                tk.END, f"Bracket Type: {self.manager.bracket.type_name}\n\n")
            for ri, rnd in enumerate(self.manager.bracket.rounds):
                self.bracket_text.insert(tk.END, f"Round {ri+1}:\n")
                for m in rnd:
                    line = f"  {m.team1.name if m.team1 else 'BYE'} vs {m.team2.name if m.team2 else 'BYE'}"
                    if m.status == "Completed" and m.winner:
                        line += f" → Winner: {m.winner.name}"
                    self.bracket_text.insert(
                        tk.END, line + f" [{m.status}] {m.score[0]}-{m.score[1]}\n")
                self.bracket_text.insert(tk.END, "\n")

        # Scoreboard
        self.scoreboard_text.delete("1.0", tk.END)
        if self.manager.teams:
            standings = sorted(
                self.manager.teams,
                key=lambda t: (t.wins, t.points_for - t.points_against),
                reverse=True
            )
            self.scoreboard_text.insert(tk.END, "Scoreboard:\n")
            for i, t in enumerate(standings, 1):
                self.scoreboard_text.insert(
                    tk.END,
                    f"{i}. {t.name} | W:{t.wins} L:{t.losses} PF:{t.points_for} PA:{t.points_against}\n"
                )
            if self.manager.bracket and self.manager.bracket.completed and self.manager.bracket.champion:
                self.scoreboard_text.insert(
                    tk.END, f"\nChampion: {self.manager.bracket.champion.name}\n")

        # Event log
        self.log_text.delete("1.0", tk.END)
        for entry in self.manager.event_log[-200:]:
            self.log_text.insert(tk.END, entry + "\n")
