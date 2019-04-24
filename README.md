Creating 3D fractals in Blender using Lindenmayer Systems.

![3D Fractal](https://i.imgur.com/gQPLXAE.jpg)

[![3D Fractal SketchFab](https://i.imgur.com/oARGCvv.png)](https://sketchfab.com/3d-models/b3d-2317c1f611e14369b7a3b83e29be676b)

- [Creating Lindenmayer System Fractals](#creating-lindenmayer-system-fractals)
- [Creating Fractal Landscapes](#creating-fractal-landscapes)
- [Running the 2D Heat Flow Simulation](#running-the-2d-heat-flow-simulation)
- [Gray Scott Parameters](#gray-scott-parameters)
- [Building the Paper](#building-the-paper)

## Creating Lindenmayer System Fractals

Note that large fractals take *quite* some time to compose, and may even crash Blender, or in extreme circumstances your entire operating system.

Use the [`batch.sh`](./batch.sh) script like so:

```shell
./batch.sh data/b3d.json --jobs 4
```

This will use 4 Blender processes to create the `data/b3d.blend` Blender scene.
Doing so creates several new files in `data/`:

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

Use [`clean.sh`](./clean.sh) to remove the intermediate generated files to save several gigabytes of disk space between runs.

The `batch.sh` script combines the `scripts/generate.py`, `scripts/render.py`, and  `scripts/join.py` scripts, each with their own usage.
For simplicity's sake, we recommend using the wrapper `batch.sh` script which runs each of the listed scripts in the correct order, even if the number of jobs is set to 1.

## Creating Fractal Landscapes

Use [`scripts/landscapes.py`](scripts/landscapes.py) to generate the fractal landscapes.
Its usage statement is given below

```shell
$ PYTHONPATH=$(pwd) python3 scripts/landscapes.py --help
usage: landscapes.py [-h] [--one] [--recursions RECURSIONS [RECURSIONS ...]]
                     [--scale SCALE [SCALE ...]] [--hurst HURST [HURST ...]]
                     [--seed SEED] [--sealevel SEALEVEL] [--title TITLE]
                     [--gui] [--output OUTPUT]

Generate fractal landscapes with the random midpoint displacement algorithm.

optional arguments:
  -h, --help            show this help message and exit
  --one                 Generate a 1D heightmap.
  --recursions RECURSIONS [RECURSIONS ...], -r RECURSIONS [RECURSIONS ...]
                        The number of recursive subdivisions.
  --scale SCALE [SCALE ...], -s SCALE [SCALE ...]
                        The vertical scale.
  --hurst HURST [HURST ...], -H HURST [HURST ...]
                        The Hurst roughness exponent.
  --seed SEED           The random seed.
  --sealevel SEALEVEL, -l SEALEVEL
                        The landscape sealevel.
  --title TITLE, -t TITLE
                        The plot title.
  --gui                 Open the plot in a GUI window.
  --output OUTPUT, -o OUTPUT
                        The file to save the plot to.

If multiple values for recursions, scale, or hurst are given, every
combination of the given parameters will be plotted on the same axis. It is
advisable to avoid plotting multiple 3D surface plots on the same axis.
```

Notice the use of the `PYTHONPATH` environment variable to make the `natural` Python library discoverable to the `landscapes.py` script.

An example usage is given below to generate a 2D landscape

```shell
$ PYTHONPATH=$(pwd) python3 scripts/landscapes.py --gui -r5 -l -0.3 -H 0.7
seed: 2729300867
```

Notice that if a seed is not given, a seed will be generated and the random number generator will be seeded so that each landscape is reproducible.

## Running the 2D Heat Flow Simulation

Use the [`scripts/heat.py`](scripts/heat.py) script to run the 2D heatflow simulation.
Its usage statement is given below

```shell
$ PYTHONPATH=$(pwd) python3 scripts/heat.py --help
usage: heat.py [-h] [--ymin YMIN] [--ymax YMAX] [--rows ROWS] [--cols COLS]
               [--timestep TIMESTEP] [--prows PROWS] [--pcols PCOLS]
               [--title TITLE] [--output OUTPUT] [--gui]

Generate 2D heat diffusion plots with CAs.

optional arguments:
  -h, --help            show this help message and exit

  --ymin YMIN           The lower domain y boundary.
  --ymax YMAX           The upper domain y boundary.
  --rows ROWS           The number of cells to use along the y axis.
  --cols COLS           The number of cells to use along the x axis.

  --timestep TIMESTEP, -i TIMESTEP
                        The time interval to generate subplots at.
  --prows PROWS         The number of rows of subplots.
  --pcols PCOLS         The number of columns of subplots
  --title TITLE         The plot title.
  --output OUTPUT       The output filename.
  --gui                 Open the plot in a GUI window.
```

Notice that there are options to generate subplots of several timeslices of the diffusion process.
An example usage is given below.

```shell
$ PYTHONPATH=$(pwd) python3 scripts/heat.py --gui --timestep 1000 --rows 100 --cols 100
```

## Gray Scott Parameters

The usage statement for the [`scripts/reaction.py`](scripts/reaction.py) is given below.

```shell
$ PYTHONPATH=$(pwd) python3 scripts/reaction.py --help
usage: reaction.py [-h] [--gui] [--output OUTPUT] [--title TITLE] [--uv]
                   [--size SIZE] [--ru RU] [--rv RV] [--feed FEED]
                   [--kill KILL] [--iterations ITERATIONS] [--radius RADIUS]
                   [--u0 U0] [--v0 V0] [--scale SCALE]

Run the Gray-Scott Model with configurable parameters.

optional arguments:
  -h, --help            show this help message and exit

  --gui                 Open a GUI window displaying the plot.
  --output OUTPUT, -o OUTPUT
                        The filename to save the results as.
  --title TITLE         The plot title.
  --uv                  Plot both U and V concentrations.

  --size SIZE, -n SIZE  The grid size.
  --ru RU               The U diffusion rate.
  --rv RV               The V diffusion rate.
  --feed FEED, -f FEED  The U feed rate.
  --kill KILL, -k KILL  The U,V kill rate.
  --iterations ITERATIONS, -i ITERATIONS
                        The number of iterations.

  --radius RADIUS, -r RADIUS
                        The initial high concentration center radius.
  --u0 U0               The initial high concentration center U concentration.
  --v0 V0               The initial high concentration center V concentration.
  --scale SCALE, -s SCALE
                        The scale of the initial uniform distribution.
```

Notice that there are *many* tweakable parameters.

An example usage of the `scripts/reaction.py` script is shown below.

```shell
$ PYTHONPATH=$(pwd) python3 scripts/reaction.py                                \
      --iterations 5000                                                        \
      --kill 0.05                                                              \
      --feed 0.017                                                             \
      --radius 5                                                               \
      --size 128                                                               \
      --title "Pattern $\\alpha$"                                              \
      --gui                                                                    \
      --output alpha.eps
```

All of the original patterns in Pearson's original work can be generated by the paper's makefile:

```shell
$ cd papers
$ make figures
```

## Building the Paper

The paper can be built by running the included makefile.
However, note that doing so requires the appropriate Python libraries installed.
There is an included [`requirements.txt`](requirements.txt) file containing the necessary libraries.

```shell
$ virtualenv ~/.virtualenvs/natural
$ source ~/.virtualenvs/natural/bin/activate
$ pip install -r requirements.txt
$ cd paper
$ make -j 8
```

Also notice that most of the figures in the paper are generated as prerequisite steps in the build process, so the first time you build the paper will take *quite some time*. **Be sure to enable parallel builds.**
