#!/usr/bin/env python3




"""
Spotify Popularity Analyzer
---------------------------
This program was created for our research on metal music. It gathers "popularity" metrics from the Spotify API
to help identify the least popular releases of a particular artist. Main features include:

- A File menu with "Export Unpopularity..." to export research-relevant data.
- A horizontal PanedWindow: left panel for artist matches and discography, right panel for charts.
- A vertical PanedWindow on the right: top for an album popularity chart, bottom for a track popularity chart.
- The search bar triggers search on pressing Enter.
- "Export Unpopularity..." includes local time zone info and "Spotify API" as the source.
- Live albums/tracks (those with 'live' in their name) are skipped. We did it on purpsose because many live-realeasese are much less popular, though they
often contain songs that are very popular themselves (within their respected realeses)
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

# Replace these with your actual Spotify credentials (you'll need to have a Spotify for Developers account)
CLIENT_ID = "ENTER_YOUR_CLIENT_ID_HERE"
CLIENT_SECRET = "ENTER_YOUR_CLIENT_SECRET_HERE"
# both are easily obtained from Spotify

class SpotifyAnalyzer(tk.Tk):


    # ------------------------------
    # UI Functions & stuff
    # ------------------------------


    def __init__(self):
        """
        Initializes the main application window, sets up the Spotify client,
        and creates the GUI layout (menu bar, PanedWindows, charts, etc.).
        Also wraps Spotify client initialization in a try/except to catch connectivity errors.
        This part of a program is up to you to configure: you can play with frames layout, size, fonts, anything.
        Here, I used my standard UI-prompt, which I use for most of my programs.
        """

        # feel free to adjust any of these parameters
        super().__init__()
        self.title("Spotify 'UN'Popularity Analyzer")
        self.geometry("1200x800")
        self.minsize(800, 600)
        self.resizable(True, True)

        # Set up Spotipy authentication with error handling (i.e. when there's no internet connection)
        try:
            auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET)
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to authenticate with Spotify: {e}")
            self.destroy()  # close the app if no connection
            return

        # Data holders:
        self.artist_id = None
        self.artist_name = None
        # Albums stored as (album_id, album_name, popularity, release_year)
        self.albums = []
        # Track-level data for the selected album
        self.current_album_tracks = []

        self._create_menubar()
        self._create_main_layout()

    def _create_menubar(self):
        """
        Builds a menu bar with a File menu that includes an "Export Unpopularity..."
        command for exporting the least popular album and track data, which is the core functionality of the program
        (since it is designed for research)
        """
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)

        # "Export Unpopularity..." calls export_unpopularity() function here
        file_menu.add_command(label="Export Unpopularity...", command=self.export_unpopularity)

    def _create_main_layout(self):
        """
        Builds the main UI using two PanedWindows:
         - A horizontal PanedWindow splits the left panel (artist matches/discography) and right panel (charts).
         - A vertical PanedWindow on the right splits the top (album chart) and bottom (track chart) areas.
       all are resizable. Default Tkinter controls are enabled as well
        """
        # Top frame for the search bar
        top_frame = ttk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        top_frame.columnconfigure(0, weight=0)
        top_frame.columnconfigure(1, weight=1)

        ttk.Label(top_frame, text="Search Artist:").grid(row=0, column=0, sticky="w")
        self.search_entry = ttk.Entry(top_frame, width=30)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_artist())

        search_btn = ttk.Button(top_frame, text="Search", command=self.search_artist)
        search_btn.grid(row=0, column=2, padx=5)

        # Main horizontal PanedWindow (left = artist/discography, right = charts)
        main_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left frame: Artist Matches + Discography
        left_frame = ttk.Frame(main_paned)
        left_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(left_frame, text="Artist Matches:").pack(anchor=tk.NW)
        self.matches_listbox = tk.Listbox(left_frame, height=5)
        self.matches_listbox.pack(fill=tk.X)
        self.matches_listbox.bind("<<ListboxSelect>>", self.on_select_artist)

        ttk.Label(left_frame, text="Discography (Albums):").pack(anchor=tk.NW, pady=(10, 0))
        self.albums_listbox = tk.Listbox(left_frame, height=15)
        self.albums_listbox.pack(fill=tk.BOTH, expand=True)
        self.albums_listbox.bind("<<ListboxSelect>>", self.on_select_album)

        main_paned.add(left_frame, minsize=200)

        # Right PanedWindow for charts (split vertically)
        right_paned = tk.PanedWindow(main_paned, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        right_paned.pack(fill=tk.BOTH, expand=True)
        main_paned.add(right_paned, minsize=400)

        # Top sub-frame for the album chart
        album_frame = ttk.Frame(right_paned)
        album_frame.pack(fill=tk.BOTH, expand=True)
        album_pack_frame = ttk.Frame(album_frame)
        album_pack_frame.pack(fill=tk.BOTH, expand=True)

        # Create the album chart figure
        self.album_fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.album_ax = self.album_fig.add_subplot(111)
        self.album_ax.set_title("Album Popularity", fontsize=8)
        self.album_ax.tick_params(axis='x', labelsize=6)
        self.album_ax.tick_params(axis='y', labelsize=6)

        self.album_canvas = FigureCanvasTkAgg(self.album_fig, master=album_pack_frame)
        album_canvas_widget = self.album_canvas.get_tk_widget()
        album_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create and pack the toolbar for the album chart
        self.album_toolbar = NavigationToolbar2Tk(self.album_canvas, album_pack_frame)
        self.album_toolbar.update()
        self.album_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        right_paned.add(album_frame, minsize=200)

        # Bottom sub-frame for the track chart
        track_frame = ttk.Frame(right_paned)
        track_frame.pack(fill=tk.BOTH, expand=True)
        track_pack_frame = ttk.Frame(track_frame)
        track_pack_frame.pack(fill=tk.BOTH, expand=True)

        # Create the track chart figure
        self.track_fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.track_ax = self.track_fig.add_subplot(111)
        self.track_ax.set_title("Track Popularity", fontsize=8)
        self.track_ax.tick_params(axis='x', labelsize=6)
        self.track_ax.tick_params(axis='y', labelsize=6)

        self.track_canvas = FigureCanvasTkAgg(self.track_fig, master=track_pack_frame)
        track_canvas_widget = self.track_canvas.get_tk_widget()
        track_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create and pack the toolbar for the track chart
        self.track_toolbar = NavigationToolbar2Tk(self.track_canvas, track_pack_frame)
        self.track_toolbar.update()
        self.track_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        right_paned.add(track_frame, minsize=200)

        # Bottom control frame for Raw Data button (other controls like Zoom are removed)
        bottom_ctrl_frame = ttk.Frame(self)
        bottom_ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        raw_data_btn = ttk.Button(bottom_ctrl_frame, text="Raw Data", command=self.show_raw_data)
        raw_data_btn.pack(side=tk.LEFT, padx=5)

    # ------------------------------
    # Spotify API Functions
    # ------------------------------
    def search_artist(self):
        """
        Called when 'Search' button is clicked or 'Enter' button on the keyboard is pressed.
        Queries Spotify for up to 5 matching artists and displays them in the matches listbox.
        """
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showinfo("Info", "Please enter an artist name.")
            return

        self.matches_listbox.delete(0, tk.END)
        try:
            results = self.sp.search(q=query, type='artist', limit=5) # adjust this to get more matches.
            # you'll need to scroll the results down/up with the mouse, no UI is implemented for this purpose.

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
        """
        Triggered when an artist is selected from the matches listbox.
        Parses the artist ID, fetches album data (skipping "live" releases), and updates the album chart.
        """
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
        """
        Fetches all albums for the selected artist (again, excluding albums with 'live' in the name).
        Stores them in self.albums and populates the discography listbox.
        """
        self.albums_listbox.delete(0, tk.END)
        self.albums.clear()
        offset = 0

        while True:
            try:
                # Request only album_type='album', but you can adjust this to include more types of releases
                results = self.sp.artist_albums(self.artist_id, album_type='album', limit=50, offset=offset)
            except Exception as e:
                messagebox.showerror("Error", f"Album retrieval failed: {e}")
                return

            items = results["items"]
            if not items:
                break

            for album in items:
                album_name = album.get("name", "")
                # Skip albums whose name contains "live" - for the purpose of our research only
                if "live" in album_name.lower():
                    continue

                album_id = album["id"]
                try:
                    details = self.sp.album(album_id)
                    pop = details.get("popularity", 0)
                    release_date = details.get("release_date", "unknown")
                    release_year = release_date.split("-")[0]
                except Exception:
                    pop = 0
                    release_year = "????"

                self.albums.append((album_id, album_name, pop, release_year))

            offset += 50
            if len(items) < 50:
                break

        # Populate the albums listbox
        for (alb_id, alb_name, alb_pop, alb_year) in self.albums:
            display_str = f"{alb_name} ({alb_year}) [pop: {alb_pop}]"
            self.albums_listbox.insert(tk.END, display_str)

        self.update_album_graph()

    def update_album_graph(self):
        """
        Updates the album popularity bar chart using self.albums.
        """
        self.album_ax.clear()
        if not self.albums:
            self.album_ax.set_title("No Albums Found")
            self.album_canvas.draw()
            return

        sorted_albums = sorted(self.albums, key=lambda x: x[2], reverse=True)
        names = [f"{a[1]} ({a[3]})" for a in sorted_albums]
        pops = [a[2] for a in sorted_albums]

        self.album_ax.barh(names, pops, color="skyblue")
        self.album_ax.invert_yaxis()  # Highest at top
        self.album_ax.set_title(f"{self.artist_name} - Albums")
        self.album_ax.set_xlabel("Popularity")
        self.album_canvas.draw()

    def on_select_album(self, event):
        """
        Triggered when an album is selected from the discography listbox.
        Fetches track data for the album (here, we also skip tracks with 'live' in the name)
        and updates the track popularity chart.
        """
        selection = self.albums_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx >= len(self.albums):
            return
        album_id, album_name, alb_pop, alb_year = self.albums[idx]

        try:
            album_tracks = self.sp.album_tracks(album_id, limit=50)['items']
        except Exception as e:
            messagebox.showerror("Error", f"Track retrieval failed: {e}")
            return

        self.current_album_tracks = []
        for track in album_tracks:
            track_name = track.get("name", "")
            if "live" in track_name.lower():
                continue

            track_id = track["id"]
            try:
                full_track = self.sp.track(track_id)
                track_pop = full_track.get("popularity", 0)
            except Exception:
                track_pop = 0
            self.current_album_tracks.append({
                "id": track_id,
                "name": track_name,
                "popularity": track_pop
            })

        self._update_track_graph(album_name, self.current_album_tracks)

    def _update_track_graph(self, album_name, track_list):
        """
        Updates the track popularity bar chart using the track data for the selected album.
        """
        self.track_ax.clear()
        if not track_list:
            self.track_ax.set_title("No Tracks Found")
            self.track_canvas.draw()
            return

        # Sort tracks by popularity descending
        sorted_tracks = sorted(track_list, key=lambda x: x["popularity"], reverse=True)
        track_names = [t["name"] for t in sorted_tracks]
        track_pops = [t["popularity"] for t in sorted_tracks]

        self.track_ax.barh(track_names, track_pops, color="orange")
        self.track_ax.invert_yaxis()  # Highest at top
        self.track_ax.set_xlabel("Popularity")
        self.track_ax.set_title(f"Tracks in '{album_name}'")
        self.track_canvas.draw()

    def show_raw_data(self):
        """
        Opens a new window displaying JSON data of the current tracks or albums,
        formatted with indentation for readability. Most of the data provided by Spotify API is irrelevant to our research, but you can
        alter this part as well to het more data you need.
        """
        raw_win = tk.Toplevel(self)
        raw_win.title("Raw Data")
        raw_win.geometry("800x600")

        text_area = scrolledtext.ScrolledText(raw_win, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        if self.current_album_tracks:
            data_list = self.current_album_tracks
        elif self.albums:
            data_list = [{"id": a_id, "name": a_name, "popularity": pop, "year": year}
                         for (a_id, a_name, pop, year) in self.albums]
        else:
            data_list = "No data available."

        text_area.insert(tk.END, json.dumps(data_list, indent=2))

    def export_unpopularity(self):
        """
        Exports a .txt file containing the artist's name, up to 3 least popular albums,
        and for each album, up to 3 least popular tracks. The export includes local time zone
        information and indicates "Spotify API" as the source.
        Live releases (albums/tracks with "live" in the name) are skipped.
        """
        if not self.artist_id:
            messagebox.showinfo("Info", "No artist selected.")
            return

        if not self.albums:
            messagebox.showinfo("Info", "No album data available. Please search and select an artist first.")
            return

        sorted_albums = sorted(self.albums, key=lambda x: x[2])
        least_pop_albums = sorted_albums[:3]  # Up to 3 least popular albums

        lines = []
        dt = datetime.datetime.now().astimezone()
        lines.append(f"Unpopularity Export for Artist: {self.artist_name}")
        lines.append(f"Date/Time (Local): {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        lines.append("Source: Spotify API")
        lines.append("")

        for (alb_id, alb_name, alb_pop, alb_year) in least_pop_albums:
            lines.append(f"Album: {alb_name} ({alb_year}), Popularity: {alb_pop}")
            try:
                album_tracks = self.sp.album_tracks(alb_id, limit=50)['items']
            except Exception as e:
                lines.append(f"  Error fetching tracks: {e}")
                lines.append("")
                continue

            track_data = []
            for tr in album_tracks:
                tr_name = tr.get("name", "")
                if "live" in tr_name.lower():
                    continue
                tr_id = tr["id"]
                try:
                    full_tr = self.sp.track(tr_id)
                    tr_pop = full_tr.get("popularity", 0)
                except Exception:
                    tr_pop = 0
                track_data.append((tr_name, tr_pop))

            track_data.sort(key=lambda x: x[1])
            least_tracks = track_data[:3]
            for (t_name, t_pop) in least_tracks:
                lines.append(f"   Track: {t_name}, Popularity: {t_pop}")
            lines.append("")

        output_text = "\n".join(lines)

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Unpopularity Export"
        )
        if not save_path:
            return

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
