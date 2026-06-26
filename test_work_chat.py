#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, r'C:\Users\82251\.openclaw\agents\main\agent\skills\work_chat')

import main

# 测试work_chat技能
result = main.main({'text': '朱金涛今日工作总结'})
print("work_chat技能测试结果:")
print("="*50)
print(result)
print("="*50)