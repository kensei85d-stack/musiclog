#!/usr/bin/env python
import sys
import os
from alembic import command
from alembic.config import Config

os.chdir(os.path.dirname(__file__))
cfg = Config('alembic.ini')
command.revision(cfg, autogenerate=True, message='initial tables')
