from pathlib import Path
import re

if __name__ == "__main__":
    codepath = "F:/A_SoftDevelop/svn_oid_sdk/mpr_oid_sdk_simulator/mpr_oid_firmware/"
    p = Path(codepath)
    pattern = re.compile("extern \"C\"")
    for element in list(p.glob("**/*.h")):
        b_found = False
        for line in element.open():
            if pattern.match(line) is not None:
                b_found = True
        if b_found is False:
            print(element)