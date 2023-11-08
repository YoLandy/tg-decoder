from utils.worker import Worker
from utils.setups import setup_tg
from utils.tg_requests import send_message
from flask import Flask, request
from threading import Thread, Semaphore

from config import START_MESSAGE, QUEUE_MESSAGE

app = Flask(__name__)
s = Semaphore()

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
    
        if 'text' in request.json["message"] and request.json["message"]['text'] == '/start':
            send_message(chat_id, START_MESSAGE)
            return {"ok": True}
        
        worker_num = apdate_workers(workers)
        if worker_num:
            print(worker_num)
            send_message(chat_id, QUEUE_MESSAGE(worker_num))
            
        if chat_id not in [work.chat_id for work in workers]:
            worker = Worker(request.json, s)
            workers.append(worker)
            thread = Thread(target=worker.render)
            thread.start()

    return {"ok": True}

if __name__ == '__main__':
    setup_tg()
    app.run(debug=False)