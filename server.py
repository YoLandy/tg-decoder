from utils.worker import Worker
from utils.setups import setup_tg
from flask import Flask, request
import threading

from config import UNSUPPORTED_TYPE_MESSAGE, DOWNLOAD_FILE_MESSAGE

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        worker = Worker(request.json)
        thread = threading.Thread(target=worker.render)
        thread.start()

    return {"ok": True}
    

if __name__ == '__main__':
    setup_tg()
    app.run(debug=True)