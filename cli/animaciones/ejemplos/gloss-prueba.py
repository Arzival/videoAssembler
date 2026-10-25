"""Corre un guion existente con el tema «gloss» (ver gloss.py), sin modificarlo.
Uso: SALIDA=noticias/2/animaciones-gloss REL=noticias/2/animaciones-gloss python3 ejemplos/gloss-prueba.py ellog-02 [ids…]
"""
import os, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import gloss

sys.modules.update({'ellog': gloss.L, 'tarjetas': gloss.T, 'escenas': gloss.E})
guion = sys.argv.pop(1)
sys.argv[0] = os.path.join(HERE, f'{guion}.py')
runpy.run_path(sys.argv[0], run_name='__main__')
