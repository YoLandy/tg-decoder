from utils.worker import Worker
from utils.setups import setup_tg
from utils.tg_requests import send_message
from flask import Flask, request
import threading

from config import UNSUPPORTED_TYPE_MESSAGE, DOWNLOAD_FILE_MESSAGE

app = Flask(__name__)

def apdate_workers(workers):
    for i, worker in enumerate(workers):
        if not worker.is_running:
            workers.pop(i)
    return len(workers)

workers = []

@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        chat_id = request.json["message"]["chat"]["id"]
        worker_num = apdate_workers(workers)
        if worker_num:
            print(worker_num)
            send_message(chat_id, f'Перед вами в очереди {worker_num} человек')
            
        if chat_id not in [work.chat_id for work in workers]:
            worker = Worker(request.json)
            workers.append(worker)
            thread = threading.Thread(target=worker.render)
            thread.start()

    return {"ok": True}

if __name__ == '__main__':
    setup_tg()
    app.run(debug=True)