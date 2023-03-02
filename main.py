# -*- coding: utf-8 -*-

import clipboard

import random, string
import shelve

from wox import Wox

from datetime import datetime
from collections import deque

LOCAL_STORAGE = "data/local.pickle"

class PasswordGenerator(Wox):

    def query(self, query):
        results = []

        # blank keyword
        if not query:
            results.append({
                "Title": "请输入密码长度",
                "SubTitle": "随机生成指定长度的复杂密码",
                "IcoPath":"Images/app.png",
            })
            with shelve.open(LOCAL_STORAGE, writeback=True) as db:
                if "copy_history" in db:
                    for r in db["copy_history"]:
                        results.append({
                            "Title": r[0],
                            "SubTitle": "Created At {}".format(r[1]),
                            "IcoPath":"Images/app.png",
                            "JsonRPCAction": {
                                'method': 'copy',
                                'parameters': [r[0], False],
                                'dontHideAfterAction': False
                            }
                        })

            return results
        
        #define data
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = "#$%&*+=?@^"

        all = lower + upper + num + symbols

        for i in range(6):
            password = "".join(random.sample(all, int(query)))
            results.append({
                "Title": "".join(password),
                # "SubTitle": "".join(""),
                "IcoPath":"Images/app.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'copy',
                    'parameters': [password, True],
                    'dontHideAfterAction': False
                }
            })

        return results

    def copy(self, text, log):
        clipboard.copy(text)
        if log:
            copyAt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            with shelve.open(LOCAL_STORAGE, writeback=True) as db:
                if "copy_history" not in db:
                    db["copy_history"] = deque(maxlen=6)
                db["copy_history"].appendleft((text, copyAt))
            

if __name__ == "__main__":
    PasswordGenerator()
