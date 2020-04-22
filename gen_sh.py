import os

tracefile = "trace_cmd.sh"
logfile = 'tmp.log'
cmd = 'sudo trace-cmd list | grep i915 >' + logfile
os.system(cmd)

with open(logfile, 'rt') as f:
    lines = f.readlines()
os.system('rm ' + logfile)

tracesh = []
tracesh.append('sudo trace-cmd record \\\n')
for l in lines:
    c = '-e "' + l.strip() + '" \\\n'
    tracesh.append(c)
tracesh.append('sleep $1\n')

with open(tracefile, "w") as f:
    for i in tracesh:
        f.write(i)
os.system('chmod +x ' + tracefile)

print(tracefile + ' generated')
print('done')
