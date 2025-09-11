import os
import importlib
from flask import Blueprint

routes_dir = os.path.dirname(__file__)
blueprints = []

for filename in os.listdir(routes_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'routes.{filename[:-3]}'
        module = importlib.import_module(module_name)
        if hasattr(module, 'bp'):
            blueprints.append(module.bp)
