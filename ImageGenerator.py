import pygame
import numpy as np
import time
from scipy.ndimage import label

# ---- Settings ----

SCALE = 25                          # Multiplyer to scale the window up to
ImageSize = 16                      # Image screen width and height
MinClusterSize = 20                 # Minimum Cluster Size to search for in pixels
DensityThreshold = 0.7              # density threshold between 0 and 1 (lower = longer less dense clusters, higher = more dense clusters)
FlashEnabled = False               # Set to True to flash the screen when a cluster is found
HideNonClusters = True            # Set to True to hide all pixels except for the found clusters
NonClusterColor = [100, 100, 100] # The color of the pixels that are not part of a cluster

# Colors that will be used in the image
# More colors = Longer times
# I recommend using 2 to 3 colors, but you can use as many as you want
PALETTE = np.array([
    [0, 0, 0],       # Black
    [255, 255, 255], # White
    # [255, 0, 0],     # Red
    # [0, 255, 0],     # Green
    # [0, 0, 255],     # Blue
    # [255, 255, 0],   # Yellow
    # [255, 0, 255],   # Magenta
    # [0, 255, 255]    # Cyan
], dtype=np.uint8)

# ---- Settings ----

pygame.init()

Width, Height = ImageSize, ImageSize
Window = pygame.display.set_mode((Width * SCALE, Height * SCALE), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Random Image Generator")

Arr = np.empty((Height, Width, 3), dtype=np.uint8)

Running = True
Paused = False

LastTime = time.time()
Frames = 0

HighlightMask = None
FlashOn = False
FlashInterval = 0.5
LastFlashTime = time.time()

ScaledSurface = pygame.Surface((Width * SCALE, Height * SCALE))
ClustersOnlySurface = None
HighlightSurface = None

def GetDenseClusterMask(ColorIndices):
    CombinedMask = np.zeros((Height, Width), dtype=bool)
    for ColorId in range(len(PALETTE)):
        Mask = (ColorIndices == ColorId)
        if np.count_nonzero(Mask) < MinClusterSize:
            continue

        Structure = np.ones((3, 3), dtype=bool)
        LabeledArray, NumFeatures = label(Mask, structure=Structure)
        if NumFeatures == 0:
            continue

        ClusterSizes = np.bincount(LabeledArray.ravel())[1:]
        
        for LabelId in np.where(ClusterSizes >= MinClusterSize)[0] + 1:
            ClusterMask = (LabeledArray == LabelId)
            Coords = np.argwhere(ClusterMask)
            
            YMin, XMin = Coords.min(axis=0)
            YMax, XMax = Coords.max(axis=0)
            
            BboxArea = (YMax - YMin + 1) * (XMax - XMin + 1)
            Density = ClusterSizes[LabelId - 1] / BboxArea if BboxArea > 0 else 0
            
            if Density >= DensityThreshold:
                CombinedMask = CombinedMask | ClusterMask

    if np.any(CombinedMask):
        return CombinedMask
    else:
        return None

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and Paused:
            print("Resuming...")
            Paused = False
            HighlightMask = None
            HighlightSurface = None
            ClustersOnlySurface = None

    if not Paused:
        ColorIndices = np.random.randint(0, len(PALETTE), (Height, Width))
        Arr[:] = PALETTE[ColorIndices]
        
        HighlightMask = GetDenseClusterMask(ColorIndices)

        if HighlightMask is not None:
            print(f"Found dense cluster!")
            Paused = True
            
            if HideNonClusters:
                TempArr = np.full((Height, Width, 3), NonClusterColor, dtype=np.uint8)
                TempArr[HighlightMask] = Arr[HighlightMask]
                ClustersOnlySurface = pygame.surfarray.make_surface(TempArr).convert()
                ClustersOnlySurface = pygame.transform.scale(ClustersOnlySurface, (Width * SCALE, Height * SCALE))


        Surface = pygame.surfarray.make_surface(Arr).convert()
        ScaledSurface = pygame.transform.scale(Surface, (Width * SCALE, Height * SCALE))
        Window.blit(ScaledSurface, (0, 0))
        pygame.display.flip()
        
        Frames += 1
        Now = time.time()
        if Now - LastTime >= 1.0:
            print(f"FPS: {Frames}")
            Frames = 0
            LastTime = Now

    else:
        Now = time.time()
        if FlashEnabled and (Now - LastFlashTime > FlashInterval):
            FlashOn = not FlashOn
            LastFlashTime = Now

        BaseSurface = ClustersOnlySurface if HideNonClusters and ClustersOnlySurface else ScaledSurface
        Window.blit(BaseSurface, (0, 0))

        if HighlightMask is not None and FlashEnabled and FlashOn:
            if HighlightSurface is None:
                Blended = Arr.copy()
                Blended[HighlightMask] = 255 - Blended[HighlightMask]
                HighlightSurface = pygame.surfarray.make_surface(Blended).convert_alpha()
                HighlightSurface = pygame.transform.scale(HighlightSurface, (Width * SCALE, Height * SCALE))
            
            Window.blit(HighlightSurface, (0, 0))

        pygame.display.flip()

pygame.quit()

