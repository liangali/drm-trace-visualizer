import sys
import json

if len(sys.argv) == 2:
    logfile = sys.argv[1]
else:
    logfile = "f:\\trace.log"

class EventItem():
    def __init__(self, line):
        self.line = line
        self.process = ''
        self.pname = ''
        self.pid = ''
        self.cpu = ''
        self.timestamp = 0
        self.eventname = ''
        self.dev = ''
        self.engine = ''
        self.hw_id = ''
        self.ctx = ''
        self.seqno = ''
        self.complete = ''
        self.gemobj = ''
        self.gemsize = ''
        self.metadata = {}
        self.metastring = ""
        self.parse(line)
    
    def getValue(self, tag):
        seg = self.line.split(tag+'=')
        if len(seg) > 1:
            v = seg[1].split(',')[0]
            return v.rstrip()
        return ''

    def parse(self, line):
        seg = line.split()
        self.process = seg[0].strip()
        self.pname, self.pid = self.process.rsplit('-', 1)
        self.cpu = seg[1][1:-1]
        self.timestamp = int(seg[2][:-1].replace('.', ''))
        self.eventname = seg[3][:-1]
        self.dev = self.getValue('dev')
        self.engine = self.getValue('engine')
        self.hw_id = self.getValue('hw_id')
        self.ctx = self.getValue('ctx')
        self.seqno = self.getValue('seqno')
        self.complete = self.getValue('completed?')
        self.gemobj = self.getValue('obj')
        self.gemsize = self.getValue('size')
        self.setMeta()

    def setMeta(self):
        self.metadata = {}
        if len(self.process) > 0:
            self.metadata["process"] = self.process
        if len(self.eventname) > 0:
            self.metadata["eventname"] = self.eventname
        if len(self.dev) > 0:
            self.metadata["dev"] = self.dev
        if len(self.engine) > 0:
            self.metadata["engine"] = self.engine
        if len(self.hw_id) > 0:
            self.metadata["hw_id"] = self.hw_id
        if len(self.ctx) > 0:
            self.metadata["ctx"] = self.ctx
        if len(self.seqno) > 0:
            self.metadata["seqno"] = self.seqno
        self.metastring = json.dumps(self.metadata)

class TraceDB():
    def __init__(self, filename):
        self.filename = filename
        self.eventlist = []
        self.procs = []
        self.enames = []
        self.devs = []
        self.engines = []
        self.hw_ids = []
        self.ctxs = []
        self.seqnos = []

    def validEvent(self, line):
        if line.find('[') >0 and line.find(']') and line.find(':'):
            return True
        else:
            return False

    def initalize(self):
        with open(self.filename, "rt") as f:
            for line in f:
                if self.validEvent(line):
                    e = EventItem(line)
                    self.eventlist.append(e)
        for e in self.eventlist:
            if e.process not in self.procs:
                self.procs.append(e.process)
            if e.eventname not in self.enames:
                self.enames.append(e.eventname)
            if len(e.dev) > 0 and e.dev not in self.devs:
                self.devs.append(e.dev)
            if len(e.engine) > 0 and e.engine not in self.engines:
                self.engines.append(e.engine)
            if len(e.hw_id) > 0 and e.hw_id not in self.hw_ids:
                self.hw_ids.append(e.hw_id)
            if len(e.ctx) > 0 and e.ctx not in self.ctxs:
                self.ctxs.append(e.ctx)
            if len(e.seqno) > 0 and e.seqno not in self.seqnos:
                self.seqnos.append(e.seqno)
        return len(self.eventlist)

    def getEventsByProc(self, proc):
        elproc = []
        for e in self.eventlist:
            if e.process == proc:
                elproc.append(e)
        return elproc

    def getCtxsByProc(self, proc):
        ctxs = []
        for e in self.eventlist:
            if e.process == proc and e.ctx != "" and e.ctx not in ctxs:
                ctxs.append(e.ctx)
        return ctxs

    def getEventsByNameAndCtx(self, name, ctx):
        el = []
        for e in self.eventlist:
            if e.ctx == ctx and e.eventname == name:
                el.append(e)
        return el

    def getEventsByNameAndProc(self, name, proc):
        el = []
        for e in self.eventlist:
            if e.process == proc and e.eventname == name:
                el.append(e)
        return el

    def getEventsByName(self, name):
        el = []
        for e in self.eventlist:
            if e.eventname == name:
                el.append(e)
        return el

class EventMeta():
    def __init__(self, name, pid, tid, args):
        self.type = 'M'
        self.name = name
        self.pid = pid
        self.tid = tid
        self.args = args
        self.string = self.toString()
    def toString(self):
        out = '{'
        out = out + '"ph":"' + self.type + '", '
        out = out + '"name":"' + self.name + '", '
        out = out + '"pid":"' + self.pid + '", '
        out = out + '"tid":"' + self.tid + '", '
        out = out + '"args":' + self.args + '}, \n'
        return out

class EventX():
    def __init__(self, name, pid, tid, ts, dur, meta):
        self.type = 'X'
        self.name = name
        self.pid = pid
        self.tid = tid
        self.ts = ts
        self.dur = dur
        self.meta = meta
        self.string = self.toString()
    def toString(self):
        out = '{'
        out = out + '"ph":"' + self.type + '", '
        out = out + '"name":"' + self.name + '", '
        out = out + '"pid":"' + self.pid + '", '
        out = out + '"tid":"' + self.tid + '", '
        out = out + '"ts":"' + self.ts + '", '
        if len(self.meta) == 0:
            out = out + '"dur":' + self.dur
        else:
            out = out + '"dur":' + self.dur + ', '
            out = out + '"args":' + self.meta
        out = out + '}, \n'
        return out

class EventC():
    def __init__(self, name, pid, tid, ts, value):
        self.type = 'C'
        self.name = name
        self.pid = pid
        self.tid = tid
        self.ts = ts
        self.value = value
        self.string = self.toString()
    def toString(self):
        out = '{'
        out = out + '"ph":"' + self.type + '", '
        out = out + '"name":"' + self.name + '", '
        out = out + '"pid":"' + self.pid + '", '
        out = out + '"tid":"' + self.tid + '", '
        out = out + '"ts":"' + self.ts + '", '
        arg = '"args":{"name": ' + self.value + '}'
        out = out + arg + '}, \n'
        return out

class EventA():
    def __init__(self, tag, cat, id, name, pid, tid, ts):
        self.type = tag
        self.cat = cat
        self.id = id
        self.name = name
        self.pid = pid
        self.tid = tid
        self.ts = ts
        self.string = self.toString()
    def toString(self):
        out = '{'
        out = out + '"ph":"' + self.type + '", '
        out = out + '"cat":"' + self.cat + '", '
        out = out + '"id":"' + self.id + '", '
        out = out + '"name":"' + self.name + '", '
        out = out + '"pid":"' + self.pid + '", '
        out = out + '"tid":"' + self.tid + '", '
        out = out + '"ts":"' + self.ts + '"}, \n'
        return out

def buildJsonProc(tdb, outjson):
    for p in tdb.procs:
        arg = '{"name":"' + p + '"}'
        pid = p.split('-')[1]
        if pid == '0':
            pid = '10'
        tid = '0'
        gproc = EventMeta('process_name', pid, tid, arg)
        gthread = EventMeta('thread_name', pid, tid, arg)
        gsort = EventMeta('process_sort_index', pid, tid, '{"sort_index":"' + pid + '"}')
        outjson.append(gproc.toString())
        outjson.append(gthread.toString())
        outjson.append(gsort.toString())
        for e in tdb.getEventsByProc(p):
            gevent = EventX(e.eventname, pid, tid, str(e.timestamp), "1", e.metastring)
            outjson.append(gevent.toString())
    print('build json for process... done!')

def buildJsonEngine(tdb, outjson):
    for engine in tdb.engines:
        engineName = {'0':'Render', '1':'BLT', '2':'VDBOX', '3':'VEBOX', '4':'CCS'}
        pid, tid = engine.split(':')
        name = engineName[pid] + '-' + tid
        argProc = '{"name":"' + engineName[pid] + '"}'
        argThread = '{"name":"' + name + '"}'
        gproc = EventMeta('process_name', pid, tid, argProc)
        gthread = EventMeta('thread_name', pid, tid, argThread)
        gsort = EventMeta('process_sort_index', pid, tid, '{"sort_index":"' + pid + '"}')
        outjson.append(gproc.toString())
        outjson.append(gthread.toString())
        outjson.append(gsort.toString())
    for ctx in tdb.ctxs:
        eli = tdb.getEventsByNameAndCtx('i915_request_in', ctx)
        elo = tdb.getEventsByNameAndCtx('i915_request_out', ctx)
        prev_seqno = ''
        for i in eli:
            found = 0
            for o in elo:
                if i.seqno == o.seqno:
                    found = 1
                    name = i.seqno
                    if o.complete == "0":
                        name = name+"a"
                    if prev_seqno == i.seqno:
                        name = name+"b"
                    pid, tid = i.engine.split(':')
                    dur = o.timestamp - i.timestamp
                    g = EventX(name, pid, tid, str(i.timestamp), str(dur), i.metastring)
                    outjson.append(g.toString())
                    prev_seqno = i.seqno
                    elo.remove(o)
                    break
            if found == 0:
                name = i.seqno
                pid, tid = i.engine.split(':')
                dur = 10
                g = EventX(name, pid, tid, str(i.timestamp), str(dur), i.metastring)
                outjson.append(g.toString())
    print('build json for engine... done!')

def buildJsonContext(tdb, outjson):
    for p in tdb.procs:
        ctxs = tdb.getCtxsByProc(p)
        elqueue = tdb.getEventsByNameAndProc('i915_request_queue', p)
        elretire = tdb.getEventsByName('i915_request_retire')
        if len(elqueue) == 0:
            continue
        pid = p.split('-')[1]
        for c in ctxs:
            tid = c
            argThread = '{"name":"' + 'GPU Context ' + c + '"}'
            gthread = EventMeta('thread_name', pid, tid, argThread)
            outjson.append(gthread.toString())
            for e in elqueue:
                if e.ctx == c:
                    gevent = EventX(e.seqno, pid, tid, str(e.timestamp), "10", e.metastring)
                    outjson.append(gevent.toString())
    print('build json for context done.')

def buildJsonMemory(tdb, outjson):
    mem_count = 0
    graphname = "GEM memory usage"
    arg = '{"name":"' + 'Memory' + '"}'
    pid, tid = '5', '0'
    gproc = EventMeta('process_name', pid, tid, arg)
    gthread = EventMeta('thread_name', pid, tid, arg)
    gsort = EventMeta('process_sort_index', pid, tid, '{"sort_index":"' + pid + '"}')
    outjson.append(gproc.toString())
    outjson.append(gthread.toString())
    outjson.append(gsort.toString())

    gem_create = tdb.getEventsByName('i915_gem_object_create')
    for ec in gem_create:
        mem_count = mem_count + int(ec.gemsize, 0)
        c = EventC(graphname, pid, tid, str(ec.timestamp), str(mem_count))
        outjson.append(c.toString())

    gem_destroy = tdb.getEventsByName('i915_gem_object_destroy')
    for ed in gem_destroy:
        dsize = '0x0'
        for ec in gem_create:
            if ed.gemobj == ec.gemobj:
                dsize = ec.gemsize;
                break
        mem_count = mem_count - int(dsize, 0)
        c = EventC(graphname, pid, tid, str(ed.timestamp), str(mem_count))
        outjson.append(c.toString())
    print('build json for memory... done!')

def buildJsonSubmit(tdb, outjson):
    pid, tid = '6', '0'
    arg = '{"name":"' + 'CMD Submission' + '"}'
    gproc = EventMeta('process_name', pid, tid, arg)
    gsort = EventMeta('process_sort_index', pid, tid, '{"sort_index":"' + pid + '"}')
    outjson.append(gproc.toString())
    outjson.append(gsort.toString())
    elsubmit = tdb.getEventsByName('i915_request_submit')
    ctxlist = []
    for e in elsubmit:
        tid = e.ctx
        if e.ctx not in ctxlist:
            ctxlist.append(e.ctx)
            arg = '{"name":"' + 'ctx=' + e.ctx + '"}'
            gthread = EventMeta('thread_name', pid, tid, arg)
            gsort = EventMeta('thread_sort_index', pid, tid, '{"sort_index":"' + tid + '"}')
            outjson.append(gthread.toString())
            outjson.append(gsort.toString())
        g = EventX(e.seqno, pid, tid, str(e.timestamp), "10", e.metastring)
        outjson.append(g.toString())

    print('build json for submission... done!')

if __name__ == "__main__":
    outjson = []
    tdb = TraceDB(logfile)
    tdb.initalize()
    print('structuralize trace log... done!')

    buildJsonProc(tdb, outjson)
    buildJsonEngine(tdb, outjson)
    buildJsonContext(tdb, outjson)
    buildJsonMemory(tdb, outjson)
    buildJsonSubmit(tdb, outjson)

    with open(logfile.split('.')[0]+'.json', 'wt') as f:
        f.writelines('[\n')
        f.writelines(outjson)
    print('execution finished!')