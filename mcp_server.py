import sys
import json
from client import KLDivergenceDriftMonitor

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-kullback-leibler-divergence-drift-monitor-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "check_kl_drift",
                        "description": "Calculates forward and reverse KL divergence between active and reference policies",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "p_dist": {"type": "array", "items": {"type": "number"}},
                                "q_dist": {"type": "array", "items": {"type": "number"}},
                                "threshold": {"type": "number", "default": 0.2}
                            },
                            "required": ["p_dist", "q_dist"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "check_kl_drift":
            res = KLDivergenceDriftMonitor.compute_kl(
                args.get("p_dist", []),
                args.get("q_dist", []),
                args.get("threshold", 0.2)
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
