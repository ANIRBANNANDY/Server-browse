from flask import Flask, render_template, abort
import os

app = Flask(__name__)

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
    # Display the root-level folders
    folders = {server: path for server, path in SERVERS.items() if os.path.exists(path)}
    return render_template("home.html", folders=folders)


@app.route("/folder/<server_name>")
@app.route("/folder/<server_name>/<path:subpath>")
def view_folder(server_name, subpath=""):
    # Validate server name
    if server_name not in SERVERS:
        return f"Server '{server_name}' not found.", 404

    base_path = SERVERS[server_name]
    folder_path = os.path.join(base_path, subpath)

    # Check if the resolved path exists
    if not os.path.exists(folder_path):
        return f"Path '{folder_path}' does not exist or cannot be accessed.", 404

    # List contents
    try:
        contents = os.listdir(folder_path)
    except Exception as e:
        return f"Error accessing folder '{folder_path}': {e}", 500

    # Distinguish files and folders
    items = [
        {
            "name": item,
            "is_folder": os.path.isdir(os.path.join(folder_path, item)),
        }
        for item in contents
    ]

    return render_template(
        "folder.html", server_name=server_name, folder_path=folder_path, items=items
    )


if __name__ == "__main__":
    app.run(debug=True)
