#!/usr/bin/python

# Insert metadata into a json ipynb file and if the cell contains
# an h1 title, make it into a new slide.

import sys,os
import json

argp = 1
do_run_nb_convert = True
do_serve = True

while argp < len(sys.argv) and sys.argv[argp][0] == '-':
  S_ = sys.argv[argp]
  argp+=1 
  if S_=='--no-view':
    do_run_nb_convert = False
    continue

  print 'Unknown option ' + S_
  exit(-1)


filename = sys.argv[argp] if argp < len(sys.argv) else 'SavedEin.ipynb' 

tree = json.load(open(filename))
if not 'metadata' in tree:
  tree['metadata'] = {
  "celltoolbar": "Slideshow",
  }

for ws in tree['worksheets']:
  for cell in ws['cells']:
    if not 'metadata' in cell or cell['metadata'] is None:
      cell['metadata'] = {}

    if ((cell['cell_type'] == 'markdown'
         and cell['source'][0].startswith('# '))
        or (cell['cell_type'] == 'heading' and cell['level']==1)):
        cell['metadata']['slideshow'] = {
         "slide_type": "slide"
        }

    # Fill in outputs with metadata
    if 'outputs' in cell:
      for out in cell['outputs']:
        if not 'metadata' in out or out['metadata'] is None:
          out['metadata'] = {}

fixed_filename = filename.replace('.ipynb','-fixed.ipynb')
open(fixed_filename,'w').write(json.dumps(tree,indent=2))

if do_run_nb_convert:
  os.system('ipython nbconvert --to slides --post serve --config slides_config.py \"' + fixed_filename + '\"')

  if 0:
    from IPython.nbconvert.exporters import SlidesExporter
    from IPython.config import Config
    
    from IPython.nbformat import current as nbformat
    
    outfile = filename.replace('.ipynb','.slides.html')
    
    notebook = open(fixed_filename).read()
    notebook_json = nbformat.reads_json(notebook)
    
    # This is the config object I talked before: 
    # After the 'url_prefix', you can set the location of your 
    # local reveal.js library, i.e. if the reveal.js is located 
    # in the same directory as your talk.slides.html, then 
    # set 'url_prefix':'reveal.js'.
    
    c = Config({
                'RevealHelpTransformer':{
                    'enabled':True,
                    'url_prefix':'reveal.js',
                    },                
                })
    
    exportHtml = SlidesExporter(config=c)
    (body,resources) = exportHtml.from_notebook_node(notebook_json)
    
    open(outfile, 'w').write(body.encode('utf-8'))
  
    if do_serve:
      os.system('python -m SimpleHTTPServer 8000 &')
      os.system('xdg-open http://127.0.0.1:8000/\"' + outfile + '\"')
  
