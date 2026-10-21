# system health monitor

a small python script that keeps an eye on your computer. every few seconds it checks **cpu**, **memory** and **disk** usage, saves each check to a csv file, and warns you when something gets too high.

works on windows, mac and linux.

## what it does

- checks cpu, ram and disk usage (using `psutil`)
- prints a clean line for each check
- shows a ⚠️ warning when something goes over the limit
- logs every check to `health_log.csv` so you can look back later (or open it in excel)

## setup

```bash
git clone https://github.com/<your-username>/system-health-monitor.git
cd system-health-monitor
pip install -r requirements.txt
```

## how to use

run it forever (checks every 5 seconds, stop with ctrl+c):

```bash
python monitor.py
```

run 10 checks, 2 seconds apart:

```bash
python monitor.py --count 10 --interval 2
```

set your own warning limits (in %):

```bash
python monitor.py --cpu 70 --mem 80 --disk 95
```

all options:

| option | what it does | default |
|---|---|---|
| `--interval` | seconds between checks | 5 |
| `--count` | how many checks (0 = forever) | 0 |
| `--cpu` | cpu warning limit % | 85 |
| `--mem` | memory warning limit % | 85 |
| `--disk` | disk warning limit % | 90 |
| `--path` | which disk to check | root drive |
| `--log` | csv file to write to | health_log.csv |

## example output

```
watching your system every 2s. ctrl+c to stop.

[2026-10-21 20:30:01] cpu  12.4% | mem  41.2% | disk  58.0% | OK
[2026-10-21 20:30:04] cpu  91.0% | mem  42.0% | disk  58.0% | WARN
   ⚠️  WARNING: cpu is at 91.0% (limit 85%)
```

## the csv log

```
timestamp,cpu_percent,mem_percent,disk_percent,status
2026-10-21 20:30:01,12.4,41.2,58.0,OK
2026-10-21 20:30:04,91.0,42.0,58.0,WARN
```

## built with

- python 3
- [psutil](https://github.com/giampaolo/psutil)

## todo maybe

- send an email or discord message when there's a warning
- check network usage too
- make a little chart from the csv
- run it as a background service on startup
- show the top 5 programs eating cpu when it spikes
