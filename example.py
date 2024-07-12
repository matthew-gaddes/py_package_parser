#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 11:58:27 2024

@author: matthew
"""

directory = "/home/matthew/university_work/03_automatic_detection_algorithm/06_LiCSAlert/00_LiCSAlert_GitHub"
root_function = "LiCSAlert_monitoring_mode"

func_tree = build_function_call_tree(directory, root_function)


func_tree
