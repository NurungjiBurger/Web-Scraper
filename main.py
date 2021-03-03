from indeed_scrapper import get_jobs as get_indeed_jobs
from so_scrapper import get_jobs as get_so_jobs
from exporter import save_to_file
from flask import Flask, render_template, request, redirect, send_file

app = Flask("SuperScrapper")


DB = {}

@app.route("/") 
def home():
  return render_template("home.html")

@app.route("/report")
def report():
  word = request.args.get('word')
  if word:
    word = word.lower()
    existingJobs = DB.get(word)
    if existingJobs:
      jobs = existingJobs
    else:
      indeed_jobs = get_indeed_jobs(word)
      so_jobs = get_so_jobs(word)
      jobs = indeed_jobs + so_jobs
      DB[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception();
    word = word.lower()
    jobs = DB.get(word)
    if not jobs:
      raise Exception();
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run(host="0.0.0.0")


"""
job = input("어떤 언어의 직종을 원하십니까?\n")

setting_to_job_indeed(job)
setting_to_job_SO(job)
indeed_jobs = get_indeed_jobs()
so_jobs = get_so_jobs()
jobs = so_jobs + indeed_jobs
save_to_file(jobs)
"""
