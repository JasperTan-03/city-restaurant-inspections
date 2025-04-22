from collections import defaultdict
from typing import Iterator

from .utils import normalize_space, parse_date


class Transformer:
    def __init__(self, city: str, state: str):
        # ID counters and maps for deduplication
        self._counters = defaultdict(lambda: 1)
        self.cuisine_map = {}
        self.inspection_type_map = {}
        self.action_map = {}
        self.address_map = {}
        self.restaurant_map = {}
        self.inspection_map = {}
        self.violations = []
        self.city = city
        self.state = state

    def _get_id(self, category: str, key):
        """Common helper to assign/get auto-increment IDs per category."""
        if key not in getattr(self, f"{category}_map"):
            _id = self._counters[category]
            getattr(self, f"{category}_map")[key] = _id
            self._counters[category] += 1
        return getattr(self, f"{category}_map")[key]

    def transform_row(self, row: dict):
        # Clean and normalize fields
        camis = normalize_space(row.get("CAMIS"))
        dba = normalize_space(row.get("DBA"))
        # ... repeat for all needed fields ...
        cuisine_desc = normalize_space(row.get("CUISINE DESCRIPTION"))
        inspection_type_desc = normalize_space(row.get("INSPECTION TYPE"))
        action_desc = normalize_space(row.get("ACTION"))

        # Parse dates & numbers
        inspection_date = parse_date(normalize_space(row.get("INSPECTION DATE")))
        grade_date = parse_date(normalize_space(row.get("GRADE DATE")))
        # ... etc ...

        # Deduplicate/lookups
        cuisine_id = self._get_id("cuisine", cuisine_desc) if cuisine_desc else None
        inspection_type_id = (
            self._get_id("inspection_type", inspection_type_desc)
            if inspection_type_desc
            else None
        )
        action_id = self._get_id("action", action_desc) if action_desc else None

        # Address key & ID
        addr_key = (
            normalize_space(row.get("BUILDING")),
            normalize_space(row.get("STREET")),
            normalize_space(row.get("ZIPCODE")),
            normalize_space(row.get("BORO")),
            normalize_space(self.city),
            normalize_space(self.state),
            # ... plus lat/lon, community board, etc ...
        )
        if any(addr_key):
            address_id = self._get_id("address", addr_key)
        else:
            address_id = None

        # Restaurant
        restaurant_id = None  # Initialize to None to avoid UnboundLocalError
        if camis:
            restaurant_id = getattr(self, "restaurant_map").get(camis)
            if not restaurant_id:
                restaurant_id = self._counters["restaurant"]
                self.restaurant_map[camis] = {
                    "RestaurantID": restaurant_id,
                    "ExternalID": camis,
                    "DBA_Name": dba,
                    "CuisineID": cuisine_id,
                    "AddressID": address_id,
                    # ...
                }
                self._counters["restaurant"] += 1

        # Inspection
        insp_key = (restaurant_id, inspection_date, inspection_type_id)
        if all(insp_key):
            if insp_key not in self.inspection_map:
                insp_id = self._counters["inspection"]
                self.inspection_map[insp_key] = {
                    "InspectionID": insp_id,
                    "RestaurantID": restaurant_id,
                    "InspectionTypeID": inspection_type_id,
                    "InspectionDate": inspection_date,
                    "ActionID": action_id,
                    # ...
                }
                self._counters["inspection"] += 1
            else:
                insp_id = self.inspection_map[insp_key]["InspectionID"]

        # Violations
        violation_code = normalize_space(row.get("VIOLATION CODE"))
        if violation_code:
            vid = self._counters["violation"]
            self.violations.append(
                {
                    "ViolationID": vid,
                    "InspectionID": insp_id,
                    "ViolationCode": violation_code,
                    "ViolationDescription": normalize_space(
                        row.get("VIOLATION DESCRIPTION")
                    ),
                    "CriticalFlag": normalize_space(row.get("CRITICAL FLAG")),
                }
            )
            self._counters["violation"] += 1

    def run(self, rows: Iterator[dict]):
        for row in rows:
            self.transform_row(row)
        return {
            "Cuisine": self.cuisine_map,
            "InspectionType": self.inspection_type_map,
            "Action": self.action_map,
            "Address": self.address_map,
            "Restaurant": self.restaurant_map,
            "Inspection": self.inspection_map,
            "Violation": self.violations,
        }
