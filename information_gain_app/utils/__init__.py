def graphwiz_to_png(filename: str):
    import os
    os.system("dot -Tpng {} -o {}.png".format(filename, filename))
