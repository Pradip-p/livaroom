from django_cron import CronJobBase, Schedule
from subprocess import call

# class ProductCronJob(CronJobBase):
#     RUN_EVERY_MINS = 60 # execute every 1 hour

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'products.product_cron_job'    # a unique code for this cron job

#     def do(self):
#         # code to be executed when the cron job runs
#         # for example, run a shell script
#         call(['/bin/bash', '-c', 'source /root/livaroom/tools/bin/activate && /root/livaroom/run_spider.sh'])
from django_cron import CronJobBase, Schedule
from subprocess import call

class ProductCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # execute every 1 hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    
    code = 'products.cron.ProductCronJob'    # update the code attribute
    # code = 'products.product_cron_job'    # a unique code for this cron job

    def do(self):
        # code to be executed when the cron job runs
        # for example, run a shell script
        call(['/bin/bash', '-c', 'source /root/livaroom/tools/bin/activate && /root/livaroom/crawler/livaroom_com.py'])
        # call(['/bin/bash', '-c', 'source /root/livaroom/tools/bin/activate && /root/livaroom/crawler/english.py'])
