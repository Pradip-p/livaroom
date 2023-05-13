# import subprocess

# import os
# import subprocess
# from django.conf import settings


# def run_spider():
#     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     script_path = os.path.join(base_dir, 'run_spider.sh')
#     if os.path.exists(script_path):
#         subprocess.run([script_path])
#     else:
#         print(f"Error: {script_path} does not exist")
from django_cron import CronJobBase, Schedule
from subprocess import call

class ProductCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # execute every 1 hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'products.product_cron_job'    # a unique code for this cron job

    def do(self):
        # code to be executed when the cron job runs
        # for example, run a shell script
        call(['/bin/bash', '-c', 'source /root/livaroom/tools/bin/activate && /root/livaroom/run_spider.sh'])
