from indeed import get_jobs as get_indeed_jobs
from SO import get_jobs as get_so_jobs
from indeed import setting_to_job as setting_to_job_indeed
from SO import setting_to_job as setting_to_job_SO
from save import save_to_file

job = input("어떤 언어의 직종을 원하십니까?\n")

setting_to_job_indeed(job)
setting_to_job_SO(job)
indeed_jobs = get_indeed_jobs()
so_jobs = get_so_jobs()
jobs = so_jobs + indeed_jobs
save_to_file(jobs)
