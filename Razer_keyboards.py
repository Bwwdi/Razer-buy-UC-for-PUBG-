Product = 5151
cods = 4325235
import os

with open(f"Pins [{Product}UC].txt", "a") as tw:
    tw.write(f"{cods}""\n")
    tw.close()
with open(f"Pins [{Product}UC].txt") as f:
    text = f.read()
    lines = text.count('\n')
    f.close()
if lines == 1:
    os.rename(f'Pins [{Product}UC].txt', f'{lines} Pin [{Product}UC].txt')
    file_name = f'{lines} Pin {Product}UC.txt'
if lines > 1:
    os.rename(f'Pins [{Product}UC].txt', f'{lines} Pins [{Product}UC].txt')
    file_name = f'{lines} Pins [{Product}UC].txt'
print(file_name)