from indeed import get_jobs as get_indeed_jobs
from SO import get_jobs as get_so_jobs
from save import save_to_file
from flask import Flask, render_template, request, redirect

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
    fromDB = DB.get(word)
    if fromDB:
      jobs = fromDB
    else:
      indeed_jobs = get_indeed_jobs(word)
      so_jobs = get_so_jobs(word)
      jobs = indeed_jobs + so_jobs
      DB[word] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=word, resultsNumber=len(jobs))

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
