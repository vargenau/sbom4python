# Copyright (C) 2022 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0


import json


class LicenseScanner:
    def __init__(self):
        # Load licenses
        licfile = open("license_data/spdx_licenses.json")
        self.licenses = json.load(licfile)

    def find_license(self, license):
        # Search list of licenses to find match

        default_license = "UNKNOWN"
        for lic in self.licenses["licenses"]:
            # Comparisons ignore case of provided license text
            if lic["licenseId"].lower() == license.lower():
                return lic["licenseId"]
            elif lic["name"].lower() == license.lower():
                return lic["licenseId"]
        return default_license