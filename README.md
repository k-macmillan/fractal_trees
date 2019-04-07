# Fractals

Creating 3D fractals in Blender using Lindenmayer Systems.


![3D Fractal](https://i.imgur.com/gQPLXAE.jpg)


[![3D Fractal SketchFab](https://i.imgur.com/oARGCvv.png)](https://sketchfab.com/3d-models/b3d-2317c1f611e14369b7a3b83e29be676b)

## Creating a Blender File

Run

```shell
PYTHONPATH=$(pwd) time blender --background --python blender.py -- data/b3d.json
```

to generate the scene for the given L string. Then open the generated scene with

```shell
blender data/b3d.blend
```

Note that large fractals take *quite* some time to compose, and may even crash Blender.

## TODO

* Improve rendering speed on large fractals.
  * It is possible to combine objects from multiple files. So generate the JSON file of cylinders,
    and render chunks of it, then combine all the chunks.

    This will likely work best/easiest from a Bash script.
* Improve colors/materials
  * Make color/material configurable from L-string?
  * Make color/material configurable from JSON/commandline?
* Play with more 3d fractals after runtime issues are fixed.
  * Generate the classic 2D fractals
  * Try to find 3D analogs of each
  * Create own fancy 3D fractals
  * See what other kinds of shapes we can create other than trees.
* Play with proportional radii and other radius sizes.
* Start working on the paper
  * Outline how the different commands work in 3D with simple examples.
  * Be sure to do the actual problem he assigned.
  * Discuss 3D trees
  * Discuss 3D koch island-like fractals
* Figure out what the second problem is (probably something with CAs).
