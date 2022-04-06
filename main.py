from flask import Flask, render_template, send_from_directory
from urllib.parse import quote as urlencode
from pathlib import PurePosixPath as VPath
import os

PATH_MAP = {
	"vid": "videos",
	"img": "images",
	"": "folder"
}

app = Flask(__name__)

@app.route('/', defaults={'url': ''})
@app.route('/<path:url>')
def routeHandler(url):
	virtualBase = ""
	virtualName = ""
	virtualPath = ""

	physicalBase = ""
	physicalName = ""
	physicalPath = ""

	for virtualBase_ in PATH_MAP:
		if url.startswith(virtualBase_):
			virtualBase = virtualBase_
			virtualName = url.removeprefix(virtualBase).removeprefix('/')
			virtualPath = url

			physicalBase = PATH_MAP[virtualBase]
			physicalName = virtualName
			physicalPath = os.path.join(physicalBase, physicalName)
			break;

	if physicalBase == "":
		return "No mapping"

	if os.path.isdir(physicalPath):
		try:
			fileNames = os.listdir(physicalPath)

			files = []
			for fileName in fileNames:
				fileVirtualPath = "/" + str(VPath(virtualPath) / fileName)

				file = {
					'name': fileName,
					'icon': "/static/icons/file.gif",
					'virtualPathUrl': urlencode(fileVirtualPath)
				}

				if os.path.isdir(os.path.join(physicalPath, fileName)):
					file["icon"] = "/static/icons/folder.gif"

				files.append(file)

			return render_template("folder.html", files=files, phyPath=physicalPath, virPath=virtualPath);
		except PermissionError:
			return render_template("403.html", virPath=virtualPath), 403;

	elif os.path.isfile(physicalPath):
		return send_from_directory(physicalBase, physicalName)
	else:
		return render_template("404.html", virPath=virtualPath), 404;

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)