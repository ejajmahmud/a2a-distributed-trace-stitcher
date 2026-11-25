"""CLI for A2A Distributed Trace Stitcher."""
import argparse
import json
from .core import A2ATraceStitcher


def main():
    parser = argparse.ArgumentParser(description="A2A Distributed Trace Stitcher CLI")
    parser.add_argument("--demo", action="store_true", help="Stitch sample multi-agent trace")
    args = parser.parse_args()

    s = A2ATraceStitcher()
    tid = "0af7651916cd43dd8448eb211c80319c"
    res = s.stitch([
        {"trace_id": tid, "span_id": "2222222222222222", "parent_span_id": "1111111111111111", "agent": "reviewer", "start_ms": 20.0},
        {"trace_id": tid, "span_id": "1111111111111111", "parent_span_id": None, "agent": "orchestrator", "start_ms": 0.0},
    ])
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
