# Fractals

Creating 3D fractals in Blender using Lindenmayer Systems.

![3D Fractal](https://i.imgur.com/gQPLXAE.jpg)

[![3D Fractal SketchFab](https://i.imgur.com/oARGCvv.png)](https://sketchfab.com/3d-models/b3d-2317c1f611e14369b7a3b83e29be676b)

## Creating a Blender File

Run

```shell
PYTHONPATH=$(pwd) time blender --background --python scripts/blender.py -- data/b3d.json
```

to generate the scene for the given L string. Then open the generated scene with

```shell
blender data/b3d.blend
```

Note that large fractals take *quite* some time to compose, and may even crash Blender.

## Using Batch Mode

There's a nifty little script (`batch.sh`) to split up work across multiple Blender processes for big
fractals.
Use it like so:

```shell
./batch.sh data/b3d.json --jobs 4
```

This creates several new files in `data/`:

```shell
$ ls data/b3d*
data/b3d.blend  data/b3d-cylinders.json  data/b3d-job-0.blend  data/b3d-job-1.blend  data/b3d-job-2.blend  data/b3d-job-3.blend  data/b3d.json
```

The `b3d-job-*-.blend` files are the results of each individual job, and the `data/b3d.blend` is the
final Blender file containing the joined results.
Note that the results will contain however many objects as there were jobs -- that is, the joining process
does not join all the meshes, it just combines all the objects into one scene.

Then run

```shell
blender data/b3d.blend
```

to view the wonderful results.

## Gray Scott Parameters

Here are the parameters to reproduce all but the three hardest patterns.

```shell
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 8000 -k 0.05 -f 0.017 -r 5 -n 256 --title "Pattern $\\alpha$"
# The -r parameter has a big impact on beta
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 8000 -k 0.045 -f 0.019 -r 2 --title "Patten $\\beta$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 8000 -k 0.052 -f 0.021 -r 10 --title "Pattern $\\gamma$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 5000 -k 0.052 -f 0.026 -r 5 --title "Pattern $\\delta$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 5000 -k 0.052 -f 0.017 -r 2 --title "Pattern $\\epsilon$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 5000 -k 0.06 -f 0.04 -r 2 --scale 0.2 --title "Pattern $\\theta$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 5000 -k 0.064 -f 0.05 -r 5 --scale 0.2 --title "Pattern $\\kappa$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 8000 -k 0.066 -f 0.04 -r 5 --title "Pattern $\\lambda$"
PYTHONPATH=$(pwd) python3 scripts/reaction.py --gui -i 15000 -k 0.0655 -f 0.0565 -r 2 --scale 0.1 --title "Pattern $\\mu$"
```
