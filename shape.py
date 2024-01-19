from PIL import Image
from sympy import isprime
from alive_progress import alive_bar
import numpy as np
from multiprocessing.pool import ThreadPool

def get_pixels(dimx: int, dimy: int):
    with alive_bar(dimx) as bar:
        def get_range(dimx: int, dimy: int, start: float, end: float):
            pixels = np.zeros((dimx, dimy))
            for x in range(int(start*dimx), int(end*dimx)):
                for y in range(0, dimy):
                    pixels[x][y] = int(isprime(x**2 + y**2))
                # Progress bar
                bar()
            return pixels
        
        pool = ThreadPool(processes=4)
        q1 = pool.apply_async(func=get_range, args=[dimx, dimy, 0.0 , 0.25])
        q2 = pool.apply_async(func=get_range, args=[dimx, dimy, 0.25, 0.5 ])
        q3 = pool.apply_async(func=get_range, args=[dimx, dimy, 0.5 , 0.75])
        q4 = pool.apply_async(func=get_range, args=[dimx, dimy, 0.75, 1.0 ])
        q1.wait()
        q2.wait()
        q3.wait()
        q4.wait()
        return np.uint8(np.logical_or(np.logical_or(np.logical_or(q1.get(), q2.get()), q3.get()), q4.get()))

# size = 3000
# pixels = get_pixels(size, size)
# im = Image.fromarray(pixels*255, "L")
# im.save(f"shape_{size}.png")
# im.show()
