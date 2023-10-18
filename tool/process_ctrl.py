import multiprocessing
import os
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
processes = {}


class Data(BaseModel):
    name: Union[str, None]
    key: str
    command: str


def get_pid(process):
    cmd = "ps aux| grep '%s'|grep -v grep " % process
    out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    infos = out.stdout.read().splitlines()
    return [i.split() for i in infos]


# @app.post("/run/")
# def run(data: Data):
#     # p = subprocess.run(command, stdin=None, input=None, stdout=None, stderr=None, shell=True, timeout=None, check=False, universal_newlines=False)
#     if data.name not in processes.keys():
#         # p = subprocess.call(command, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         # data.command = 'nohup /opt/miniconda3/envs/spider/bin/python /home/process_controler/a.py &'
#         print(data.command)
#         process = multiprocessing.Process(target=run_conmand, args=(data.command,))
#         process.start()
#         print('---------------', process)
#         # p = subprocess.Popen(command, shell=False)
#         processes[data.name] = process
#         return str(process)
#     else:
#         return {'status': 401, 'detail': '进程名称重复'}


# def run_conmand(command):
#     # p = subprocess.call(command, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     p = os.popen(command)
#     # p = subprocess.run(command, stdin=None, input=None, stdout=None, stderr=None, shell=False, timeout=None, check=False, universal_newlines=False)
#     return p


@app.post("/run/")
def run(data: Data):
    # p = subprocess.run(command, stdin=None, input=None, stdout=None, stderr=None, shell=True, timeout=None, check=False, universal_newlines=False)
    if len(get_pid(data.key)) > 0:
        return {'status': 401, 'detail': '进程key重复'}
    if data.key not in processes.keys():

        # p = subprocess.call(command, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # data.command = 'nohup /opt/miniconda3/envs/spider/bin/python /home/process_controler/a.py &'
        process = os.system(data.command)
        pids = get_pid(data.key)
        if len(pids) == 1:
            processes[data.name] = pids[0][1]
            return {'status': 200, 'detail': '多个进程', 'data': pids[0]}
        return {'status': 401, 'detail': '多个进程或创建失败', 'data': pids}


@app.get("/tasks/")
def tasks():
    print(processes)
    return str(processes)


@app.get("/kill/")
def kill(key: str):
    pids = get_pid(key)
    if len(pids) > 1:
        return {'status': 401, 'detail': '进程key重复', 'data': pids}
    elif len(pids) == 1:
        print('执行', f"kill {pids[0][1].decode()}")
        r = os.system(f"kill {pids[0][1].decode()}")
        return {'status': 200, 'detail': '已关闭', 'data': pids, 'output': r}
    else:
        return {'status': 401, 'detail': '进程key未找到'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
