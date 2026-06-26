#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, r'C:\Users\82251\.openclaw\agents\main\agent\skills\work_chat')

import main

# 测试chat_query技能
result = main.main({'text': '朱金涛今日工作总结'})
print("chat_query技能返回结果:")
print(result)