# Fractals

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
