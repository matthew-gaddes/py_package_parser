#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:37:28 2024

@author: matthew
"""

import os

import pdb

#from pathlib import Path


#%%

def read_py_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines



#%% 
class py_function:
    
    def __init__(self, name, file, line_start):
        self.name = name
        self.file = file
        self.line_start = line_start
        
    def find_line_end(self):
        """ Find the line that the function ends on.  
        """
        
        lines = read_py_file_lines(self.file)
        
        end_found = False
        line_n = self.line_start + 1
        while (not end_found):
            line = lines[line_n]
            # function ends either when the next function starts
            if line[:3] == "def":
                self.line_end = (line_n -1) 
                end_found = True
            
            # or the file ends, for the last function.  
            if line_n == (len(lines) -1):
                self.line_end = (line_n -1) 
                end_found = True
            line_n += 1
            
                
#%%


class TreeNode:
    """ To store a heirarchical set of py_function to describe 
    all the function calls within a Python package.  """
    
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self, level=0, final_child = False, indent_parent = ''):
        """ Returns a py_function.name attribute to be readable.  
        """
        
        #u2502 is vertical, 
        # u2014 is horizontal
        # u2514 is end of vertical with horizontal tick
        # u251c is vertical with tick in middle
       
        
        if level == 0:
            # initiliase
            name_start = ''
        else:
            #indent = indent_parent + "\u2502   "  
            if not final_child:
                # vertical line with horizontal going to function
                name_start = indent_parent + "\u251C" + ("\u2014" *3)
            else:
                # end of vertical line with horizontal going to function
                name_start = indent_parent + "\u2514" + ("\u2014" *3)
                
        # add the function to the start of the name
        ret = name_start + self.value.name + "\n"
                
        # if there are no children, this is skipped
        n_children = len(self.children)
        for child_n, child in enumerate(self.children):
            # determien if this is the final child of these children
            if child_n == (len(self.children) - 1):
                final_child = True
            else:
                final_child = False
            # first level doesn't have a line, all others need line updating.  
            if level >= 1:
                # 251c is vertical with tick in middle
                if name_start[-4] == "\u251c":
                    new_indent = indent_parent + "\u2502   "
                # 2514 is end of vertical with tick in middle
                elif name_start[-4] == "\u2514":
                    new_indent = indent_parent + "    "
            else:
                new_indent = indent_parent + "    "
            # call on child, recursively.  
            ret += child.__repr__(level + 1, final_child, new_indent)
            
            
                
        return ret  
    
    def find_function_n(function_name, py_functions):
        """
        """
        for func_n, py_f in enumerate(py_functions):
            if py_f.name == function_name:
                return func_n
        raise Exception(f"Failed to find {function_name} in py_functions")
        
        
#%% 


def find_all_functions(directory, verbose = True):
    """ Find all the functions in a python directory (including child 
    directories)
    """
    
    from pathlib import Path

    # Find all the functions in a directory of python files.  
    py_functions = []
    # recursively look at all directories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                print(f"Opening {file}")
                file_path = Path(root) / file
                lines = read_py_file_lines(file_path)

                for line_n, line in enumerate(lines):
                    # if this line is the start of a function
                    if line[:3] == "def":
                        # get the name (between def and first ( )
                        function_name = line.split('(')[0][4:]
                        # add to list of functions
                        py_functions.append(py_function(function_name, file_path,
                                                            line_n))
                # debug
                # for py_f in py_functions:
                #     print(py_f.name)
    
    # get the line end numbers for the functions
    for py_f in py_functions:
        py_f.find_line_end()
        
    # single list of all the function names
    py_function_names = [py_f.name for py_f in py_functions]
    
    if verbose:
        for py_f in py_functions:
            print(f"{py_f.name} : {py_f.line_start} - {py_f.line_end} ")
        
    return py_functions, py_function_names

#%%

def find_function_calls(script, line_start, line_end,
                        functions_of_interest):
    """ Find the functions called by a function
    """
    import ast
    
    with open(script, "r") as file:
        tree = ast.parse(file.read(), filename=script)


    # 1: get all the functions used in that block of code (line_start - line_end)    
    all_function_calls = []
    class FunctionCallVisitor(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if line_start <= node.lineno <= line_end:
                    all_function_calls.append(node.func.id)
            self.generic_visit(node)
    
    FunctionCallVisitor().visit(tree)
    
    # 2: reject any that aren't the ones we're interested in
    # i.e. usually things that aren't in our module/package
    
    function_calls = []
    for function_call in all_function_calls:
        if function_call in functions_of_interest:
            function_calls.append(function_call)
    return function_calls

#%%

def find_function_n(function_name, py_functions):
        """
        """
        for func_n, py_f in enumerate(py_functions):
            if py_f.name == function_name:
                return func_n
        raise Exception(f"Failed to find {function_name} in py_functions")


#%%


def add_functions_to_tree(func_tree_node, py_functions, py_function_names):
    """
    """

    # find all functions used by the function.  
    func_calls = find_function_calls(func_tree_node.value.file,
                                     func_tree_node.value.line_start, 
                                     func_tree_node.value.line_end, 
                                     py_function_names)
    
    # if there are no functions of interest in this function, nothing more:
    if len(func_calls) == 0:
        return 

    # else add those functions as children to this node.  
    else:
        print(f"In {func_tree_node.value.name} the following functions were found: ")
        for func_call in func_calls:
            print(f"    {func_call}")
        
        # convert the strings back to py_functions, and add as children to node.          
        for child_n, func_call in enumerate(func_calls):
            index_n = find_function_n(func_call, py_functions)    
            py_func = py_functions[index_n]
            func_tree_node.add_child(TreeNode(py_func))
            
            # Recursive look for child functions of this function.  
            print(f"Looking for functions that are called in {py_func.name}")
            add_functions_to_tree(func_tree_node.children[child_n], py_functions,
                                  py_function_names)

        return func_tree_node


#%% 

def build_function_call_tree(directory, root_function):
    """ Build a heirarchical tree of all the functions in a python
    package.  
    
    """

    # find all the functions in the directory (names, files, line numbers)
    py_functions, py_function_names = find_all_functions(directory, verbose = True)
          
    # Get the root function (i.e. the one called)
    func_n = find_function_n(root_function, py_functions)    
    root_function = py_functions[func_n]

    # start the heirarchical tree
    func_tree_node = TreeNode(root_function)

    # populate the heirarchical tree recursively.  
    func_tree = add_functions_to_tree(func_tree_node, py_functions, py_function_names)
        
    return func_tree



