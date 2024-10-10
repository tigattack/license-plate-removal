#!/usr/bin/env python3

import os

import click
import cv2

from helpers import Helpers

helpers = Helpers()

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    "-s",
    "--source",
    type=click.Path(exists=True),
    required=True,
    help="Source image path.",
)
@click.option(
    "-d",
    "--destination",
    type=click.Path(exists=True),
    help="Destination image path. Default is <source>_obfuscated.<ext>",
)
@click.option(
    "-f",
    "--force",
    help="Overwrite the destination file if it exists.",
    is_flag=True,
    default=False,
)
def obfuscate_plate(source: str, destination: str | None, force: bool) -> None:
    """Obfuscate the number plate in the given image."""

    if not destination:
        fileparts = os.path.splitext(source)
        destination = fileparts[0] + "_obfuscated" + fileparts[1]

    # Open image
    imageCv = helpers.openImageCv(source)

    # Pre-processing
    gray = helpers.cvToGrayScale(imageCv)
    bilateral = helpers.cvApplyBilateralFilter(gray)
    blur = helpers.cvApplyGaussianBlur(bilateral, 5)

    # Detect edge contours and find the plate contour
    edged = helpers.cvToCannyEdge(blur)
    contours = helpers.cvExtractContours(edged)
    rectangleContours = helpers.cvFilterRectangleContours(contours)
    plateContour = rectangleContours[0]
    plateContour = helpers.cvResizeContour(plateContour, 1.0)

    # Crop and blur the plate
    plateImage = helpers.cvCropByContour(imageCv, plateContour)

    # Find the plate's background color
    plateBackgroundColor = helpers.cvFindMostOccurringColor(plateImage)

    # Draw over the plate
    result = cv2.drawContours(
        imageCv.copy(), [plateContour], -1, plateBackgroundColor, -1
    )

    # Save the result
    if os.path.exists(destination) and not force:
        click.echo(f"File already exists: {destination}")
        return

    cv2.imwrite(destination, result)
    click.echo(f"Obfuscated image saved as: {destination}")


if __name__ == "__main__":
    obfuscate_plate()
