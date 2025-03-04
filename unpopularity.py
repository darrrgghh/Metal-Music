#!/usr/bin/env python3
"""
Spotify Popularity Analyzer with:
- File menu ("Unpopularity export...")
- Horizontal PanedWindow splitting left vs. right
- Vertical PanedWindow splitting top vs. bottom charts on the right
- Charts fill the entire allocated space
- Press Enter in the search bar to trigger search
- Unpopularity export includes time zone info and "Spotify API" as the source
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import json
import datetime

# Replace these with your actual Spotify credentials
CLIENT_ID = "c2b19885fbef4cd3a0f5230ddf855b28"
CLIENT_SECRET = "2203859547ef47038e231e2d8c0fe8fc"

class SpotifyAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spotify Popularity Analyzer (PanedWindows + Menu, Full-Space Charts)")
        self.geometry("1200x800")
        self.minsize(800, 600)
        self.resizable(True, True)

        # Set up Spotipy
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

        # Data holders
        self.artist_id = None
        self.artist_name = None
        # We'll store (album_id, album_name, popularity, release_year)
        self.albums = []
        # We'll store track-level data for the selected album
        self.tracks = []

        self._create_menubar()
        self._create_main_layout()

    def _create_menubar(self):
        """Creates the top menu bar with File -> Unpopularity export..."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)

        # "Unpopularity export..." item
        file_menu.add_command(label="Unpopularity export...", command=self.export_unpopularity)

    def _create_main_layout(self):
        """Builds the main UI using PanedWindows to allow resizable splits and tries to occupy full space for charts."""

        # 1) Top frame for the search bar
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Layout for the search bar
        top_frame.columnconfigure(0, weight=0)
        top_frame.columnconfigure(1, weight=1)

        ttk.Label(top_frame, text="Search Artist:").grid(row=0, column=0, sticky="w")
        self.search_entry = ttk.Entry(top_frame, width=30)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5)

        # Bind Enter key to trigger search
        self.search_entry.bind("<Return>", lambda e: self.search_artist())

        search_btn = ttk.Button(top_frame, text="Search", command=self.search_artist)
        search_btn.grid(row=0, column=2, padx=5)

        # 2) Main horizontal PanedWindow
        main_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left frame: Artist Matches + Discography
        left_frame = ttk.Frame(main_paned)
        left_frame.pack(fill=tk.BOTH, expand=True)

        # Inside left_frame, we can pack the widgets
        ttk.Label(left_frame, text="Artist Matches:").pack(anchor=tk.NW)
        self.matches_listbox = tk.Listbox(left_frame, height=5)
        self.matches_listbox.pack(fill=tk.X)
        self.matches_listbox.bind("<<ListboxSelect>>", self.on_select_artist)

        ttk.Label(left_frame, text="Discography (Albums):").pack(anchor=tk.NW, pady=(10, 0))
        self.albums_listbox = tk.Listbox(left_frame, height=15)
        self.albums_listbox.pack(fill=tk.BOTH, expand=True)
        self.albums_listbox.bind("<<ListboxSelect>>", self.on_select_album)

        main_paned.add(left_frame, minsize=200)

        # Right side: a vertical PanedWindow for top/bottom charts
        right_paned = tk.PanedWindow(main_paned, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        right_paned.pack(fill=tk.BOTH, expand=True)

        main_paned.add(right_paned, minsize=400)

        # -- TOP (album) sub-frame
        album_frame = ttk.Frame(right_paned)
        album_frame.pack(fill=tk.BOTH, expand=True)

        # We'll create a sub-sub-frame that uses pack for the figure + toolbar
        album_pack_frame = ttk.Frame(album_frame)
        album_pack_frame.pack(fill=tk.BOTH, expand=True)

        self.album_fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.album_ax = self.album_fig.add_subplot(111)
        self.album_ax.set_title("Album Popularity", fontsize=8)
        self.album_ax.tick_params(axis='x', labelsize=6)
        self.album_ax.tick_params(axis='y', labelsize=6)

        self.album_canvas = FigureCanvasTkAgg(self.album_fig, master=album_pack_frame)
        album_canvas_widget = self.album_canvas.get_tk_widget()
        album_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Bind <Configure> to resize the figure
        album_canvas_widget.bind("<Configure>",
            lambda e: self._on_resize_figure(e, self.album_fig, self.album_canvas))

        self.album_toolbar = NavigationToolbar2Tk(self.album_canvas, album_pack_frame)
        self.album_toolbar.update()
        self.album_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        right_paned.add(album_frame, minsize=200)

        # -- BOTTOM (track) sub-frame
        track_frame = ttk.Frame(right_paned)
        track_frame.pack(fill=tk.BOTH, expand=True)

        track_pack_frame = ttk.Frame(track_frame)
        track_pack_frame.pack(fill=tk.BOTH, expand=True)

        self.track_fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.track_ax = self.track_fig.add_subplot(111)
        self.track_ax.set_title("Track Popularity", fontsize=8)
        self.track_ax.tick_params(axis='x', labelsize=6)
        self.track_ax.tick_params(axis='y', labelsize=6)

        self.track_canvas = FigureCanvasTkAgg(self.track_fig, master=track_pack_frame)
        track_canvas_widget = self.track_canvas.get_tk_widget()
        track_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        track_canvas_widget.bind("<Configure>",
            lambda e: self._on_resize_figure(e, self.track_fig, self.track_canvas))

        self.track_toolbar = NavigationToolbar2Tk(self.track_canvas, track_pack_frame)
        self.track_toolbar.update()
        self.track_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        right_paned.add(track_frame, minsize=200)

        # Set initial sash positions after a brief delay to let geometry settle
        self.after(100, lambda: main_paned.sashpos(0, 600))    # ~300 px for left panel
        self.after(200, lambda: right_paned.sashpos(0, 600))   # ~300 px for top chart

        # Optional bottom controls: Zoom In/Out, Raw Data
        bottom_ctrl_frame = ttk.Frame(self)
        bottom_ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        zoom_in_btn = ttk.Button(bottom_ctrl_frame, text="Zoom In", command=self._zoom_in)
        zoom_in_btn.pack(side=tk.LEFT, padx=5)
        zoom_out_btn = ttk.Button(bottom_ctrl_frame, text="Zoom Out", command=self._zoom_out)
        zoom_out_btn.pack(side=tk.LEFT, padx=5)
        raw_data_btn = ttk.Button(bottom_ctrl_frame, text="Raw Data", command=self.show_raw_data)
        raw_data_btn.pack(side=tk.LEFT, padx=5)

    def _on_resize_figure(self, event, figure, canvas):
        """Resizes the Matplotlib Figure whenever the canvas widget is resized."""
        width = event.width
        height = event.height
        figure.set_size_inches(width / figure.dpi, height / figure.dpi, forward=True)
        canvas.draw()

    # ------------------------------
    # Spotify logic
    # ------------------------------
    def search_artist(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showinfo("Info", "Please enter an artist name.")
            return

        self.matches_listbox.delete(0, tk.END)
        try:
            results = self.sp.search(q=query, type='artist', limit=5)
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
            return

        artists = results['artists']['items']
        if not artists:
            self.matches_listbox.insert(tk.END, "No matches found.")
            return

        for artist in artists:
            entry = f"{artist['name']} ({artist['id']})"
            self.matches_listbox.insert(tk.END, entry)

    def on_select_artist(self, event):
        selection = self.matches_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        text = self.matches_listbox.get(idx)
        if "No matches found." in text:
            return
        try:
            artist_id = text.split("(")[1].split(")")[0]
        except:
            messagebox.showerror("Error", "Unable to parse artist ID.")
            return
        try:
            artist_info = self.sp.artist(artist_id)
        except Exception as e:
            messagebox.showerror("Error", f"Artist retrieval failed: {e}")
            return

        self.artist_id = artist_id
        self.artist_name = artist_info["name"]
        self.fetch_albums()

    def fetch_albums(self):
        """Fetch all albums for the current artist, store them with popularity and release year."""
        self.albums_listbox.delete(0, tk.END)
        self.albums.clear()
        offset = 0
        while True:
            try:
                results = self.sp.artist_albums(self.artist_id, album_type='album', limit=50, offset=offset)
            except Exception as e:
                messagebox.showerror("Error", f"Album retrieval failed: {e}")
                return
            items = results["items"]
            if not items:
                break
            for album in items:
                album_id = album["id"]
                album_name = album["name"]
                try:
                    details = self.sp.album(album_id)
                    pop = details.get("popularity", 0)
                    release_date = details.get("release_date", "unknown")
                    release_year = release_date.split("-")[0]
                except:
                    pop = 0
                    release_year = "????"
                self.albums.append((album_id, album_name, pop, release_year))
            offset += 50
            if len(items) < 50:
                break

        for (a_id, a_name, pop, year) in self.albums:
            self.albums_listbox.insert(tk.END, f"{a_name} ({year}) [pop: {pop}]")

        self.update_album_graph()

    def update_album_graph(self):
        self.album_ax.clear()
        if not self.albums:
            self.album_ax.set_title("No Albums Found", fontsize=8)
            self.album_canvas.draw()
            return

        sorted_albums = sorted(self.albums, key=lambda x: x[2], reverse=True)
        names = [f"{a[1]} ({a[3]})" for a in sorted_albums]  # album name + year
        pops = [a[2] for a in sorted_albums]

        self.album_ax.barh(names, pops, color="skyblue")
        self.album_ax.invert_yaxis()
        self.album_ax.set_title(f"{self.artist_name} - Albums", fontsize=8)
        self.album_ax.set_xlabel("Popularity", fontsize=6)
        self.album_ax.tick_params(axis='x', labelsize=6)
        self.album_ax.tick_params(axis='y', labelsize=6)
        self.album_canvas.draw()

    def on_select_album(self, event):
        selection = self.albums_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx >= len(self.albums):
            return
        album_id, album_name, pop, year = self.albums[idx]
        try:
            album_tracks = self.sp.album_tracks(album_id, limit=50)['items']
        except Exception as e:
            messagebox.showerror("Error", f"Track retrieval failed: {e}")
            return

        self.tracks.clear()
        for track in album_tracks:
            track_id = track["id"]
            track_name = track["name"]
            try:
                full_track = self.sp.track(track_id)
                track_pop = full_track.get("popularity", 0)
            except:
                track_pop = 0
            self.tracks.append({
                "id": track_id,
                "name": track_name,
                "popularity": track_pop,
                "raw_data": full_track
            })

        self.update_track_graph(album_name)

    def update_track_graph(self, album_name):
        self.track_ax.clear()
        if not self.tracks:
            self.track_ax.set_title("No Tracks Found", fontsize=8)
            self.track_canvas.draw()
            return

        sorted_tracks = sorted(self.tracks, key=lambda x: x["popularity"], reverse=True)
        names = [t["name"] for t in sorted_tracks]
        pops = [t["popularity"] for t in sorted_tracks]

        self.track_ax.barh(names, pops, color="orange")
        self.track_ax.invert_yaxis()
        self.track_ax.set_title(f"{album_name} - Track Popularity", fontsize=8)
        self.track_ax.set_xlabel("Popularity", fontsize=6)
        self.track_ax.tick_params(axis='x', labelsize=6)
        self.track_ax.tick_params(axis='y', labelsize=6)
        self.track_canvas.draw()

    # --------------------------------
    # Zoom In/Out demonstration
    # --------------------------------
    def _zoom_in(self):
        for ax, canvas in [(self.album_ax, self.album_canvas), (self.track_ax, self.track_canvas)]:
            x_left, x_right = ax.get_xlim()
            center = (x_left + x_right) / 2
            new_width = (x_right - x_left) * 0.8
            ax.set_xlim(center - new_width/2, center + new_width/2)
            canvas.draw()

    def _zoom_out(self):
        for ax, canvas in [(self.album_ax, self.album_canvas), (self.track_ax, self.track_canvas)]:
            x_left, x_right = ax.get_xlim()
            center = (x_left + x_right) / 2
            new_width = (x_right - x_left) / 0.8
            ax.set_xlim(center - new_width/2, center + new_width/2)
            canvas.draw()

    # --------------------------------
    # Raw Data
    # --------------------------------
    def show_raw_data(self):
        raw_win = tk.Toplevel(self)
        raw_win.title("Raw Data")
        raw_win.geometry("800x600")

        text_area = scrolledtext.ScrolledText(raw_win, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        if self.tracks:
            data_list = []
            for t in self.tracks:
                data_list.append(self._clean_spotify_dict(t["raw_data"]))
            data_to_display = data_list
        elif self.albums:
            data_list = []
            for (a_id, a_name, pop, year) in self.albums:
                data_list.append({"id": a_id, "name": a_name, "popularity": pop, "year": year})
            data_to_display = data_list
        else:
            data_to_display = "No data available."

        try:
            text_area.insert(tk.END, json.dumps(data_to_display, indent=2))
        except:
            text_area.insert(tk.END, str(data_to_display))

    def _clean_spotify_dict(self, raw_item):
        if not isinstance(raw_item, dict):
            return raw_item
        copy_item = dict(raw_item)
        for big_field in ["available_markets", "images", "artists"]:
            if big_field in copy_item:
                del copy_item[big_field]
        if "album" in copy_item and isinstance(copy_item["album"], dict):
            alb = dict(copy_item["album"])
            for bf in ["available_markets", "images", "artists"]:
                if bf in alb:
                    del alb[bf]
            copy_item["album"] = alb
        return copy_item

    # --------------------------------
    # Unpopularity Export
    # --------------------------------
    def export_unpopularity(self):
        """Exports a .txt file with the artist, 3 least popular albums, and 3 least popular tracks per album.
           Also includes time zone info and source = Spotify API."""
        if not self.artist_id:
            messagebox.showinfo("Info", "No artist selected.")
            return

        if not self.albums:
            messagebox.showinfo("Info", "No album data available. Please search and select an artist first.")
            return

        # Sort albums by ascending popularity
        sorted_albums = sorted(self.albums, key=lambda x: x[2])
        # Take up to 3
        least_pop_albums = sorted_albums[:3]

        # We'll build a text output
        lines = []
        dt = datetime.datetime.now().astimezone()  # local time with time zone
        lines.append(f"Unpopularity Export for Artist: {self.artist_name}")
        lines.append(f"Date/Time (Local): {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        lines.append("Source: Spotify API")
        lines.append("")

        for (alb_id, alb_name, alb_pop, alb_year) in least_pop_albums:
            lines.append(f"Album: {alb_name} ({alb_year}), Popularity: {alb_pop}")

            # fetch track info for that album
            try:
                album_tracks = self.sp.album_tracks(alb_id, limit=50)['items']
            except Exception as e:
                lines.append(f"  Error fetching tracks: {e}")
                continue

            # build a list of (track_name, track_pop)
            track_data = []
            for tr in album_tracks:
                tr_id = tr["id"]
                tr_name = tr["name"]
                try:
                    full_tr = self.sp.track(tr_id)
                    tr_pop = full_tr.get("popularity", 0)
                except:
                    tr_pop = 0
                track_data.append((tr_name, tr_pop))

            # sort by ascending popularity
            track_data.sort(key=lambda x: x[1])
            least_tracks = track_data[:3]
            for (t_name, t_pop) in least_tracks:
                lines.append(f"   Track: {t_name}, Popularity: {t_pop}")

            lines.append("")

        output_text = "\n".join(lines)

        # Prompt user for a file location
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Unpopularity Export"
        )
        if not save_path:
            return  # user canceled

        # Write to file
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(output_text)
            messagebox.showinfo("Export Complete", f"Data exported to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write file: {e}")

def main():
    app = SpotifyAnalyzer()
    app.mainloop()

if __name__ == "__main__":
    main()
