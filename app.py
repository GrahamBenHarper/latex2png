from flask import Flask, render_template, request, send_file
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

def RunCMD(cmd: str, timeout = 15):
    """
        Runs a command, captures stdout & stderr, trims output
        timeout: how long to let command run, -1 for infinite
    """

    proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    try:
        if timeout == -1:
            outs, errs = proc.communicate()
        else:
            outs, errs = proc.communicate(timeout=timeout)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    outs = outs.decode("UTF-8").strip()
    errs = (errs.decode("UTF-8").strip() if errs else None)

    return {"out": outs, "err": errs, "ret": proc.returncode}


app = Flask(__name__)


def save_file():
    # TODO: make this a non-blocking operation and update the page after the command executes if possible
    # TODO: fix how the textbox works... it's a little gross at the moment
    
    # steps:
    # 1. Create a file using the template
    f = open("equation.tex","w")
    f.write("\\documentclass[12pt]{article}\n")
    f.write("\\usepackage[utf8]{inputenc}\n")
    f.write("\\usepackage{amsmath,amsfonts,amssymb}\n")
    f.write("\\begin{document}\n")
    f.write("\\begin{align*}\n")
    
    equation = request.args.get("equation")
    f.write(equation)
    f.write("\\end{align*}\n")
    f.write("\\pagenumbering{gobble}\n")
    f.write("\\end{document}\n")
    f.close()

    # 2. Compile to pdf
    cmd = "pdflatex equation.tex"
    print("Executing: " + cmd)
    res = RunCMD(cmd, -1)
    if(not res["ret"]==0):
        print("Command exited with status: " + str(res["ret"]))
        if(res["out"]==None):
            res["out"]=""
        if(res["err"]==None):
            res["err"]=""
        print("Command stdout: " + res["out"])
        print("        stderr: " + res["err"])
        return render_template("index.html", equation_image="latex_failed.png")
    
    # 3. Convert to png
    cmd = "convert -density 300 equation.pdf -quality 90 -trim static/equation.png"
    print("Executing: " + cmd)
    res = RunCMD(cmd, -1)
    if(not res["ret"]==0):
        print("Command exited with status: " + str(res["ret"]))
        if(res["out"]==None):
            res["out"]=""
        if(res["err"]==None):
            res["err"]=""
        print("Command stdout: " + res["out"])
        print("        stderr: " + res["err"])
        return render_template("index.html", equation_image="convert_failed.png")
    
    return render_template("index.html", equation_image="equation.png")

@app.route('/')
def index():
    if not request.args.get("equation"):
        return render_template("index.html", equation_image="equation.png")

    return save_file()

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
