import os

bw = 12
buf = 750
dl = 15
plr = 0.0

#schemes = "pcc_kernel"
schemes = "pcc_experimental"
#schemes = "default_tcp bbr pcc_experimental copa vivace_latency pcc"

mm_delay = "mm-delay %d" % dl

mm_loss = "mm-loss uplink %f" % plr

mm_cmds = mm_delay + " " + mm_loss

mm_opts = "--uplink-queue=droptail --uplink-queue-args=bytes=" + str(1000 * buf)

cmd = "python gen_trace.py --bw=%d" % bw
os.system(cmd)

cmd = "./test/test.py local --schemes \"%s\" -t 30 --interval 15 --run-times 3 --flows 2 --uplink-trace %s --downlink-trace %s --prepend-mm-cmds \"%s\" --extra-mm-link-args \"%s\"" % (schemes, "link.trace", "link.trace", mm_cmds, mm_opts)
os.system(cmd)

cmd = "./analysis/analyze.py --data-dir test/data/"
os.system(cmd)
