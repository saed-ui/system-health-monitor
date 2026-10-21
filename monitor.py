# system health monitor
# checks cpu, ram and disk, logs to csv, yells if something looks bad

import argparse
import csv
import os
import time
from datetime import datetime

import psutil

LOG_FILE = "health_log.csv"

# default limits (percent). go over these = warning
CPU_LIMIT = 85
MEM_LIMIT = 85
DISK_LIMIT = 90


def get_stats(disk_path):
    # cpu needs a tiny wait to get a real number
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage(disk_path).percent
    return cpu, mem, disk


def check_limits(cpu, mem, disk, limits):
    warnings = []
    if cpu > limits["cpu"]:
        warnings.append(f"cpu is at {cpu}% (limit {limits['cpu']}%)")
    if mem > limits["mem"]:
        warnings.append(f"memory is at {mem}% (limit {limits['mem']}%)")
    if disk > limits["disk"]:
        warnings.append(f"disk is at {disk}% (limit {limits['disk']}%)")
    return warnings


def log_row(path, row):
    # write header only if file is new
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp", "cpu_percent", "mem_percent", "disk_percent", "status"])
        w.writerow(row)


def main():
    p = argparse.ArgumentParser(description="simple system health monitor")
    p.add_argument("--interval", type=int, default=5, help="seconds between checks")
    p.add_argument("--count", type=int, default=0, help="how many checks (0 = forever)")
    p.add_argument("--cpu", type=float, default=CPU_LIMIT, help="cpu warn limit %%")
    p.add_argument("--mem", type=float, default=MEM_LIMIT, help="memory warn limit %%")
    p.add_argument("--disk", type=float, default=DISK_LIMIT, help="disk warn limit %%")
    p.add_argument("--path", default=os.path.abspath(os.sep), help="disk to check")
    p.add_argument("--log", default=LOG_FILE, help="csv log file")
    args = p.parse_args()

    limits = {"cpu": args.cpu, "mem": args.mem, "disk": args.disk}
    print(f"watching your system every {args.interval}s. ctrl+c to stop.\n")

    done = 0
    try:
        while args.count == 0 or done < args.count:
            cpu, mem, disk = get_stats(args.path)
            warnings = check_limits(cpu, mem, disk, limits)
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "WARN" if warnings else "OK"

            print(f"[{stamp}] cpu {cpu:5.1f}% | mem {mem:5.1f}% | disk {disk:5.1f}% | {status}")
            for w in warnings:
                print(f"   ⚠️  WARNING: {w}")

            log_row(args.log, [stamp, cpu, mem, disk, status])
            done += 1

            # no point sleeping after the last one
            if args.count == 0 or done < args.count:
                time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nstopped. bye")

    print(f"\nlogged {done} checks to {args.log}")


if __name__ == "__main__":
    main()
