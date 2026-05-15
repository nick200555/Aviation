import sys
from frappe.utils import scrub, make_camel_case
print("SCRUB:", scrub("AD Affected Aircraft"))
print("CAMEL:", make_camel_case("AD Affected Aircraft"))
