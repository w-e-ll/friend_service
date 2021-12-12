incoming_heroes_list = [
    {"name": "Thor", "status": "alive", "power": 90, "goal": "good"},
    {"name": "Wasp", "status": "alive", "power": 80, "goal": "bad"},
    {"name": "Hulk", "status": "alive", "power": 40, "goal": "good"},
    {"name": "AntMan", "status": "alive", "power": 100, "goal": "bad"},
    {"name": "Kargo", "status": "alive", "power": 70, "goal": "good"},
    {"name": "Dandi", "status": "alive", "power": 60, "goal": "good"},
    {"name": "Mindy", "status": "alive", "power": 50, "goal": "good"},
    {"name": "Tina", "status": "alive", "power": 70, "goal": "bad"},
    {"name": "Ivan", "status": "alive", "power": 90, "goal": "bad"},
    {"name": "Denys", "status": "alive", "power": 50, "goal": "bad"},
    {"name": "Toma", "status": "alive", "power": 50, "goal": "bad"},
    {"name": "Grisha", "status": "alive", "power": 50, "goal": "bad"},
    {"name": "Den", "status": "alive", "power": 50, "goal": "bad"},
]


class Hero:
    """
    Describes a hero, his main attributes
    """
    def __init__(self, properties):
        self.name = properties["name"]
        self.status = properties["status"]
        self.power = properties["power"]
        self.goal = properties["goal"]

    @staticmethod
    def power_level(hero_acting: int, hero_resting: int) -> bool:
        # checks who is stronger
        return hero_acting > hero_resting

    @staticmethod
    def attack(hero_acting: int, hero_resting: int) -> dict:
        # makes an attack, counts power and based on power updates hero status
        new_resting_power = hero_resting - hero_acting
        new_resting_status = "dead" if new_resting_power <= 0 else "injured"
        return {"new_power": new_resting_power, "new_status": new_resting_status}

    @staticmethod
    def attack_back(hero_acting: int, hero_resting: int) -> dict:
        # gives back to acting hero, counts power and based on power updates hero status
        new_acting_power = hero_acting - hero_resting
        new_acting_status = "dead" if new_acting_power <= 0 else "injured"
        return {"new_power": new_acting_power, "new_status": new_acting_status}


class Squad:
    """
    Describes a squad.
    IF a hero has a bad goal he will join resting squad.
    IF hero has a good goal he will join in_action squad.
    """
    def __init__(self, squad_name: str, squad_status: str):
        self.squad_name = squad_name
        self.squad_status = squad_status
        self.squad_resting = []
        self.squad_in_action = []

    def create_squad_resting(self, heroes):
        for hero in heroes:
            if hero["goal"] == "bad":
                self.squad_resting.append(hero)
        return self.squad_resting

    def create_squad_in_action(self, heroes):
        for hero in heroes:
            if hero["goal"] == "good":
                self.squad_in_action.append(hero)
        return self.squad_in_action


class SquadService:
    """
    Main service which describes the fight.
    Service checks who is stronger based on power level of a heroes.
    Provides main functions to heroes:
    - attack, attack back, start the fight
    """
    @staticmethod
    def start_the_fight(friends, avengers):
        # fight process, while we have friends
        can_fight = True
        count = 0
        while can_fight:

            if count == len(avengers):
                can_fight = False
                break

            for f_hero in friends:
                if f_hero.get("status") != "dead":
                    if f_hero.get("status") == "dead":
                        continue
                    friend = f_hero
                    print("friend :", friend)

                    for a_hero in avengers:
                        if a_hero.get("status") != "dead":
                            if friend.get("status") == "dead":
                                break
                            avenger = a_hero
                            print("avenger :", avenger)

                            eq = Hero.power_level(friend["power"], avenger["power"])
                            print("friend is able to beat avenger? ", eq)

                            if eq is True and avenger.get("status") != "dead":
                                print("friend makes attack")
                                damaged_hero = Hero.attack(friend.get("power"), avenger.get("power"))
                                avenger["power"] = damaged_hero.get("new_power")
                                avenger["status"] = damaged_hero.get("new_status")

                                print("avenger was killed by a friend: ", avenger)
                                if avenger.get("status") == "dead":
                                    count += 1
                                    break

                            elif eq is False and avenger.get("status") != "dead":
                                while friend.get("status") != "dead" or avenger.get("status") != "dead":
                                    print("avenger is stronger, but friend knows if he will beat first, he will win this battle")
                                    damaged_hero = Hero.attack(friend.get("power"), avenger.get("power"))
                                    avenger["power"] = damaged_hero.get("new_power")
                                    avenger["status"] = damaged_hero.get("new_status")
                                    print("damaged_avenger: ", damaged_hero)

                                    if avenger.get("status") == "dead":
                                        count += 1
                                        break

                                    damaged_acting_hero = Hero.attack_back(friend.get("power"), avenger.get("power"))
                                    friend["power"] = damaged_acting_hero.get("new_power")
                                    friend["status"] = damaged_acting_hero.get("new_status")

                                    if friend.get("status") == "dead":
                                        break
                        else:
                            continue

        print("All Avengers are dead")
        print("Friends WIN")


class Main:
    """
    Provides main steps to achieve goal:
    - create heroes
    - create friends squad
    - create avengers squad
    - initialize squad service
    - start the fight
    """
    def __init__(self, f_squad_name: str, f_squad_status: str, a_squad_name: str, a_squad_status: str):
        self.f_squad_name = f_squad_name
        self.f_squad_status = f_squad_status
        self.a_squad_name = a_squad_name
        self.a_squad_status = a_squad_status

        self.heroes = self.create_heroes(incoming_heroes_list)
        self.friends = self.create_friends_squad(self.f_squad_name, self.f_squad_status, self.heroes)
        self.avengers = self.create_avengers_squad(self.a_squad_name, self.a_squad_status, self.heroes)
        self.squad_service = self.init_squad_service()
        self.beat_them_all(self.squad_service, self.friends, self.avengers)

    @staticmethod
    def create_heroes(heroes) -> list:
        # initializes heroes from given incoming heroes list
        heroes_list = []
        for hero in heroes:
            hero = Hero(hero)
            heroes_list.append(hero.__dict__)
        return heroes_list

    @staticmethod
    def create_avengers_squad(a_squad_name: str, a_squad_status: str, heroes):
        # creates avengers squad
        avengers = Squad(a_squad_name, a_squad_status)
        avengers.create_squad_resting(heroes)
        return avengers

    @staticmethod
    def create_friends_squad(f_squad_name: str, f_squad_status: str, heroes):
        # creates friends squad
        friends = Squad(f_squad_name, f_squad_status)
        friends.create_squad_in_action(heroes)
        return friends

    @staticmethod
    def init_squad_service() -> SquadService:
        # initializes Squad Service
        s = SquadService()
        return s

    @staticmethod
    def beat_them_all(squad_service: SquadService, friends, avengers):
        # starts the fight
        squad_service.start_the_fight(friends.squad_in_action, avengers.squad_resting)


if __name__ == '__main__':
    m = Main(f_squad_name="The Friends", f_squad_status="in-action", a_squad_name="The Avengers",
             a_squad_status="resting")

