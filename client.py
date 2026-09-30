"""Kullback-Leibler Divergence Drift Monitor.
100% Python Standard Library.
"""

import math

class KLDivergenceDriftMonitor:
    """Tracks probability distribution drift between active and reference policies."""
    @staticmethod
    def compute_kl(p_dist: list, q_dist: list, drift_threshold: float = 0.2) -> dict:
        kl_forward = 0.0
        kl_reverse = 0.0

        for p, q in zip(p_dist, q_dist):
            p_safe = max(1e-12, p)
            q_safe = max(1e-12, q)
            kl_forward += p_safe * math.log(p_safe / q_safe)
            kl_reverse += q_safe * math.log(q_safe / p_safe)

        is_drifted = kl_forward > drift_threshold
        return {
            "kl_forward": round(kl_forward, 4),
            "kl_reverse": round(kl_reverse, 4),
            "symmetric_kl": round((kl_forward + kl_reverse) / 2.0, 4),
            "drift_detected": is_drifted,
            "status": "ALERT_DRIFT" if is_drifted else "STABLE"
        }
