from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 敏感词过滤
class DFAFilter():
    # https://github.com/observerss/textfilter
    '''Filter Messages from keywords

    Use DFA to keep algorithm perform constantly

    >>> f = DFAFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path) as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        # message = message.decode('utf-8')
        message = message.lower()
        ret = []
        start = 0
        is_filter = False
        words = []
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            tempchar = ""
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    tempchar += char
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:

                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        is_filter = True
                        words.append(tempchar)
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1
        # print('words',words)
        return ''.join(ret), is_filter, words


class post_data(BaseModel):
    data: str | None = None


@app.post("/filter/")
def filter(data: post_data):
    replaced, is_replaced, replaced_words = gfw.filter(i, "*")
    return {
        'source': data,
        'replaced': replaced,
        'is_replaced': is_replaced,
        'replaced_words': replaced_words,
    }


@app.post("/correct/")
def correct(data: post_data):
    return nlp(data.data)


@app.get("/filter/")
def get_get(data: str):
    replaced, is_replaced, replaced_words = gfw.filter(data, "*")
    return {
        'source': data,
        'replaced': replaced,
        'is_replaced': is_replaced,
        'replaced_words': replaced_words,
    }


@app.get("/correct/")
def correct_get(data: str):
    return nlp(data)


if __name__ == "__main__":
    import uvicorn
    from pycorrector.macbert.macbert_corrector import MacBertCorrector
    # https://github.com/shibing624/pycorrector
    gfw = DFAFilter()
    gfw.parse("/home/spider/filter_word.txt")  # 添加词库
    
    # 错词纠错
    nlp = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct
    uvicorn.run(app, host="127.0.0.1", port=8888)
