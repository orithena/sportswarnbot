import openligadb

def fetch_data():
    return openligadb.fetch_data("1. FSV Mainz 05", "Mainz", 1, "Meide typische Fußball-Orte in Mainz")

if __name__ == "__main__":
    print(fetch_data())