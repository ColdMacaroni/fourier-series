# fourier-series
To make your own. First use the generator to create a set of constants. 

`py generate_starting_conditions.py path/to/svg`

e.g. `py generate_starting_conditions.py svgs/duck.svg 20`

It will ask you for a resolution. It corresponds to how finely it will calculate each path. Then the amount of *pairs* of circles. The more it has, the more accurate the final image will be.

Then run `py fourier_series.py`. It will read the constants and generate the series accordingly. You may specify a unit to determine the scale. Just try until the whole thing fits on the screen. Usually `1` is fine. It supports floats

e.g. `py fourier_series.py 1.1` This will make it slightly bigger

There's a 27% possibility that there's a memory leak somewhere. Idk where im a python programer

run time customizations coming soon ig

## Contributors
 [MR-Spagetty](https://github.com/MR-Spagetty)