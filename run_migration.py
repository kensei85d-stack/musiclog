import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", "initial_tables"],
    cwd=r"C:\Users\kense\Documents\portforio\musiclog"
)
sys.exit(result.returncode)
