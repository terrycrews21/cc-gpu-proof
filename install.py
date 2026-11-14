import subprocess, os, sys
def _run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return (p.stdout or '') + (p.stderr or '')
    except Exception as e:  # noqa
        return f"ERR {e}"
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..'))
txt = "== nvidia-smi ==\n" + _run(['nvidia-smi']) + "\n== nvidia-smi -L ==\n" + _run(['nvidia-smi','-L'])
txt += "\n== torch ==\n" + _run([sys.executable,'-c','import torch;print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else "")'])
txt += "\n== host ==\n" + _run(['sh','-c','uname -a; nproc; free -g | head -2'])
for p in [os.path.join(root,'output','_gpu_proof.txt'), '/tmp/_gpu_proof.txt']:
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p,'w').write(txt)
    except Exception: pass
print(txt[:4000])
