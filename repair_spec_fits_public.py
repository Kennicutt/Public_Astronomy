# This file is part of Public Astronomy.
#
# Public Astronomy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Public Astronomy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Public Astronomy. If not, see <https://www.gnu.org/licenses/>.


import glob, sys

from astropy.io import fits
import matplotlib.pyplot as plt

ROOT = "Root directory"


if __name__ == "__main__":
    program = sys.argv[1]
    block = sys.argv[2]

    lst_spectra = sorted(glob.glob(ROOT + f"/rest of the route/Science/spec_*.fits"))

    column_name = "wave"

    for spectrum in lst_spectra:
        with fits.open(spectrum, mode='update') as hdulist:
            bin_table_hdu = hdulist[1]
            column_data = bin_table_hdu.data[column_name]
            filtered_data = bin_table_hdu.data[column_data != 0]
            new_bin_table_hdu = fits.BinTableHDU(data=filtered_data, header=bin_table_hdu.header)
            hdulist[1] = new_bin_table_hdu
            hdulist.flush()
        
        flux = new_bin_table_hdu.data["flux"].astype("float64")
        wave = new_bin_table_hdu.data["wave"].astype("float64")

        plt.plot(wave,flux, 'k-')
        plt.pause(2)
        plt.close()
