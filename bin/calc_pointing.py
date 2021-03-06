#!/usr/bin/env python

__author__ = "Natasha Hurley-Walker"
__date__ = "10/09/2019"

import sys
from optparse import OptionParser #NB zeus does not have argparse!
from astropy.io import fits
from astropy.coordinates import EarthLocation, SkyCoord
from astropy import units as u

def calc_optimal_ra_dec(metafits):
    hdu = fits.open(options.metafits)
    alt = hdu[0].header["ALTITUDE"]
    if alt < 55. :
        az = hdu[0].header["AZIMUTH"]
        date = hdu[0].header["DATE-OBS"]
        mwa = EarthLocation.of_site("Murchison Widefield Array")
# Empirical testing shows that if the altitude is < 55 degrees, the pointing is actually 8 degrees above where you think it is
        alt += 8.0
        newaltaz = SkyCoord(az, alt, frame="altaz", unit=(u.deg, u.deg), obstime=date, location=mwa)
        newradec = newaltaz.transform_to("fk5")
    else:
        newradec = SkyCoord(hdu[0].header["RA"], hdu[0].header["Dec"], unit = (u.deg, u.deg))
    return newradec

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: %prog [options]" +
    """
    Highly off-zenith pointings have maximum primary beam sensitivity quite far from the pointing centre.
    This script returns the ideal phase centre for the GLEAM-X pointings.
    """)
    parser.add_option("--metafits", default=None, dest="metafits", help="Metafits filename")
    options, args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    else:
        radec = calc_optimal_ra_dec(options.metafits)
        print radec.to_string("hmsdms")



