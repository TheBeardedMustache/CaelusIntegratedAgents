"""
Master Process Framework entry-point implementing the Star of Caelus flow.
Usage: python scripts/star_of_caelus_pipeline.py --intent "Export canvases" --agent exporter
"""
import argparse
import importlib

from sefirot import run_sefirot

parser = argparse.ArgumentParser()
parser.add_argument('--intent', required=True)
parser.add_argument('--agent', required=True)
args = parser.parse_args()

agent = importlib.import_module(f"agents.{args.agent}").Agent()
print(run_sefirot(args.intent, agent))
