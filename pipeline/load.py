from typing import Any, Dict, List

from .utils import sql_val


def generate_inserts(data: Dict) -> Dict[str, List[str]]:
    """
    Given transformed data, produce SQL INSERT statements per table.
    Returns a dict: table_name -> list of SQL strings.
    """
    inserts: Dict[str, List[str]] = {table: [] for table in data}

    # Cuisine
    for desc, cid in data["Cuisine"].items():
        inserts["Cuisine"].append(
            f"INSERT INTO Cuisine (CuisineID, CuisineDescription) "
            f"VALUES ({cid}, {sql_val(desc)});"
        )

    # InspectionType
    for desc, tid in data["InspectionType"].items():
        inserts["InspectionType"].append(
            f"INSERT INTO InspectionType (InspectionTypeID, TypeName, Description) "
            f"VALUES ({tid}, {sql_val(desc)}, {sql_val(desc)});"
        )

    # Action
    for desc, aid in data["Action"].items():
        inserts["Action"].append(
            f"INSERT INTO Action (ActionID, ActionDescription) "
            f"VALUES ({aid}, {sql_val(desc)});"
        )

    # Address
    for addr_key, aid in data["Address"].items():
        # Unpack the tuple in the same order used in transform
        # addr_line, zip_code, borough, city, state, *rest = addr_key
        addr_line = addr_key[0] + " " + addr_key[1]
        zip_code = addr_key[2]
        borough = addr_key[3]
        city = addr_key[4]
        state = addr_key[5]
        inserts["Address"].append(
            "INSERT INTO Address (AddressID, AddressLine1, ZipCode, Borough, City, State) "
            f"VALUES ({aid}, {sql_val(addr_line)}, {sql_val(zip_code)}, {sql_val(borough)}, {sql_val(city)}, {sql_val(state)});"
        )

    # Restaurant
    for rest in data["Restaurant"].values():
        inserts["Restaurant"].append(
            "INSERT INTO Restaurant (RestaurantID, ExternalID, DBA_Name, CuisineID, AddressID) "
            f"VALUES ({rest['RestaurantID']}, {sql_val(rest['ExternalID'])}, "
            f"{sql_val(rest['DBA_Name'])}, {sql_val(rest['CuisineID'])}, {sql_val(rest['AddressID'])});"
        )

    # Inspection
    for insp in data["Inspection"].values():
        inserts["Inspection"].append(
            "INSERT INTO Inspection (InspectionID, RestaurantID, InspectionTypeID, InspectionDate, ActionID) "
            f"VALUES ({insp['InspectionID']}, {insp['RestaurantID']}, "
            f"{insp['InspectionTypeID']}, {sql_val(insp['InspectionDate'])}, {sql_val(insp['ActionID'])});"
        )

    # Violation
    for viol in data["Violation"]:
        inserts["Violation"].append(
            "INSERT INTO Violation (ViolationID, InspectionID, ViolationCode, ViolationDescription, CriticalFlag) "
            f"VALUES ({viol['ViolationID']}, {viol['InspectionID']}, "
            f"{sql_val(viol['ViolationCode'])}, {sql_val(viol['ViolationDescription'])}, {sql_val(viol['CriticalFlag'])});"
        )

    return inserts


def write_sql_files(inserts: Dict[str, List[str]], out_dir: str = "."):
    """Write each list of INSERTs to its own .sql file in out_dir."""
    for table, stmts in inserts.items():
        path = f"{out_dir}/insert_{table.lower()}.sql"
        with open(path, "w") as f:
            for line in stmts:
                f.write(line + "\n")
