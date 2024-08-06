"""
Reading, saving, and  handling population models 
"""
import asdf
import numpy as np

def load_population_model(model):

    pth = f'data/popsycle_singles_{model}.asdf'

    f = 