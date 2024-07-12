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


print(func_tree)


#%%


sys.exit()

#%%

def print_tree(tree, indent=0):
    for key, value in tree.items():
        print("  " * indent + key)
        print_tree(value, indent + 1)













def plot_tree(tree, root_function):
    fig, ax = plt.subplots(figsize=(8, 12))  # Make the figure taller and narrower
    ax.axis('off')

    def draw_tree(tree, x=0.5, y=1, depth=1):
        if not tree:
            return x, y
        
        node = list(tree.keys())[0]
        ax.text(x, y, node, ha='center', va='center', bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="skyblue"))

        children = list(tree[node].keys())
        if not children:
            return x, y
        
        new_y = y - 1 / depth
        new_x = x - (len(children) - 1) / (2 * depth)
        for i, child in enumerate(children):
            ax.plot([x, new_x + i / depth], [y, new_y], 'k-', lw=1)
            draw_tree({child: tree[node][child]}, new_x + i / depth, new_y, depth * 2)
        
        return x, y

    draw_tree(tree, x=0.5, y=1, depth=1)
    plt.title('Function Call Tree')
    plt.show()

# Usage example:
directory_path = Path("/home/matthew/university_work/03_automatic_detection_algorithm/06_LiCSAlert/00_LiCSAlert_GitHub/licsalert")
root_function_name = "LiCSAlert_monitoring_mode"

function_tree = build_function_call_tree(directory_path, root_function_name)
print_tree(function_tree)
plot_tree(function_tree, root_function_name)
