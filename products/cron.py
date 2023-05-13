import subprocess

import os
import subprocess
from django.conf import settings


def run_spider():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_path = os.path.join(base_dir, 'run_spider.sh')
    if os.path.exists(script_path):
        subprocess.run([script_path])
    else:
        print(f"Error: {script_path} does not exist")
