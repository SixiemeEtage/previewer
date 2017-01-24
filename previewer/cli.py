import time

import click
import cv2
from PIL import Image

from .previewer import PreviewGeneratorNative, PreviewGeneratorOpenCV


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def main(file_path):
    click.echo("Image will be loaded at path '{}'".format(file_path))
    
    preview_size = (1000,750)

    ## OpenCV implementation

    click.echo("Loading image (opencv)...", nl=False)
    t0 = time.time()
    p = PreviewGeneratorOpenCV(file_path, preview_size=preview_size)
    click.echo(" executed in {:.3f}s".format(time.time() - t0))
    
    click.echo("Generating preview (opencv)...", nl=False)
    t0 = time.time()
    out = p.generate()
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    click.echo("Saving the preview...", nl=False)
    t0 = time.time()
    cv2.imwrite('out_1.jpg', out)
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    ## Native implementation

    click.echo("Loading image (native)...", nl=False)
    t0 = time.time()
    p = PreviewGeneratorNative(file_path, preview_size=preview_size)
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    click.echo("Generating preview (native)...", nl=False)
    t0 = time.time()
    out = p.generate()
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    click.echo("Saving the preview...", nl=False)
    t0 = time.time()
    out.save('out_2.jpg')
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    click.echo("Done!")


if __name__ == "__main__":
    main()
