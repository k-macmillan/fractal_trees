# Fractals

[![3D Fractal](https://i.imgur.com/oARGCvv.png)](https://sketchfab.com/3d-models/b3d-2317c1f611e14369b7a3b83e29be676b)

<div class="sketchfab-embed-wrapper"><iframe width="640" height="480" src="https://sketchfab.com/models/2317c1f611e14369b7a3b83e29be676b/embed" frameborder="0" allow="autoplay; fullscreen; vr" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
<p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;">
    <a href="https://sketchfab.com/3d-models/b3d-2317c1f611e14369b7a3b83e29be676b?utm_medium=embed&utm_source=website&utm_campaign=share-popup" target="_blank" style="font-weight: bold; color: #1CAAD9;">B3d</a>
    by <a href="https://sketchfab.com/macattackftw?utm_medium=embed&utm_source=website&utm_campaign=share-popup" target="_blank" style="font-weight: bold; color: #1CAAD9;">macattackftw</a>
    on <a href="https://sketchfab.com?utm_medium=embed&utm_source=website&utm_campaign=share-popup" target="_blank" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a>
</p>
</div>

## Unit Tests

Because some of the 3D graphics is enough over my head to get wrong and not even notice, there are
unit tests in the `fractals/tests/` submodule. Run them by running the command `nosetests` from the
repository root directory.

## Process

I'm thinking a three-four part process to rendering the fractals.

1. Given a set of production rules and a starting axiom, perform some number of iterations.
2. Consume the resulting sequence of commands to produce the JSON file of cylinders.
3. Create a Blender file for the fractal (`blender.py`).
4. Touch up the fractal in Blender?? Render the fractal somehow??

## Creating a Blender File

Run

```shell
PYTHONPATH=$(pwd) blender --background --python blender.py -- "F+F"
```

to generate the scene for the given L string. Then open the generated scene with

```shell
blender data/lstring.blend
```
