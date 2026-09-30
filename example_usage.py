from client import KLDivergenceDriftMonitor

p = [0.8, 0.1, 0.1]
q = [0.33, 0.33, 0.34]
res = KLDivergenceDriftMonitor.compute_kl(p, q)
print("Policy Divergence Telemetry:", res)
