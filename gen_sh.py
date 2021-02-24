import os
import sys

short_trace = False

if len(sys.argv) == 2 and sys.argv[1] == '-short':
    short_trace = True

tracefile = "trace.sh"
logfile = 'tmp.log'
cmd = 'sudo trace-cmd list | grep i915 >' + logfile
os.system(cmd)

with open(logfile, 'rt') as f:
    lines = f.readlines()
os.system('rm ' + logfile)

tracesh = []
tracesh.append('sudo trace-cmd record \\\n')
for l in lines:
    if short_trace == True and 'i915_request' not in l:
        continue
    if l == lines[-1]:
        c = '-e "' + l.strip() + '" \n'
    else:
        c = '-e "' + l.strip() + '" \\\n'
    tracesh.append(c)

if '\\' in tracesh[-1]:
    tracesh[-1] = tracesh[-1].replace('\\', '')

with open(tracefile, "w") as f:
    for i in tracesh:
        f.write(i)
os.system('chmod +x ' + tracefile)

print(tracefile + ' generated')
print('done')
