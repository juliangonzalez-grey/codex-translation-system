# Import dependencies                                                             
from translate_service import load_demo_data, translate

# Testing data
print("\nLoading data")
load_demo_data()

print("\nTranslate Ibuprofen with filter lang")
print(translate("Ibuprofen", lang="en"))
