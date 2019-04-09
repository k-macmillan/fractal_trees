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

## TODO

* Automate camera placement using the object(s) bounding box:

  [option 1](https://docs.blender.org/api/blender_python_api_current/bpy.types.Object.html#bpy.types.Object.bound_box),
  [option 2](https://blender.stackexchange.com/questions/8459/get-blender-x-y-z-and-bounding-box-with-script)
* Play with more 3d fractals.
  * Generate the classic 2D fractals
  * Try to find 3D analogs of each
  * Create own fancy 3D fractals
  * See what other kinds of shapes we can create other than trees.
* Play with random perturbations.
* Start working on the paper
  * Outline how the different commands work in 3D with simple examples.
  * Be sure to do the actual problem he assigned.
  * Discuss 3D trees
  * Discuss 3D koch island-like fractals
* Start on the other 4 problems.
  1. Use L-Systems to reproduce the book pictures (done)
  2. Do fractal landscapes (maybe in Blender, if we can figure out gradient colors when rendering)
  3. Be less extra on the CAs --- they'll be very easy in numpy, and matplotlib can do nice colors.
  4. It might be necessary to use Numba on the Gray-Scott model.
