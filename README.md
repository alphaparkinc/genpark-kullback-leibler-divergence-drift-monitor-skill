# genpark-kullback-leibler-divergence-drift-monitor-skill

Telemetry monitor calculating forward, reverse, and symmetric Kullback-Leibler (KL) divergence to prevent reward hacking.

## Architecture

```mermaid
flowchart LR
    P["Active Policy pi_theta"] --> KL["Kullback-Leibler Engine"]
    Q["Reference Policy pi_ref"] --> KL
    KL --> Fwd["Forward KL(P || Q)"]
    KL --> Rev["Reverse KL(Q || P)"]
    Fwd --> Guard{KL > Threshold?}
    Guard -->|Yes| Alert[Trigger Drift Alert / Step Rollback]
    Guard -->|No| Safe[Policy Within Safe Bounds]
```

## Features
- **Symmetric & Asymmetric Drift**: Tracks both mode collapse and out-of-distribution tokens.
- **Zero Dependencies**: 100% Python Standard Library.
