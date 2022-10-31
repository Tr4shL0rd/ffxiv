import csv


class Tables:
    def __init__(self) -> None:
        pass
    def gender(self,gender):
        genders = {
            1: "Male",
            2: "Female",
        }
        #if genders.get(gender) is None:
        #    return f"ID {gender} is not a valid gender ID"
        return genders.get(gender) if gender < len(genders)+1 else "Other"

    def race(self,race):
        races = {
            1: "Hyur",
            2: "Elezen",
            3: "Lalafell",
            4: "Miqo'te",
            5: "Roehadyn",
            6: "Au Ra",
            7: "Hrothgar",
            8: "Viera"
        }
        #if races.get(race) is None:
        #    return f"ID {race} is not a valid race ID"
        return races.get(race) if race < len(races)+1 else "Other"
    def job(self,job):
        jobs = {
            0:"adventurer",
            1:"gladiator",
            2:"pugilist",
            3:"marauder",
            4:"lancer",
            5:"archer",
            6:"conjurer",
            7:"thaumaturge",
            8:"carpenter",
            9:"blacksmith",
            10:"armorer",
            11:"goldsmith",
            12:"leatherworker",
            13:"weaver",
            14:"alchemist",
            15:"culinarian",
            16:"miner",
            17:"botanist",
            18:"fisher",
            19:"paladin",
            20:"monk",
            21:"warrior",
            22:"dragoon",
            23:"bard",
            24:"white mage",
            25:"black mage",
            26:"arcanist",
            27:"summoner",
            28:"scholar",
            29:"rogue",
            30:"ninja",
            31:"machinist",
            32:"dark knight",
            33:"astrologian",
            34:"samurai",
            35:"red mage",
            36:"blue mage",
            37:"gunbreaker",
            38:"dancer",
            39:"reaper",
            40:"sage"
        }
        return jobs.get(job) if job < len(jobs)+1 else "Other" 
    def title(self,titleID):
        with open("titles.csv", "r") as titles:
            reader = csv.reader(titles)
            for col in reader:
                if col[0] == titleID:
                    return (col[1],col[2])

    def grandCompany(self,gcID):
        companies = {
            0:"None",             
            1:"Maelstrom",
            2:"Order of the Twin Adder",
            3:"Immortal Flames",        
        }
        return companies.get(gcID) if gcID < len(companies)+1 else "Other"


