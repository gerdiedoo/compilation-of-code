import ast
import javalang

import pandas
from random import randint
import os

# For generating random identifiers
import exrex, re

from random import randint
import string

from DatasetUtils import py_cleaner, c_cleaner, add_to_list

py_keywords = {}
java_keywords = {}

with open('pythonkeywords.txt', 'r') as f:
    py_keywords = set(f.read().split())
    
with open('javakeywords.txt', 'r') as f:
    java_keywords = set(f.read().split())

class RewriteClass(ast.NodeTransformer):
    def __init__(self, thesaurus):
        super().__init__()
        self.thesaurus = thesaurus
    
    def visit_ClassDef(self, node):
        if node.name in self.thesaurus.keys():
            node.name = self.thesaurus[node.arg]
            return node
        else:
            return node
        
class RewriteArguments(ast.NodeTransformer):
    def __init__(self, thesaurus):
        super().__init__()
        self.thesaurus = thesaurus
        
    def visit_arg(self, node):
        #arg(arg, annotation, type_comment)¶
        if node.arg in self.thesaurus.keys():
            node.arg = self.thesaurus[node.arg]
            return node
        else:
            return node
    
class RewriteFunctions(ast.NodeTransformer):
    def __init__(self, thesaurus):
        super().__init__()
        self.thesaurus = thesaurus
        self.reargue = RewriteArguments(self.thesaurus)
    
    def visit_FunctionDef(self, node):
        if node.name in self.thesaurus.keys():
            node.name = self.thesaurus[node.name]
            self.reargue.visit(node)
            return node
        else:
            return node
    
class RewriteName(ast.NodeTransformer):
    def __init__(self, thesaurus):
        super().__init__()
        self.thesaurus = thesaurus
        
    def visit_Name(self, node):
        if node.id in self.thesaurus.keys():
            return ast.Name(id=self.thesaurus[node.id], ctx=node.ctx)
        else:
            return node

def generate_keywords(identifiers, length_min=1, length_max=2):
    ids_lengths = len(identifiers)
    reg_ex = '[a-zA-Z][a-zA-Z0-9_]*'
    generated = set()
    
    while len(generated) < ids_lengths:
        random_string = ''.join(exrex.getone(reg_ex, limit=randint(length_min, length_max)))
        
        if len(random_string) > length_max:
            random_string = random_string[0:length_max]
        
        if random_string not in py_keywords:
            generated.add(random_string)
    return dict(zip(identifiers, generated))

def flatten(t):
    return [item for sublist in t for item in sublist]

def get_file_lines(file):
    try:
        with open(file, 'r') as f:
            return len(f.readlines())
    except:
        return 1_000_000

def find_all_files(folders, ext, thresh):
    label_folders = [
        'Hash-Map', 'Linked-List', 'Search-Binary', 'Search-Linear',
        'Sort-Bubble', 'Sort-Insertion', 'Sort-Merge', 'Sort-Quick',
        'Sort-Selection', 'Sort-zOthers'
    ]
    
    #exp = re.compile(f'$*.{ext}')
    
    files = []
    
    for folder in folders:
        for label_folder in label_folders:
            # We've gotten the files that has the corresponding extension.
            files_in_dir = list(filter(lambda y: f'.{ext}' in y, os.listdir(f'{folder}/{label_folder}')))
            # Then, let's check if the file has less than thresh lines
            for file in files_in_dir:
                with open(f'{folder}/{label_folder}/{file}', 'r') as f:
                    try:
                        if ext == 'py':
                            __file = py_cleaner(f.read())
                        else:
                            __file = c_cleaner(f.read())
                            
                        splitted = __file.splitlines()
                        if len(splitted) <= thresh:
                            files.append(f'{folder}/{label_folder}/{file}')
                    except:
                        pass
                    
            
                                
            
                                  
                                  
#             x = map(lambda p: f'{folder}/{label_folder}/{p}',
#                     (filter(lambda y: f'.{ext}' in y and 
#                             thresh <= get_file_lines(f'{folder}/{label_folder}/{y}'), 
#                             os.listdir(f'{folder}/{label_folder}'))))
#             files.append(list(x))
                
    return files
            
def generate_new_code(source, ext):
    identifiers = set()
    
    if ext == 'py':
        root = ast.parse(source)
        names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
        # The unique identifiers in this file minus
        # the Python keywords.
        identifiers = set(names).difference(py_keywords)
        thesaurus = generate_keywords(identifiers, length_max=2)

        # Replace all identifiers
        renamer = RewriteName(thesaurus)
        refunction = RewriteFunctions(thesaurus)
        reclass = RewriteClass(thesaurus)
        
        root = renamer.visit(root)
        root = refunction.visit(root)
        root = reclass.visit(root)
        
        
        return ast.unparse(root)
    elif ext == 'java':
        
        
        
        tokens = list(javalang.tokenizer.tokenize(source))

        types = set([type(token) for token in tokens])
        
        identifiers = set([token.value for token in tokens if isinstance(token, javalang.tokenizer.Identifier)])
        identifiers = identifiers.difference(java_keywords)
        
        
        thesaurus = generate_keywords(identifiers, length_max=2)
        
        def replace(match):
            return thesaurus[match.group(0)]
        
        return re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in thesaurus), replace, source)
        
    else:
        raise Exception(f'Error! Not available for language "{ext}".')
        
def intercalate_files(df, ext, *files):
    
    dest = 'intercalate_augment'
    
    cols = ['quicksort', 'mergesort', 'selectionsort', 'insertionsort', 
        'bubblesort', 'linearsearch', 'binarysearch', 'linkedlist', 'hashmap']
    files = list(files)
    contents = []
    
    fnames = [file.split('.')[0] for file in files]
    fnames = [file.split('/')[1] for file in fnames]
    
    new_rows = []
    
    for file in files:
        with open(file, 'r') as f:
            try:
                if ext == 'py':
                    contents.append(py_cleaner(f.read()))
                else:
                    contents.append(c_cleaner(f.read())) 
            except:
                pass
    contents_1 = '\n'.join(contents)
    df_files = [file.split('/')[1] for file in files]
    
    loc = df.loc[df['Filename'].isin(df_files)][cols].values.tolist()
    
    log_or = lambda x, y: int(x or y)
    
    # Compute the logical or of the labels
    row = [log_or(x, y) for x, y in zip(*loc)]

    # If there are more than 150 lines, discard.
    if len(contents_1.splitlines()) <= 150:
        forward_fname = f"{'_'.join(fnames)}.{ext}"

        reverse = randint(0, 10) >= 5
        
        row_1 = [forward_fname, *row]
        
        new_rows.append(row_1)
        
        # Save
        with open(f'{dest}/{forward_fname}', 'w') as f:
            f.write(contents_1)
        
        if reverse:
            contents.reverse()
            contents_2 = '\n'.join(contents)
            backward_fname = f"{'_'.join(fnames)}_reverse.{ext}"
            row_2 = [backward_fname, *row]
            new_rows.append(row_2)
            
            with open(f'{dest}/{backward_fname}', 'w') as f:
                f.write(contents_2)
    
    return new_rows