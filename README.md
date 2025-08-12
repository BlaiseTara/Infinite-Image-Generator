# Infinite Image Generator
This is a simple Infinite Image Generator that I coded.
It uses Python and PyGame to draw random pixels on the screen.
Each frame it uses a function to check the entire canvas for groups of pixels which could potentially be an "Image".
Most of the time it will just be random pixels, but there is always the chance that it could generate an actual image.
(probably not tho...)

# Instructions
You will need Python and Pygame installed,
along with Numpy and SciPy.

Basically just run the python file, and watch it generate.
If it finds anything, it will pause until you press any key.

# Settings
By default I have it setup to generate a Black and White, 16x16 image.
But here are some values you can change inside the file:

```SCALE = 25```

This value multiplys the window size based off the Width and Height


```ImageSize = 16```

This is the Size in Pixels that the window will be


```MinClusterSize = 20```

This is the Minimum Cluster size that it searches for in pixels, in this case it is looking for clusters 20px or bigger


```DensityThreshold = 0.7```

This is how dense a cluster can be before it is found,
Values closer to 0 will result in finding clusters that are longer and spread out
Values closer to 1 will result in finding cluster that are smaller and more dense


There is more variables you can change, but these are the most important.
All other values are explained more in the code file.
Just check it out, or you can finish this instructions for me and make a PR. IDC...
