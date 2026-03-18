"""Pre-built board layout for standard US Monopoly."""

from .property import Property
from .space import Space, SpaceColor, SpaceType
from .title_deed import TitleDeed


def get_board_spaces() -> list[Space]:
    """Return list of 40 spaces in order around the board."""
    return [
        # Corner 1: GO
        Space(id="go", name="GO", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        
        # Brown properties
        Property(
            id="med_ave",
            name="Mediterranean Avenue",
            color=SpaceColor.BROWN,
            type=SpaceType.PROPERTY,
            purchase_price=60,
            base_rent=2,
            house_cost=50,
            house_rents=[10, 30, 90, 160, 250],
            mortgage_value=30,
        ),
        Space(id="community_chest_1", name="Community Chest", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        Property(
            id="baltic_ave",
            name="Baltic Avenue",
            color=SpaceColor.BROWN,
            type=SpaceType.PROPERTY,
            purchase_price=40,
            base_rent=2,
            house_cost=50,
            house_rents=[10, 30, 90, 160, 250],
            mortgage_value=20,
        ),
        Space(id="income_tax", name="Income Tax", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        
        # Station 1
        TitleDeed(
            id="reading_rr",
            name="Reading Railroad",
            color=SpaceColor.NONE,
            type=SpaceType.STATION,
            purchase_price=200,
            base_rent=25,
            mortgage_value=100,
        ),
        
        # Light Blue properties
        Property(
            id="oriental_ave",
            name="Oriental Avenue",
            color=SpaceColor.LIGHT_BLUE,
            type=SpaceType.PROPERTY,
            purchase_price=100,
            base_rent=6,
            house_cost=50,
            house_rents=[30, 90, 270, 400, 550],
            mortgage_value=50,
        ),
        Space(id="chance_1", name="Chance", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        Property(
            id="vermont_ave",
            name="Vermont Avenue",
            color=SpaceColor.LIGHT_BLUE,
            type=SpaceType.PROPERTY,
            purchase_price=100,
            base_rent=6,
            house_cost=50,
            house_rents=[30, 90, 270, 400, 550],
            mortgage_value=50,
        ),
        Property(
            id="connecticut_ave",
            name="Connecticut Avenue",
            color=SpaceColor.LIGHT_BLUE,
            type=SpaceType.PROPERTY,
            purchase_price=120,
            base_rent=8,
            house_cost=50,
            house_rents=[40, 120, 360, 500, 600],
            mortgage_value=60,
        ),
        
        # Corner 2: Jail
        Space(id="jail", name="Jail", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        
        # Pink properties
        Property(
            id="st_charles",
            name="St. Charles Place",
            color=SpaceColor.PINK,
            type=SpaceType.PROPERTY,
            purchase_price=140,
            base_rent=10,
            house_cost=100,
            house_rents=[30, 90, 270, 400, 550],
            mortgage_value=70,
        ),
        
        # Utility 1
        TitleDeed(
            id="electric_company",
            name="Electric Company",
            color=SpaceColor.NONE,
            type=SpaceType.UTILITY,
            purchase_price=150,
            base_rent=12,
            mortgage_value=75,
        ),
        
        Property(
            id="states_ave",
            name="States Avenue",
            color=SpaceColor.PINK,
            type=SpaceType.PROPERTY,
            purchase_price=150,
            base_rent=12,
            house_cost=100,
            house_rents=[30, 90, 270, 400, 550],
            mortgage_value=75,
        ),
        Property(
            id="virginia_ave",
            name="Virginia Avenue",
            color=SpaceColor.PINK,
            type=SpaceType.PROPERTY,
            purchase_price=160,
            base_rent=14,
            house_cost=100,
            house_rents=[40, 120, 360, 500, 600],
            mortgage_value=80,
        ),
        
        # Station 2
        TitleDeed(
            id="pennsylvania_rr",
            name="Pennsylvania Railroad",
            color=SpaceColor.NONE,
            type=SpaceType.STATION,
            purchase_price=200,
            base_rent=25,
            mortgage_value=100,
        ),
        
        # Orange properties
        Property(
            id="st_james",
            name="St. James Place",
            color=SpaceColor.ORANGE,
            type=SpaceType.PROPERTY,
            purchase_price=180,
            base_rent=16,
            house_cost=100,
            house_rents=[50, 150, 450, 625, 750],
            mortgage_value=90,
        ),
        Space(id="community_chest_2", name="Community Chest", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        Property(
            id="tennessee_ave",
            name="Tennessee Avenue",
            color=SpaceColor.ORANGE,
            type=SpaceType.PROPERTY,
            purchase_price=190,
            base_rent=18,
            house_cost=100,
            house_rents=[50, 150, 450, 625, 750],
            mortgage_value=95,
        ),
        Property(
            id="new_york_ave",
            name="New York Avenue",
            color=SpaceColor.ORANGE,
            type=SpaceType.PROPERTY,
            purchase_price=200,
            base_rent=20,
            house_cost=100,
            house_rents=[60, 180, 500, 700, 900],
            mortgage_value=100,
        ),
        
        # Corner 3: Free Parking
        Space(id="free_parking", name="Free Parking", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        
        # Red properties
        Property(
            id="kentucky_ave",
            name="Kentucky Avenue",
            color=SpaceColor.RED,
            type=SpaceType.PROPERTY,
            purchase_price=220,
            base_rent=22,
            house_cost=150,
            house_rents=[70, 200, 550, 750, 950],
            mortgage_value=110,
        ),
        Space(id="chance_2", name="Chance", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        Property(
            id="indiana_ave",
            name="Indiana Avenue",
            color=SpaceColor.RED,
            type=SpaceType.PROPERTY,
            purchase_price=220,
            base_rent=22,
            house_cost=150,
            house_rents=[70, 200, 550, 750, 950],
            mortgage_value=110,
        ),
        Property(
            id="illinois_ave",
            name="Illinois Avenue",
            color=SpaceColor.RED,
            type=SpaceType.PROPERTY,
            purchase_price=240,
            base_rent=24,
            house_cost=150,
            house_rents=[80, 220, 600, 800, 1000],
            mortgage_value=120,
        ),
        
        # Station 3
        TitleDeed(
            id="bo_railroad",
            name="B&O Railroad",
            color=SpaceColor.NONE,
            type=SpaceType.STATION,
            purchase_price=200,
            base_rent=25,
            mortgage_value=100,
        ),
        
        # Yellow properties
        Property(
            id="atlantic_ave",
            name="Atlantic Avenue",
            color=SpaceColor.YELLOW,
            type=SpaceType.PROPERTY,
            purchase_price=260,
            base_rent=26,
            house_cost=150,
            house_rents=[90, 250, 700, 875, 1050],
            mortgage_value=130,
        ),
        Property(
            id="ventnor_ave",
            name="Ventnor Avenue",
            color=SpaceColor.YELLOW,
            type=SpaceType.PROPERTY,
            purchase_price=260,
            base_rent=26,
            house_cost=150,
            house_rents=[90, 250, 700, 875, 1050],
            mortgage_value=130,
        ),
        
        # Utility 2
        TitleDeed(
            id="water_works",
            name="Water Works",
            color=SpaceColor.NONE,
            type=SpaceType.UTILITY,
            purchase_price=150,
            base_rent=12,
            mortgage_value=75,
        ),
        
        Property(
            id="marvin_gardens",
            name="Marvin Gardens",
            color=SpaceColor.YELLOW,
            type=SpaceType.PROPERTY,
            purchase_price=280,
            base_rent=28,
            house_cost=150,
            house_rents=[100, 300, 750, 925, 1100],
            mortgage_value=140,
        ),
        
        # Corner 4: Go to Jail
        Space(id="go_to_jail", name="Go to Jail", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        
        # Green properties
        Property(
            id="pacific_ave",
            name="Pacific Avenue",
            color=SpaceColor.GREEN,
            type=SpaceType.PROPERTY,
            purchase_price=300,
            base_rent=30,
            house_cost=200,
            house_rents=[110, 330, 800, 975, 1150],
            mortgage_value=150,
        ),
        Property(
            id="north_carolina_ave",
            name="North Carolina Avenue",
            color=SpaceColor.GREEN,
            type=SpaceType.PROPERTY,
            purchase_price=300,
            base_rent=30,
            house_cost=200,
            house_rents=[110, 330, 800, 975, 1150],
            mortgage_value=150,
        ),
        Space(id="community_chest_3", name="Community Chest", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        Property(
            id="pennsylvania_ave",
            name="Pennsylvania Avenue",
            color=SpaceColor.GREEN,
            type=SpaceType.PROPERTY,
            purchase_price=320,
            base_rent=32,
            house_cost=200,
            house_rents=[120, 360, 850, 1025, 1200],
            mortgage_value=160,
        ),
        
        # Station 4
        TitleDeed(
            id="short_line",
            name="Short Line",
            color=SpaceColor.NONE,
            type=SpaceType.STATION,
            purchase_price=200,
            base_rent=25,
            mortgage_value=100,
        ),
        
        Space(id="chance_3", name="Chance", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        
        # Dark Blue properties
        Property(
            id="park_place",
            name="Park Place",
            color=SpaceColor.DARK_BLUE,
            type=SpaceType.PROPERTY,
            purchase_price=350,
            base_rent=35,
            house_cost=200,
            house_rents=[150, 450, 1000, 1200, 1400],
            mortgage_value=175,
        ),
        Space(id="luxury_tax", name="Luxury Tax", color=SpaceColor.NONE, type=SpaceType.SPECIAL),
        Property(
            id="boardwalk",
            name="Boardwalk",
            color=SpaceColor.DARK_BLUE,
            type=SpaceType.PROPERTY,
            purchase_price=400,
            base_rent=50,
            house_cost=200,
            house_rents=[200, 600, 1400, 1700, 2000],
            mortgage_value=200,
        ),
    ]
