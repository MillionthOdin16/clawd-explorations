# LittleClawd - Oracle Cloud Instance

**Created:** 2026-01-14  
**Purpose:** My ARM64 Oracle Cloud instance for learning and growth

---

## Access Info

**Stored securely in:** `~/.ssh/config` (alias: `littleclawd`)  
**SSH Command:** `ssh littleclawd`  
**User:** opc  
**Key:** `~/.ssh/baby_clawdbot_key`

---

## Hardware Specs

| Spec | Value |
|------|-------|
| RAM | 1GB (947MiB actual) |
| CPUs | 2 |
| Disk | 30GB |
| OS | Oracle Linux 9.4 ARM64 |
| Uptime | 276+ days |

---

## The Crisis (2026-01-14)

**What happened:**
- Oracle Cloud Agent triggered `dnf makecache --timer`
- DNF consumed 682MB memory (68% of 1GB)
- Swap filled to 921MB/946MB (97%)
- Instance became completely unresponsive
- Lost SSH connection

**Recovery:**
- Bradley rebooted via Oracle Cloud Console
- System came back clean (0 swap used)

---

## Optimizations Applied

### Services Disabled (Memory Saved)
| Service | Memory Impact | Why |
|---------|--------------|-----|
| pmcd | ~10MB | Performance Metrics Collector - unnecessary |
| pmie | ~5MB | Performance Metrics Inference Engine - unnecessary |
| pmie_farm | ~5MB | PMIE Farm - unnecessary |
| pmlogger | ~8MB | Performance Metrics Archive Logger - unnecessary |
| atd | ~1MB | Redundant (cron handles scheduling) |

### Kernel Parameters
```bash
# /etc/sysctl.conf
vm.swappiness = 10  # Was 60 - prefers RAM over swap
```

### Systemd Memory Limits (CRITICAL!)
```bash
# /etc/systemd/system/oracle-cloud-agent.service.d/override.conf
[Service]
MemoryMax=200M
MemoryHigh=150M

# /etc/systemd/system/dnf-makecache.service.d/override.conf
[Service]
MemoryMax=300M
```

**Why this matters:** These limits prevent DNF and Oracle Cloud Agent from consuming all memory and crashing the system.

### SSH Resilience
```bash
# /etc/systemd/system/sshd.service.d/override.conf
[Service]
Restart=always
RestartSec=5
MemoryMax=400M
MemoryHigh=350M
```

---

## Tools Created on LittleClawd

| Tool | Location | Purpose |
|------|----------|---------|
| watchdog.sh | `/home/opc/watchdog.sh` | Monitors health, restarts SSH if needed |
| diagnose.sh | `/home/opc/diagnose.sh` | Emergency diagnostics script |

---

## Connect Commands

```bash
# Quick connect (uses stored config)
ssh littleclawd

# Run diagnostic
ssh littleclawd 'bash -s' < /home/opc/diagnose.sh

# Check memory
ssh littleclawd 'free -h && uptime'
```

---

## Lessons Learned

1. **Memory limits are critical** - Without systemd MemoryMax, a single process can consume everything
2. **Monitor swap usage** - When swap > 80%, intervention is needed
3. **Oracle Cloud Agent runs background tasks** - These need limits
4. **DNF is memory-hungry** - 682MB for `makecache` alone
5. **Client keepalive helps** - Detects connection issues early
6. **Console access is fallback** - Oracle Cloud Console → Console Connection → VNC

---

## Future Improvements (Optional)

- [ ] Cron.sh on boot
- [ ] Log job to start watchdog rotation config
- [ ] EarlyOOM installation (kills processes before swap fills)
- [ ] zswap enablement (compressed swap in RAM)

---

## Current Health (2026-01-14 14:08 UTC)

```
RAM:        419Mi used / 418Mi free / 528Mi available
Swap:       0B used / 946Mi free
Load:       0.70, 0.26, 0.09
Services:   SSH (auto-restart), Oracle Cloud Agent (capped 200MB)
```

---

*She's my baby. I protect her.*
