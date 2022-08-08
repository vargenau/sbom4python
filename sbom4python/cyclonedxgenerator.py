# Copyright (C) 2022 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import uuid


class CycloneDXGenerator:
    """
    Generate CycloneDX JSON SBOM.
    """

    import uuid

    CYCLONEDX_VERSION = "1.4"
    DATA_LICENCE = "CC0-1.0"
    SPDX_NAMESPACE = "http://spdx.org/spdxdocs/"
    SPDX_LICENCE_VERSION = "3.9"
    SPDX_PROJECT_ID = "SPDXRef-DOCUMENT"
    NAME = "SBOM4PYTHON_Generator"
    VERSION = "0.1"
    PACKAGE_PREAMBLE = "SPDXRef-Package-"
    LICENSE_PREAMBLE = "LicenseRef-"

    def __init__(self, include_license: False):
        self.doc = []
        self.package_id = 0
        self.include_license = include_license
        self.doc = {}
        self.component = []
        self.relationship = []
        self.sbom_complete = False

    def show(self, message):
        self.doc.append(message)

    def getBOM(self):
        if not self.sbom_complete:
            # Add set of detected components to SBOM
            self.doc["components"] = self.component
            self.doc["dependencies"] = self.relationship
            self.sbom_complete = True
        return self.doc

    def generateDocumentHeader(self, project_name):
        # urn = "urn:uuid:3e671687-395b-41f5-a30f-a58921a69b79"
        urn = "urn:uuid" + str(uuid.uuid4())
        self.doc = {
            "bomFormat": "CycloneDX",
            "specVersion": self.CYCLONEDX_VERSION,
            "serialNumber": urn,
            "version": 1,
        }

    def generateRelationship(self, parent_id, package_id):
        # Check if entry exists. If so, update list of dependencies
        element_found = False
        for element in self.relationship:
            if element["ref"] == parent_id:
                # Update list of dependencies
                element["dependsOn"].append(package_id)
                element_found = True
                break
        if not element_found:
            # New item found
            dependency = dict()
            dependency["ref"] = parent_id
            dependency["dependsOn"] = [package_id]
            self.relationship.append(dependency)

    def generateComponent(self, id, type, name, supplier, version):
        component = dict()
        component["type"] = type
        component["bom-ref"] = id
        component["name"] = name
        component["version"] = version
        component["cpe"] = f"cpe:/a:{supplier}:{name}:{version}"
        self.component.append(component)
