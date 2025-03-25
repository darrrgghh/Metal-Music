#!/usr/bin/env python3
"""
Spotify {UN}Popularity Analyzer 0.4

This program was created for our research on metal music. It gathers "popularity" metrics from the Spotify API
to help identify the least popular releases of a particular artist. Main features include:

- A File menu with:
    - "Export Unpopularity..." to export research-relevant data.
    - "Export Count": set how many least popular items you want to export 1 to 5 or 'all' (exports all active discography when the artist is selected)
    - "Raw Data" to display quantitative JSON data.
    - "Exit" to, you know...>>>.(8.8).>>>...
- Panels for artist matches and discography on the left, right panel for charts (top for an album popularity chart, bottom for a track popularity chart).
- The search bar triggers a search when the Enter key is pressed (or click on search button)
- "Export Unpopularity..." exports three least popular albums of a chosen artist and three least popular songs on those albums.
  Also includes local time zone info and "Spotify API" as the source.
- This version of "Spotify {UN}Popularity Analyzer" is designed for the research purposes and only searches for releases labeled as "album".
  Live albums and tracks (those with "live" in the name) are skipped. We did it on purpose because many live releases are much less popular,
  even though they often contain songs that are very popular themselves (within their respective releases). Also,
  for accuracy and to avoid false data, releases labeled as 'Remastered,' 'Re-issue,' 'Reissue,' 'Demo,' or 'Edition' are excluded.
- Click on an item in discography and press 'delete' on your keyboard to exclude
Future improvements:
- Add a Filter menu that allows users to include or exclude various release types (e.g., EP, LP, Single, Live, Remastered, Demo).
  By default, all release types would be selected, and users could simply uncheck any categories they wish to exclude,
  providing flexible filtering for different research or personal needs.
- Add various options for exporting data.

run this to make a build
pyinstaller --onefile --noconsole unpopularity.py --hidden-import=spotipy.oauth2

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
# both are easily obtained from Spotify
CLIENT_ID = "c2b19885fbef4cd3a0f5230ddf855b28"
CLIENT_SECRET = "2203859547ef47038e231e2d8c0fe8fc"

class SpotifyAnalyzer(tk.Tk):
    # ------------------------------
    # UI Functions & stuff
    # ------------------------------
    def __init__(self):
        super().__init__()
        self.title("Spotify Popularity Analyzer 0.5")
        self.geometry("1200x800")
        self.minsize(800, 600)
        self.resizable(True, True)
        # Set up Spotipy authentication with error handling (e.g., when there's no internet connection or no spotify API credentials)
        try:
            auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID,
                                                    client_secret=CLIENT_SECRET)
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to authenticate with Spotify: {e}")
            self.destroy()
            return
        self.artist_id = None
        self.artist_name = None
        self.albums = []
        self.current_album_tracks = []
        self.settings = {
            "types": ["album", "single", "compilation"],
            "filters": [],  # По умолчанию — без фильтрации
            "albums_to_export": "3",
            "tracks_to_export": "5"
        }

        self._create_menubar()
        self._create_main_layout()

    def _create_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Popularity...", command=self.export_popularity)
        file_menu.add_command(label="Settings", command=self.open_settings_window)  # Новое!
        file_menu.add_command(label="Raw Data", command=self.show_raw_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)

    def open_settings_window(self):
        settings_win = tk.Toplevel(self)
        settings_win.title("Settings")
        settings_win.geometry("500x480")
        settings_win.resizable(False, False)

        label_font = ("Arial", 11, "bold")
        checkbox_font = ("Arial", 10)

        # Секция: Типы релизов
        tk.Label(settings_win, text="To Look For:", font=label_font, fg='black').grid(row=0, column=0, sticky="w", padx=10,
                                                                                   pady=(10, 0))
        self.release_types = {
            key: tk.BooleanVar(value=(key in self.settings["types"]))
            for key in ["album", "single", "compilation", "appears_on"]
        }
        for i, (rtype, var) in enumerate(self.release_types.items()):
            tk.Checkbutton(settings_win, text=rtype.capitalize(), variable=var, font=checkbox_font).grid(row=1,
                                                                                                         column=i,
                                                                                                         padx=10,
                                                                                                         sticky="w")

        # Секция: Фильтрация по ключевым словам
        tk.Label(settings_win, text="To Filter Out:", font=label_font, fg='black').grid(row=2, column=0, sticky="w",
                                                                                          padx=10, pady=(15, 0))
        keywords_list = ["demo", "live", "remastered", "edition", "deluxe", "reissue", "remix", "edit", "feat"]
        self.filter_keywords = {
            key: tk.BooleanVar(value=(key in self.settings["filters"]))
            for key in keywords_list
        }
        for i, (keyword, var) in enumerate(self.filter_keywords.items()):
            row = 3 + i // 3
            col = i % 3
            tk.Checkbutton(settings_win, text=keyword.capitalize(), variable=var, font=checkbox_font).grid(row=row,
                                                                                                           column=col,
                                                                                                           padx=10,
                                                                                                           sticky="w")

        # Кол-во альбомов и треков
        tk.Label(settings_win, text="Export Settings", font=label_font, fg='black').grid(row=7, column=0, sticky="w",
                                                                                         padx=10, pady=(20, 0))
        tk.Label(settings_win, text="Albums to export:", font=checkbox_font).grid(row=8, column=0, padx=10, sticky="w")
        self.album_export_var = tk.StringVar(value=self.settings.get("albums_to_export", "3"))
        album_options = ["1", "2", "3", "4", "5", "All"]
        ttk.OptionMenu(settings_win, self.album_export_var, self.album_export_var.get(), *album_options).grid(row=8,
                                                                                                              column=1,
                                                                                                              sticky="w")

        tk.Label(settings_win, text="Tracks per album:", font=checkbox_font).grid(row=9, column=0, padx=10,
                                                                                  pady=(10, 0), sticky="w")
        self.track_export_var = tk.StringVar(value=self.settings.get("tracks_to_export", "3"))
        track_options = ["1", "2", "3", "4", "5", "All"]
        ttk.OptionMenu(settings_win, self.track_export_var, self.track_export_var.get(), *track_options).grid(row=9,
                                                                                                              column=1,
                                                                                                              sticky="w")

        # Кнопка сохранить
        def save_and_close():
            self.settings = {
                "types": [k for k, v in self.release_types.items() if v.get()],
                "filters": [k for k, v in self.filter_keywords.items() if v.get()],
                "albums_to_export": self.album_export_var.get(),
                "tracks_to_export": self.track_export_var.get()
            }
            settings_win.destroy()
            if self.artist_id:
                self.fetch_albums()

        tk.Button(settings_win, text="OK", command=save_and_close, font=("Arial", 11, "bold"), fg="green").grid(
            row=10, column=0, columnspan=3, pady=10
        )

        tk.Button(settings_win, text="Cancel", command=settings_win.destroy, font=("Arial", 11, "bold"), fg="red").grid(
            row=11, column=0, columnspan=3, pady=(0, 20)
        )

    def _create_main_layout(self):
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

        # Main horizontal Paned Window (left = artist/discography, right = charts)
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
        self.albums_listbox.bind("<Delete>", self.delete_selected_album)
        main_paned.add(left_frame, minsize=200)

        # Right Paned Window for charts (split vertically, but you can adjust any of these)
        right_paned = tk.PanedWindow(main_paned, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        right_paned.pack(fill=tk.BOTH, expand=True)
        main_paned.add(right_paned, minsize=400)

        # Top sub-frame for the album chart
        album_frame = ttk.Frame(right_paned)
        album_frame.pack(fill=tk.BOTH, expand=True)
        album_pack_frame = ttk.Frame(album_frame)
        album_pack_frame.pack(fill=tk.BOTH, expand=True)

        # Create the album chart figure and axes
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
        # Create the track chart figure and axes
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

    def _get_expanded_keywords(self):
        filters = self.settings.get("filters", [])
        alias_map = {
            "reissue": ["reissue", "re-issue"],
            "remix": ["remix", "remixed"],
            "remastered": ["remastered", "remaster"]
        }
        result = []
        for keyword in filters:
            if keyword in alias_map:
                result.extend(alias_map[keyword])
            else:
                result.append(keyword)
        return result

    # ------------------------------
    # Spotify API Functions
    # ------------------------------
    def search_artist(self):
        # this function is called when the 'Search' button is clicked or the Enter key is pressed.
        # the app then asks Spotify for up to 5 matching artists and displays them in the matches listbox.
        # if you increase the number of matches, you'll need to scroll down the results, I didn't make any sliders for that.
        # Also, you're free to make typos or any mistakes in your inquiry. Normally, if artist name is correct, the first matching result is what you're looking for.

        query = self.search_entry.get().strip()
        if not query:
            messagebox.showinfo("Info", "Please enter an artist name.")
            return
        self.matches_listbox.delete(0, tk.END)
        try:
            results = self.sp.search(q=query, type='artist', limit=5) # feel free to increase/decrease this number if needed
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
        # this function is triggered when an artist is selected from the 'Artist Matches' listbox.
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
        # Reset filters to defaults on new artist selection
        self.settings = {
            "types": ["album", "single", "compilation"],  # appears_on отключён
            "filters": [],  # никаких ключевых фильтров
            "albums_to_export": "3",
            "tracks_to_export": "3"
        }
        self.current_album_tracks = []
        self.track_ax.clear()
        self.track_ax.set_title("Track Popularity")
        self.track_canvas.draw()
        self.fetch_albums()

    def fetch_albums(self):
        self.albums_listbox.delete(0, tk.END)
        self.albums.clear()
        offset = 0

        album_types = ",".join(self.settings.get("types", ["album"]))
        all_keywords = self._get_expanded_keywords()

        while True:
            try:
                results = self.sp.artist_albums(self.artist_id, album_type=album_types, limit=50, offset=offset)
            except Exception as e:
                messagebox.showerror("Error", f"Album retrieval failed: {e}")
                return

            items = results["items"]
            if not items:
                break

            for album in items:
                album_name = album.get("name", "")
                if any(kw in album_name.lower() for kw in all_keywords):
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

        for (alb_id, alb_name, alb_pop, alb_year) in self.albums:
            display_str = f"{alb_name} ({alb_year}) [pop: {alb_pop}]"
            self.albums_listbox.insert(tk.END, display_str)

        self.update_album_graph()

    def update_album_graph(self):
        self.album_ax.clear()
        if not self.albums:
            self.album_ax.set_title("No Albums Found")
            self.album_canvas.draw()
            return
        sorted_albums = sorted(self.albums, key=lambda x: x[2], reverse=True)
        names = [f"{a[1]} ({a[3]})" for a in sorted_albums]
        pops = [a[2] for a in sorted_albums]
        self.album_ax.barh(names, pops, color="skyblue")
        self.album_ax.invert_yaxis()  # Highest popularity at the top
        self.album_ax.set_title(f"{self.artist_name} - Albums")
        self.album_ax.set_xlabel("Popularity")
        self.album_canvas.draw()

    def on_select_album(self, event):
        # This function is triggered when an album is selected from the discography listbox.
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
        # List of keywords for filtering tracks
        filter_keywords = ["live", "remastered", "re-issue", "reissue", "demo"]
        for track in album_tracks:
            track_name = track.get("name", "")
            # Skip tracks whose name contains any of the filtered keywords
            # You can modify the keyword list or comment this section if you want to look through all albums
            if any(keyword in track_name.lower() for keyword in filter_keywords):
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

    def delete_selected_album(self, event):
        # this functions allows you to delete selected item in discography. it also updates graphs.
        selection = self.albums_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        # Remove the album from the internal list
        del self.albums[idx]
        # Update the listbox
        self.albums_listbox.delete(0, tk.END)
        for (alb_id, alb_name, alb_pop, alb_year) in self.albums:
            display_str = f"{alb_name} ({alb_year}) [pop: {alb_pop}]"
            self.albums_listbox.insert(tk.END, display_str)
        # Update the album graph
        self.update_album_graph()
        # Clear the track graph since
        self.current_album_tracks = []
        self.track_ax.clear()
        self.track_ax.set_title("Track Popularity")
        self.track_canvas.draw()

    def _update_track_graph(self, album_name, track_list):
        # Updates the track popularity bar chart using the track data for the selected album
        self.track_ax.clear()
        if not track_list:
            self.track_ax.set_title("No Tracks Found")
            self.track_canvas.draw()
            return
        sorted_tracks = sorted(track_list, key=lambda x: x["popularity"], reverse=True)
        track_names = [t["name"] for t in sorted_tracks]
        track_pops = [t["popularity"] for t in sorted_tracks]
        self.track_ax.barh(track_names, track_pops, color="orange")
        self.track_ax.invert_yaxis()  # Highest popularity at the top
        self.track_ax.set_xlabel("Popularity")
        self.track_ax.set_title(f"Tracks in '{album_name}'")
        self.track_canvas.draw()

    def show_raw_data(self):
        raw_win = tk.Toplevel(self)
        raw_win.title("Raw Data")
        raw_win.geometry("800x600")
        text_area = scrolledtext.ScrolledText(raw_win, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        def ms_to_minsec(ms):
            minutes = ms // 60000
            seconds = (ms % 60000) // 1000
            return f"{minutes}:{seconds:02d}"

        data = {
            "albums": "No album data available.",
            "tracks": "No track data available."
        }

        # Жанр исполнителя
        try:
            artist_info = self.sp.artist(self.artist_id)
            genres = artist_info.get("genres", [])
            genre_str = ", ".join(genres) if genres else "N/A"
        except:
            genre_str = "N/A"

        if self.albums:
            data["albums"] = [
                {
                    "id": a_id,
                    "name": a_name,
                    "popularity": pop,
                    "year": year,
                    "genre": genre_str
                }
                for (a_id, a_name, pop, year) in self.albums
            ]

        if self.current_album_tracks:
            enriched_tracks = []
            track_ids = [t["id"] for t in self.current_album_tracks]
            try:
                features_list = self.sp.audio_features(track_ids)
            except Exception:
                features_list = [None] * len(track_ids)

            for t, f in zip(self.current_album_tracks, features_list):
                enriched_tracks.append({
                    "id": t["id"],
                    "name": t["name"],
                    "popularity": t["popularity"],
                    "duration": ms_to_minsec(f["duration_ms"]) if f else "N/A",
                    "valence": f["valence"] if f else "N/A",
                    "tempo": f["tempo"] if f else "N/A"
                })
            data["tracks"] = enriched_tracks

        text_area.insert(tk.END, json.dumps(data, indent=2))

    def export_popularity(self):
        if not self.artist_id or not self.albums:
            messagebox.showinfo("Info", "Please search and select an artist first.")
            return

        count_option = self.settings.get("albums_to_export", "3")
        export_num = len(self.albums) if count_option == "All" else min(int(count_option), len(self.albums))

        sorted_albums = sorted(self.albums, key=lambda x: x[2], reverse=True)
        top_albums = sorted_albums[:export_num]

        lines = []
        dt = datetime.datetime.now().astimezone()
        lines.append(f"Popularity Export for Artist: {self.artist_name}")
        lines.append(f"Date/Time (Local): {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        lines.append("Source: Spotify API\n")

        all_keywords = self._get_expanded_keywords()

        try:
            artist_info = self.sp.artist(self.artist_id)
            genres = artist_info.get("genres", [])
            genre_str = ", ".join(genres) if genres else "N/A"
        except:
            genre_str = "N/A"

        for (alb_id, alb_name, alb_pop, alb_year) in top_albums:
            lines.append(f"Album: {alb_name} ({alb_year}), Popularity: {alb_pop}")
            lines.append(f"  Genre: {genre_str}")
            try:
                album_tracks = self.sp.album_tracks(alb_id, limit=50)['items']
            except Exception as e:
                lines.append(f"  Error fetching tracks: {e}\n")
                continue

            track_data = []
            for tr in album_tracks:
                tr_name = tr.get("name", "")
                if any(kw in tr_name.lower() for kw in all_keywords):
                    continue
                tr_id = tr["id"]
                try:
                    full_tr = self.sp.track(tr_id)
                    tr_pop = full_tr.get("popularity", 0)
                except Exception:
                    tr_pop = 0
                track_data.append((tr_name, tr_pop))

            track_data.sort(key=lambda x: x[1], reverse=True)  # от самых популярных треков

            track_limit = self.settings.get("tracks_to_export", "3")
            top_tracks = track_data if track_limit == "All" else track_data[:int(track_limit)]

            for (t_name, t_pop) in top_tracks:
                lines.append(f"   Track: {t_name}, Popularity: {t_pop}")
            lines.append("")

        output_text = "\n".join(lines)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Popularity Export"
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