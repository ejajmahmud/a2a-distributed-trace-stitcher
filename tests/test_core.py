"""Tests for A2A Distributed Trace Stitcher."""
import unittest
from a2a_distributed_trace_stitcher.core import A2ATraceStitcher


class TestA2ATraceStitcher(unittest.TestCase):
    def test_traceparent_roundtrip_and_stitch_order(self):
        s = A2ATraceStitcher()
        tid = "a" * 32
        hdr = s.make_traceparent(tid, "b" * 16)
        parsed = s.parse_traceparent(hdr)
        self.assertEqual(parsed["trace_id"], tid)

        stitched = s.stitch([
            {"trace_id": tid, "span_id": "2" * 16, "parent_span_id": "1" * 16, "start_ms": 15.0},
            {"trace_id": tid, "span_id": "1" * 16, "parent_span_id": None, "start_ms": 0.0},
        ])
        self.assertEqual([x["span_id"] for x in stitched[tid]], ["1" * 16, "2" * 16])

    def test_malformed_traceparent_raises(self):
        with self.assertRaises(ValueError):
            A2ATraceStitcher().parse_traceparent("bad-header")
