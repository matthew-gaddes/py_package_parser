#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:58:27 2024

@author: matthew
"""

import sys

#%%

import ppp
from ppp.parsing import build_function_call_tree


#%%

directory = "/home/matthew/university_work/03_automatic_detection_algorithm/06_LiCSAlert/00_LiCSAlert_GitHub"
root_function = "LiCSAlert_monitoring_mode"

func_tree = build_function_call_tree(directory, root_function)

# to a file
with open("ppp_output.txt", 'w') as f:
    print(func_tree, file = f)

# to a terminal
print(func_tree)


#%%
