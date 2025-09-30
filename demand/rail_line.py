from itertools import combinations
import numpy as np
from data.models import Metro
from enum import Enum
from scipy.interpolate import interp1d
from geopy.distance import geodesic
from data.metro_operations import (
    get_simplified_name
)


class LineMode(Enum):
    CONVENTIONAL = "Conventional"
    SEMIHIGHSPEED = "Semi High-Speed"
    HIGHSPEED = "High-Speed"


class RailLine:

    #region initialization

    def __init__(self, avg_speed: float, mode: LineMode):
        self.cities: list[Metro] = []
        self.city_pairs: list[tuple[Metro, Metro]] = []
        self.avg_speed: float = avg_speed
        self.edge_gravities: list[float] = []
        self.mode: LineMode = mode
        self.fitness_curve: interp1d
    


    def init_city_pairs(self):
       self.city_pairs = list(combinations(self.cities, 2))
    


    def init_fitness_curve(self, method = 'linear'):
        plane_time_offset = 3
        rail_time_offest = 0.5
        plane_speed = 440
        upper_limit: float = round(-(plane_time_offset - rail_time_offest) / (1 / plane_speed - 1 / self.avg_speed),1)
        print(f"upper distance limit: {upper_limit}")
        match self.mode:
            case LineMode.CONVENTIONAL:
                x_points = [0,25,100,upper_limit,100000]
                y_points = [0,0, 1, 0,0]
            case LineMode.SEMIHIGHSPEED:
                x_points = [0,35,170,upper_limit,100000]
                y_points = [0,0, 1, 0,0]
            case LineMode.HIGHSPEED:
                x_points = [0,50,250,upper_limit,100000]
                y_points = [0,0, 1, 0,0]

        fitness_curve = interp1d(np.array(x_points), np.array(y_points),
                                kind=method, bounds_error=False, fill_value='extrapolate')
        
        self.fitness_curve = fitness_curve
    


    def init_segment_gravities(self):
        if len(self.cities) <= 1:
            print("not enough cities in line to calculate gravity.")
        else:
            #initializes edge gravities to zero
            for i in range(len(self.cities) - 1):
                self.edge_gravities.append(0)
            
            for pair in self.city_pairs:
                index_1: int = self.cities.index(pair[0])
                index_2: int = self.cities.index(pair[1])
                start_index: int = min(index_1, index_2)
                end_index: int = max(index_1, index_2)

                for i in range(start_index, end_index):
                    self.edge_gravities[i] += self.calculate_gravity(pair[0], pair[1])
                    
    #endregion



    #region gravity calculation

    def distance_on_line(self, city_1: Metro, city_2: Metro) -> float:
        distance: float = 0

        index_1: int = self.cities.index(city_1)
        index_2: int = self.cities.index(city_2)
        start_index: int = min(index_1, index_2)
        end_index: int = max(index_1, index_2)

        for i in range(start_index, end_index):
            city_1_location: tuple[float, float] = (self.cities[i].latitude, self.cities[i].longitude)
            city_2_location: tuple[float, float] = (self.cities[i+1].latitude, self.cities[i+1].longitude)
            distance += geodesic(city_1_location, city_2_location).miles
        
        return distance
    


    def calculate_gravity(self, city_1: Metro, city_2: Metro) -> float:
        numerator: float = city_1.population * city_2.population
        distance: float = self.distance_on_line(city_1, city_2) #in miles
        travel_time: float = distance / self.avg_speed #in hours
        denominator: float = pow(travel_time, 2)
        if denominator == 0:
            print(f"travel time is zero between {get_simplified_name(city_1.name)} and {get_simplified_name(city_2.name)}")
        return round(1e-11 * self.fitness_curve(distance) * numerator / denominator)

    #endregion



    #region console display

    def to_string(self) -> str:
        line_str: str = ""
        for i in range(len(self.cities)):
            line_str += get_simplified_name(self.cities[i].name)
            if i != len(self.cities) - 1:
                line_str += " - "
                line_str += str(self.edge_gravities[i])  # Convert to string if it's not already
                line_str += " - "
        return line_str
    


    def get_city_pair_info(self, gravity_percent_threshold: float = 0) -> str:
        city_pairs_to_gravity: dict[tuple[Metro, Metro], float] = {}

        for pair in self.city_pairs:
            city_pairs_to_gravity[pair] = self.calculate_gravity(pair[0], pair[1])

        #sorts the city pairs by gravity decreasing
        city_pairs_to_gravity = dict(sorted(city_pairs_to_gravity.items(), key=lambda x: x[1], reverse=True))
        total_line_gravity: float = round(sum(city_pairs_to_gravity.values()))

        result_lines = []

        for key in city_pairs_to_gravity.keys():
            gravity_percent = city_pairs_to_gravity[key] / total_line_gravity
            if gravity_percent < gravity_percent_threshold:
                break

            city_pair_str = f"{get_simplified_name(key[0].name)} - {get_simplified_name(key[1].name)}"
            percentage_str = f"{round(100 * gravity_percent, 1)}%"

            line = f"city pair: {city_pair_str:<35} gravity: {city_pairs_to_gravity[key]:<7} total gravity percentage: {percentage_str:<8}  distance: {round(self.distance_on_line(key[0], key[1]))}"
            result_lines.append(line)

        result_lines.append(f"\ntotal line gravity: {total_line_gravity}")

        return "\n".join(result_lines)