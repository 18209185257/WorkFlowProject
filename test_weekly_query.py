#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, r'C:\Users\82251\.openclaw\agents\main\agent\skills\work_chat')

import main

# 测试周查询功能
result = main.main({'text': '朱金涛本周工作总结'})
print("朱金涛本周工作总结:")
print("="*50)
print(result)
print("="*50)