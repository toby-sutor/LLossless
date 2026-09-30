import os, sys, pathlib, tempfile, shutil, subprocess, re, json
S = pathlib.Path("<home>/Documents/Dev/claude-tmp/claimcheck/2026-09-26-sourced-2183")
TREE = S / "tree"; sys.path.insert(0, str(TREE / "src"))
import llossless
assert llossless.__file__.startswith(str(TREE / "src") + "/"), llossless.__file__
from llossless import config
from llossless.web import commands
model = sys.argv[1]; wrapper = sys.argv[2]; work = pathlib.Path(sys.argv[3]); extra = sys.argv[4:]
with tempfile.TemporaryDirectory() as tmp:
    book = commands.Commands(pathlib.Path(tmp) / "commands.json"); book.enable(f"claude-{model}")
    env_route = dict(book.get(f"claude-{model}").environ())
argv = env_route["LLOSSLESS_COMMAND"].split()
env_route["LLOSSLESS_COMMAND"] = " ".join([wrapper, *argv[1:]])
print("route:", config.command_with_isolation(env_route["LLOSSLESS_COMMAND"]))
DROP = re.compile(r"^(CLAUDE|AI_AGENT|LLOSSLESS_|CLAIMCHECK_)")
env = {k: v for k, v in os.environ.items() if not DROP.match(k)}
env.update(env_route); env["PYTHONPATH"] = str(TREE / "src")
if work.exists(): shutil.rmtree(work)
(work / "tmp").mkdir(parents=True); env["TMPDIR"] = str(work / "tmp")
src = TREE / "tests" / "handwritten" / "voyager"
for p in src.glob("source_*.md"): shutil.copy(p, work / p.name)
cmd = [sys.executable, "-m", "llossless", "merge", "source_a.md", "source_b.md", "--base", "source_a.md", *extra,
       "--json", str(work / "report.json"), "-o", str(work / "merged.md")]
p = subprocess.run(cmd, env=env, cwd=str(work), capture_output=True, text=True, timeout=3600)
(work / "stdout.txt").write_text(p.stdout); (work / "stderr.txt").write_text(p.stderr)
print("exit", p.returncode); print(p.stderr[-1500:])
