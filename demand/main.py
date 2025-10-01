from demand.rail_line import RailLine, LineMode
from data.models import Metro
import os
from data.database import get_session
from data.metro_operations import import_metros_from_csv, find_metro, clear_metros, get_all_metros


#region line creation

def print_cities(session, metros: list[Metro]):
    print(f"\nCities in database ({len(metros)} total):")
    for metro in metros:
        print(f" - {metro.name}: {metro.population:,} people at ({metro.latitude}, {metro.longitude})")



def get_metros_from_cli(session, num_metros: int) -> list[Metro]:
    metros: list[str] = []
    while len(metros) < num_metros:
        name = input(f"Enter metro #{len(metros)+1}: ")
        print(name)
        metro = find_metro(session, name, True)
        
        if metro:
            if metro not in metros:
                metros.append(metro.name)
                print(f"Added {metro.name}")
            else:
                print("Error: Metro already selected")
        else:
            print("Metro not found. Try again.")
    
    return metros



def create_line(metros: list[Metro], avg_speed: float, mode: LineMode):
    line: RailLine = RailLine(avg_speed, mode)
    line.cities = metros
    line.init_fitness_curve()
    line.init_city_pairs()
    line.init_segment_gravities()
    return line

#endregion



#region graph visualization
'''
def latlon_to_mercator(lat, lon):
    """Convert latitude/longitude to Mercator projection coordinates"""
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = lon_rad
    y = np.log(np.tan(np.pi/4 + lat_rad/2))
    return x, y



def graph_line(line: RailLine):
    city_x_positions: list[float] = []
    city_y_positions: list[float] = []
    city_populations: list[int] = []

    # Convert coordinates
    for city in line.cities:
        x, y = latlon_to_mercator(city.latitude, city.longitude)
        city_x_positions.append(x)
        city_y_positions.append(y)
        city_populations.append(city.population / 10000)
    
    # Plot connections
    for i in range(len(line.edge_gravities)):
        x1, y1 = latlon_to_mercator(line.cities[i].latitude, line.cities[i].longitude)
        x2, y2 = latlon_to_mercator(line.cities[i+1].latitude, line.cities[i+1].longitude)
        plt.plot([x1, x2], [y1, y2], 'r', linewidth = line.edge_gravities[i]/100, zorder = 1)
    
    plt.scatter(city_x_positions, city_y_positions, s = city_populations, zorder = 2)

    plt.gca().set_aspect('equal')
    plt.xticks([])
    plt.yticks([])

    plt.show()
'''
#endregion



#region premade corridors

def get_acela_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Boston")
    metros.append("Providence")
    metros.append("New Haven")
    metros.append("New York")
    metros.append("Philadelphia")
    metros.append("Baltimore")
    metros.append("Washington")
    return metros



def get_rust_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Boston")
    metros.append("Providence")
    metros.append("New Haven")
    metros.append("New York")
    metros.append("Philadelphia")
    metros.append("Harrisburg")
    metros.append("Pittsburgh")
    metros.append("Cleveland")
    metros.append("Toledo")
    metros.append("Chicago")
    metros.append("Milwaukee")
    metros.append("Madison")
    metros.append("Eau Claire")
    metros.append("Minneapolis")
    return metros



def get_rust_lite_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Boston")
    metros.append("Providence")
    metros.append("New York")
    metros.append("Philadelphia")
    metros.append("Pittsburgh")
    metros.append("Cleveland")
    metros.append("Chicago")
    metros.append("Milwaukee")
    metros.append("Minneapolis")
    return metros



def get_extended_acela_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Portland-South Portland ME")
    metros.append("Boston")
    metros.append("Providence")
    metros.append("New Haven")
    metros.append("New York")
    metros.append("Philadelphia")
    metros.append("Baltimore")
    metros.append("Washington")
    metros.append("Richmond")
    metros.append("Raleigh")
    metros.append("Greensboro")
    metros.append("Charlotte")
    metros.append("Columbia SC")
    metros.append("Augusta")
    metros.append("Atlanta")
    return metros



def get_california_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("San Francisco")
    metros.append("San Jose")
    metros.append("Gilroy")
    metros.append("Madera")
    metros.append("Fresno")
    metros.append("Tulare")
    metros.append("Bakersfield")
    metros.append("Lancaster")
    metros.append("Burbank")
    metros.append("Los Angeles")
    metros.append("Riverside")
    metros.append("San Diego")
    return metros



def get_australia_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Adelaide")
    metros.append("Melbourne")
    metros.append("Canberra")
    metros.append("Sydney")
    metros.append("Newcastle Aus")
    metros.append("Gold Coast")
    metros.append("Brisbane")
    return metros



def get_nz_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("wellington")
    metros.append("palmerston")
    metros.append("hamilton NZ")
    metros.append("Auckland")
    return metros



def get_hs2_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("London UK")
    metros.append("Birmingham UK")
    metros.append("Manchester")
    metros.append("Leeds")
    metros.append("Middlesbrough")
    metros.append("newcastle UK")
    metros.append("Edinburgh")
    metros.append("Glasgow")
    return metros



def get_iberia_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Lisbon")
    metros.append("Sevilla")
    metros.append("Cordoba")
    metros.append("Madrid")
    metros.append("Zaragoza")
    metros.append("Barcelona")
    return metros



def get_south_europe_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Lisbon")
    metros.append("Sevilla")
    metros.append("Cordoba")
    metros.append("Madrid")
    metros.append("Zaragoza")
    metros.append("Barcelona")
    metros.append("Montepelier")
    metros.append("Lyon")
    metros.append("Paris")
    metros.append("London UK")
    return metros



def get_shinkansen_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("Tokyo")
    metros.append("Shizuoka")
    metros.append("Hamamatsu")
    metros.append("Nagoya")
    metros.append("Kyoto")
    metros.append("Osaka")
    return metros



def get_california_lite_corridor() -> list[str]:
    metros: list[str] = []
    metros.append("San Francisco")
    metros.append("Fresno")
    metros.append("Bakersfield")
    metros.append("Los Angeles")
    return metros




def get_metros_from_names(session, inputs: list[str], debug: bool = False) -> list[Metro]:
    metros: list[Metro] = []
    for metro_name in inputs:
        metro: Metro = find_metro(session, metro_name, debug)
        if metro:
            metros.append(metro)
        else:
            return metros
    return metros

#endregion


def init_database(session):
    clear_metros(session)
    import_metros_from_csv(session, "csv/metros.csv")



def get_line(city_names: list[str], avg_speed: float, reinitialize_database: bool = False) -> RailLine:
    session = get_session()
    if reinitialize_database:
        init_database(session)
    selected_metros: list[Metro] = get_metros_from_names(session, city_names)
    if len(selected_metros) == len(city_names):
        line: RailLine = create_line(selected_metros, avg_speed, LineMode.HIGHSPEED)
        session.close()
        return line
    else:
        session.close()
        return line




if __name__ == "__main__":
    session = get_session()
    os.system('clear')
    line: RailLine = get_line(get_metros_from_cli(session, 3),200)
    session.close()
    if line:
        print(f"rail mode: {line.mode.value}  average speed (mph): {line.avg_speed}\n")
        print(line.to_string() + "\n")
        print(line.get_city_pair_info() + "\n")
    else:
        print("error: invalid cities")
