import time

import click
import cv2
from PIL import Image

from .previewer import PreviewGeneratorNative, PreviewGeneratorOpenCV


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), default='output.jpg')
@click.option('--preview-height', type=int, default=750)
@click.option('--preview-width', type=int, default=1000)
@click.option('--fov', type=float, default=55.0)
@click.option('--latitude', type=float, default=0.0)
@click.option('--longitude', type=float, default=0.0)
@click.option('--no-opencv', type=bool, default=False)
def main(file_path, output, preview_height, preview_width, fov, latitude, longitude, no_opencv):
    click.echo(click.style("Image will be loaded from path '{}'".format(file_path), fg='blue'))

    preview_size = (preview_width, preview_height)
    click.echo(click.style("Preview will be generated at size '{}'".format(preview_size), fg='blue'))

    click.echo("Loading image...", nl=False)
    t0 = time.time()
    if not no_opencv:
        p = PreviewGeneratorOpenCV(file_path, preview_size=preview_size, fov=fov, latitude=latitude, longitude=longitude)
    else:
        click.echo(click.style("Warning: very unefficient implementation, it might take more than a minute", fg='orange'))
        p = PreviewGeneratorNative(file_path, preview_size=preview_size, fov=fov, latitude=latitude, longitude=longitude)
    click.echo(" executed in {:.3f}s".format(time.time() - t0))
    
    click.echo("Generating preview...", nl=False)
    t0 = time.time()
    out = p.generate()
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    click.echo("Saving the preview...", nl=False)
    t0 = time.time()
    cv2.imwrite(output, out)
    click.echo(" executed in {:.3f}s".format(time.time() - t0))

    click.echo(click.style("Done!", fg='green'))


if __name__ == "__main__":
    main()
