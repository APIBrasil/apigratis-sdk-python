"""Configuração compartilhada dos testes: garante ``src/`` no ``sys.path``."""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
