# /app.py

from flask import Flask, render_template, send_from_directory, abort
import os

app = Flask(__name__)

# Configuration: Paths to the shared folders on each Windows server
SERVERS = {
    "Server1": r"\\server1\shared\folder",
    "Server2": r"\\server2\shared\folder",
    "Server3": r"\\server3\shared\folder",
    "Server4": r"\\server4\shared\folder",
    "Server5": r"\\server5\shared\folder",
    "Server6": r"\\server6\shared\folder",
}

@app.route("/")
def home():
    # Get a list of folders and ensure they exist
    folders = {server: path for server, path in SERVERS.items() if os.path.exists(path)}
    return render_template("home.html", folders=folders)

@app.route("/folder/<server_name>")
def view_folder(server_name):
    # Check if the server name exists
    if server_name not in SERVERS:
        abort(404, description="Server not found")

    folder_path = SERVERS[server_name]

    # List folder contents
    if not os.path.exists(folder_path):
        abort(404, description="Folder not found")

    contents = os.listdir(folder_path)
    return render_template("folder.html", server_name=server_name, contents=contents, folder_path=folder_path)

@app.route("/download/<server_name>/<filename>")
def download_file(server_name, filename):
    if server_name not in SERVERS:
        abort(404, description="Server not found")

    folder_path = SERVERS[server_name]
    if not os.path.exists(folder_path):
        abort(404, description="Folder not found")

    file_path = os.path.join(folder_path, filename)
    if not os.path.exists(file_path):
        abort(404, description="File not found")

    return send_from_directory(folder_path, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
