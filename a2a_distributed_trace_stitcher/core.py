"""Core W3C traceparent parser and cross-agent A2A trace stitcher."""
import re
from typing import Any, Dict, List, Optional


TRACEPARENT_RE = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


class A2ATraceStitcher:
    """Correlates W3C traceparent headers across distributed A2A agent invocations."""

    def make_traceparent(self, trace_id: str, span_id: str, flags: str = "01") -> str:
        header = f"00-{trace_id}-{span_id}-{flags}"
        if not TRACEPARENT_RE.match(header):
            raise ValueError("Invalid trace_id, span_id, or flags format")
        return header

    def parse_traceparent(self, header: str) -> Dict[str, str]:
        m = TRACEPARENT_RE.match(header.strip().lower())
        if not m:
            raise ValueError(f"Malformed W3C traceparent: {header}")
        return {"trace_id": m.group(1), "span_id": m.group(2), "flags": m.group(3)}

    def stitch(self, spans: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        by_trace: Dict[str, List[Dict[str, Any]]] = {}
        for sp in spans:
            tid = sp["trace_id"]
            by_trace.setdefault(tid, []).append(dict(sp))

        stitched: Dict[str, List[Dict[str, Any]]] = {}
        for tid, items in by_trace.items():
            # Sort by start_ms ascending, placing root (parent_span_id=None) first on ties
            stitched[tid] = sorted(
                items,
                key=lambda x: (x.get("start_ms", 0.0), 0 if x.get("parent_span_id") is None else 1),
            )
        return stitched
