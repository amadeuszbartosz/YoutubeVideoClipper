#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3

import os
import re
import pickle
from youtube_transcript_api import YouTubeTranscriptApi
import tkinter as tk
from tkinter import messagebox, filedialog, StringVar
from pytube import YouTube
from moviepy.editor import VideoFileClip

def save_to_txt(transcript, title, save_path):
    safe_title = "".join(c if c.isalnum() else "_" for c in title)
    filename = os.path.join(save_path, f"{safe_title}_transcript.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Transcript for Video: {title}\n\n")
        for entry in transcript:
            f.write(f"{entry['start']} - {entry['start'] + entry['duration']}: {entry['text']}\n")

SAVE_PATH_FILE = "save_path.pkl"

def save_save_path(path):
    with open(SAVE_PATH_FILE, 'wb') as f:
        pickle.dump(path, f)

def load_save_path():
    if os.path.exists(SAVE_PATH_FILE):
        with open(SAVE_PATH_FILE, 'rb') as f:
            return pickle.load(f)
    return None

def select_directory():
    """Open a directory selection dialog and update the save_path_var with the chosen directory."""
    chosen_directory = filedialog.askdirectory(title="Choose save location")
    if chosen_directory:
        save_path_var.set(chosen_directory)
        save_save_path(chosen_directory)

def time_to_seconds(timestr):
    """Convert MM:SS to seconds."""
    minutes, seconds = map(int, timestr.split(':'))
    return minutes * 60 + seconds

def sanitize_filename(filename):
    """Sanitize the filename by removing or replacing invalid characters."""
    s = re.sub(r'[\\/:*?"<>|]', '_', filename)  # Replace invalid characters with underscores
    s = re.sub(r'__+', '_', s)  # Replace multiple underscores with a single underscore
    s = s.replace('//', '_')   # Replace double slashes with a single underscore
    return s

def trim_video(input_path, start_time, end_time, output_path, video_title):
    with VideoFileClip(input_path) as video:
        new = video.subclip(start_time, end_time)

        # Sanitize the video_title here
        sanitized_title = sanitize_filename(video_title)
        print("Sanitized Title:", sanitized_title)  # Debug line

        base_name = sanitized_title.replace(" ", "_")
        counter = 1
        final_output_path = os.path.join(output_path, f"{base_name}.mp4")
        print("Final Output Path:", final_output_path)  # Debug line
        while os.path.exists(final_output_path):
            final_output_path = os.path.join(output_path, f"{base_name}_{counter}.mp4")
            counter += 1


        new.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

def download_video(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    downloaded_path = stream.download(output_path)
    return os.path.join(output_path, stream.default_filename), yt.title

def select_directory():
    """Open a directory selection dialog and update the save_path_var with the chosen directory."""
    chosen_directory = filedialog.askdirectory(title="Choose save location")
    if chosen_directory:
        save_path_var.set(chosen_directory)

def download_and_trim():
    url = url_entry.get()
    start_time = time_to_seconds(start_time_entry.get())
    end_time = time_to_seconds(end_time_entry.get())
    save_path = save_path_var.get()

    # Check if video duration is over 90 seconds
    if end_time - start_time > 90:
        messagebox.showerror("Error", "You can only clip videos up to 90 seconds in length.")
        return

    if not save_path:
        messagebox.showerror("Error", "Please choose a save path.")
        return

    try:
        temp_path, video_title = download_video(url, '.')
        trim_video(temp_path, start_time, end_time, save_path, video_title)
        os.remove(temp_path)

        # Transcription
        if transcribe_var.get():
            video_id = url.split('v=')[-1]  # Extract video ID from URL
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                save_to_txt(transcript, video_title, save_path)
            except Exception as te:
                messagebox.showwarning("Transcription Warning", f"Could not transcribe the video due to: {str(te)}")

        messagebox.showinfo("Success", "Video clipped and saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, color, text="", command=None):
        tk.Canvas.__init__(self, parent, width=width, height=height, borderwidth=0, relief="flat", highlightthickness=0, bg="#181818")

        self.command = command
        self.corner_radius = corner_radius

        if color == "red":
            self.color = "#FF0000"
        else:
            self.color = color

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

        self.create_oval((5, 5, corner_radius + 5, corner_radius + 5), outline=self.color, fill=self.color)
        self.create_oval((5, height - corner_radius - 5, corner_radius + 5, height - 5), outline=self.color,
                         fill=self.color)
        self.create_oval((width - corner_radius - 5, height - corner_radius - 5, width - 5, height - 5),
                         outline=self.color, fill=self.color)
        self.create_oval((width - corner_radius - 5, 5, width - 5, corner_radius + 5), outline=self.color,
                         fill=self.color)
        self.create_rectangle(5, corner_radius, width - 5, height - corner_radius, outline=self.color, fill=self.color)
        self.create_rectangle(corner_radius, 5, width - corner_radius, height - 5, outline=self.color, fill=self.color)

        self.create_text(width // 2, height // 2, text=text, fill=FG_COLOR)  # Text color set to white for visibility

    def _on_press(self, event):
        self.configure(bg="#D50000")

    def _on_release(self, event):
        self.configure(bg="#FF0000")
        if self.command:
            self.command()

# Create the main window
root = tk.Tk()
root.title("YouTube Video Clipper")

# Set colors for the GUI elements
BG_COLOR = '#181818'  # Dark Gray
FG_COLOR = '#FFFFFF'  # White
BUTTON_BG_COLOR = '#FF0000'  # YouTube Red
BUTTON_FG_COLOR = '#181818'  # Dark Gray for button text

# Apply colors
root.configure(bg=BG_COLOR)

# Add a checkbox for transcription
transcribe_var = tk.IntVar()
transcribe_checkbox = tk.Checkbutton(root, text="Transcribe full video", variable=transcribe_var, bg=BG_COLOR, fg=FG_COLOR)
transcribe_checkbox.grid(row=4, columnspan=3, pady=10)

# Add label, entry, and button for directory selection
tk.Label(root, text="Save Path", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, padx=10, pady=10)
save_path_var = StringVar()
saved_path = load_save_path()  # Load the saved path here
if saved_path:
    save_path_var.set(saved_path)  # Set the saved path here

save_path_entry = tk.Entry(root, width=40, textvariable=save_path_var, bg='#505050', fg=FG_COLOR, insertbackground=FG_COLOR, highlightbackground="#282828", highlightcolor="#282828")
save_path_entry.grid(row=3, column=1, padx=10, pady=10)
path_button = RoundedButton(root, width=120, height=30, corner_radius=10, color="red", text="Choose Path", command=select_directory)
path_button.grid(row=3, column=2, padx=10, pady=10)

# Add labels and input fields for YouTube URL, start time, and end time
tk.Label(root, text="YouTube URL", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=40, bg='#505050', fg=FG_COLOR, insertbackground=FG_COLOR, highlightbackground="#282828", highlightcolor="#282828")
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Start time (MM:SS)", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=10, pady=10)
start_time_entry = tk.Entry(root, width=10, bg='#505050', fg=FG_COLOR, insertbackground=FG_COLOR, highlightbackground="#282828", highlightcolor="#282828")
start_time_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="End time (MM:SS)", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, padx=10, pady=10)
end_time_entry = tk.Entry(root, width=10, bg='#505050', fg=FG_COLOR, insertbackground=FG_COLOR, highlightbackground="#282828", highlightcolor="#282828")
end_time_entry.grid(row=2, column=1, padx=10, pady=10)

# Create the "Download and Trim" button (adjust size)
download_button = RoundedButton(root, width=160, height=40, corner_radius=15, color="red", text="Download and Trim", command=download_and_trim)
download_button.grid(row=5, columnspan=3, pady=20)

# Run the main loop
root.mainloop()
