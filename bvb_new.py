import openligadb

def fetch_data():
    return openligadb.fetch_data("Borussia Dortmund", "Dortmund", 1, "Meide U42/U46/Kreuzviertel/Borsigplatz/Uni-Parkplatz")

if __name__ == "__main__":
    print(fetch_data())