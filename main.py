import os
import clang
import clang.cindex as cl
from clang.cindex import CursorKind

current_folder = os.path.dirname(__file__)
cl.Config.set_library_file(os.path.join(current_folder, 'libclang.dll'))

def fully_qualified(c):
    if c is None:
        return ''
    elif c.kind == CursorKind.TRANSLATION_UNIT:
        return ''
    else:
        return_type = c.result_type.spelling
        parameters = [param.type.spelling for param in c.get_arguments()]
        return [return_type, c.spelling, parameters]

def get_methods(file):
    methods = []
    path = os.path.join(current_folder, file)
    idx = clang.cindex.Index.create()
    tu = idx.parse(path, args='-xc++ --std=c++11'.split())
    for c in tu.cursor.walk_preorder():
        if c.kind == CursorKind.CXX_METHOD:
            methods.append(fully_qualified(c.referenced))
    return methods

def convert_method_to_string(method):
    return f'{method[0]} {method[1]}({", ".join(method[2])})'

def compare_methods(mysolution_methods, testclass_methods):
    methods = []
    missing_methods = []
    for method in mysolution_methods:
        if method not in testclass_methods:
            missing_methods.append(method)
        elif method in testclass_methods:
            methods.append(method)
    return [methods, missing_methods]

mysolution_methods = get_methods('MySolution.h')
testclass_methods = get_methods('TestClass.h')

methods = compare_methods(mysolution_methods, testclass_methods)
matching_methods = methods[0]
missing_methods = methods[1]
print('\nMatching methods:')
for method in matching_methods:
    print(convert_method_to_string(method))
    
print('\nMissing methods:')
for method in missing_methods:
    print(convert_method_to_string(method))