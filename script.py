import json
import time
from sys import argv
from datetime import date
import requests
from rich import print as rprint
from args import Args
from tables import Tables

def dump(data_dump_file_path, update=False):
    if data_dump_file_path is None:
        data_dump_file_path = data_file

    if not data_dump_file_path.endswith(".json"):
        data_dump_file_path = f"{data_dump_file_path.strip()}.json"

    with open(data_dump_file_path, "w") as data_dump_file:
        json.dump(request_data, data_dump_file, indent=4)
        rprint(
            f"[underline green]Data written to {data_dump_file_path}[/underline green]"
        )
        if not update:
            exit()
        else:
            return

def check_for_local_small_changes(update: bool = False):
    if update:
        dump(None, update)
    try:
        with open(data_file) as local_data_file:
            local_data = json.load(local_data_file)
    except FileNotFoundError:
        rprint(
            "[red underline]WARNING: COULD NOT FIND DATA FILE![/red underline]\n[red underline]creating new...[/red underline]"
        )
        dump(None)
    local_date_year,local_date_month,local_date_day = epoch_to_human(local_data["Character"]["ParseDate"]).split("/")
    last_update = f"{local_date_day}/{local_date_month}/{local_date_year}"
    local_exp_data = local_data["Character"]["ClassJobs"]
    client_exp_data = request_data["Character"]["ClassJobs"]
    local_exp = [local_exp_dat["ExpLevel"] for local_exp_dat in local_exp_data]
    client_exp = [client_exp_dat["ExpLevel"] for client_exp_dat in client_exp_data]
    for i in range(len(client_exp)):
        if client_exp[i] != local_exp[i]:
            print(f"DATA IS OUT OF DATE!\n[LAST UPDATE: {last_update}]")
            print()
            update_data = input("Update? (Y/n): ").lower() or "y"
            if update_data == "y":
                dump(None)
            else:
                break


def check_local_file_date():
    day_limit = 5
    try:
        with open(data_file) as local_data_file:
            request_data = json.load(local_data_file)
    except FileNotFoundError:
        rprint(
            "[red underline]WARNING: COULD NOT FIND DATA FILE![/red underline]\n[red underline]creating new...[/red underline]"
        )
        dump(data_dump_file_path=args.dump)
    current_epoch_readable = epoch_to_human(time.time())
    current_epoch_datetime = str_to_datetime(current_epoch_readable)

    local_epoch = request_data["Character"]["ParseDate"]
    local_epoch_readable = epoch_to_human(local_epoch)
    local_epoch_datetime = str_to_datetime(local_epoch_readable)

    date_delta = current_epoch_datetime.day - local_epoch_datetime.day
    if date_delta >= day_limit:
        rprint(
            f"[yellow underline]NOTICE: LOCAL DATA IS {date_delta} DAYS OLD![/yellow underline]\n[yellow underline]use 'python {SCRIPT_NAME} --dump' to update local data"
        )
    data_dump_file_path = None
    return (data_dump_file_path, request_data)


def epoch_to_human(epoch):
    return time.strftime("%Y/%m/%d", time.localtime(epoch))


def str_to_datetime(date_str):
    int_date = date_str.split("/")
    return date(int(int_date[0]), int(int_date[1]), int(int_date[2]))


def current_job():
    return request_data["Character"]["ActiveClassJob"]["UnlockedState"]["Name"]


def character_details():
    char_data = request_data.get("Character")

    if char_data is None:
        rprint(f"[red underline]ID {args.id} could not be found![/red underline]")
        exit()
    
    rprint("[green underline]CHARACTER[/green underline]")
    server               = char_data["Server"]
    data_center          = char_data["DC"]

    char_name              = char_data["Name"]
    char_free_company      = char_data["FreeCompanyName"]
    char_bio               = char_data["Bio"]
    char_nameday           = char_data["Nameday"]
    char_gender            = char_data["Gender"]
    char_race              = char_data["Race"]
    char_job               = char_data["ActiveClassJob"]["UnlockedState"]["Name"]
    char_job_lvl           = char_data["ActiveClassJob"]["Level"]
    char_title,is_prefix   = tables.title(str(char_data["Title"]))
    char_grand_company     = char_data["GrandCompany"]
    char_achievement_score = request_data["Achievements"]["Points"]
    minions                = request_data["Minions"]
    mounts                 = request_data["Mounts"]
    title_name             = f"{char_title} {char_name}" if is_prefix == "True" else f"{char_name} {char_title}"
    SPACE = ""
    rprint(f"\t[underline]SERVER:[/underline]{SPACE:<6} {server}【{data_center}】")
    rprint(f"\t[underline]FREE COMPANY:[/underline] {char_free_company}")
    rprint(f"\t[underline]NAME:[/underline]{SPACE:<8} {title_name}")
    if char_bio != "-":
        rprint(f"\t[underline]BIO:[/underline] {char_bio}")
    rprint(f"\t{' '*2}[underline]GENDER/RACE:[/underline] lv {char_job_lvl} {tables.gender(char_gender)} {char_job} {tables.race(char_race)}")
    rprint(f"\t{' '*2}[underline]Name day:[/underline] {char_nameday}")
    rprint(f"\t{' '*2}[underline]Grand Company:[/underline] {tables.grandCompany(char_grand_company['NameID'])}")
    rprint(f"\t{' '*2}[underline]Achievement Score:[/underline] {char_achievement_score}")
    rprint(f"\t{' '*2}[underline]Minions:[/underline] {len(minions)}")
    rprint(f"\t{' '*2}[underline]Mounts:[/underline] {len(mounts)}")
    if args.verbose:
        minions_details()
        mounts_details()

def minions_details():
    rprint("[green underline]MINIONS[/green underline]")
    minions = request_data["Minions"]
    for minion in minions:
        print(f"\t{minion['Name']}")  

def mounts_details():
    rprint("[green underline]MOUNTS[/green underline]")
    minions = request_data["Mounts"]
    for minion in minions:
        print(f"\t{minion['Name']}")  


def job_stats():
    rprint("[green underline]JOBS[/green underline]")
    char_data = request_data["Character"]
    char_jobs = char_data["ClassJobs"]
    job_dict = {}
    for job in char_jobs:
        job_lvl = job["Level"]
        job_name = job["UnlockedState"]["Name"]
        job_exp = job["ExpLevel"]
        job_exp_left = job["ExpLevelTogo"]
        if job_lvl > 1:
            job_exp_percent = (
                round(job["ExpLevel"] / job["ExpLevelMax"] * 100, 2)
                if job["ExpLevel"] != 0
                else None
            )
            job_dict[job_name] = job_lvl
            if args.verbose:
                job_dict[job_name] = {
                    "LVL": job_lvl,
                    "Exp_Left": job_exp_left,
                    "Percent_Filled": job_exp_percent,
                    "Total_Exp": job_exp,
                }
    if not args.verbose:
        sorted_jobs = sorted(job_dict.items(), key=lambda x: x[1], reverse=True)
        for job, lvl in sorted_jobs:
            if job == current_job():
                rprint(f"\tLVL {lvl} [green underline]{job}[/green underline]")
            else:
                rprint(f"\tLVL {lvl} {job}")
    elif args.verbose:
        for job, lvl in job_dict.items():
            rprint(
                f'\tLVL {lvl["LVL"]} {job}\n\t\t[EXP LEFT: {job_exp_left} | {job_exp_percent}% filled | Total Exp: {job_exp}]'
            )

def debug():
    char_data = request_data["Character"]
    print(json.dumps(char_data,indent=4))
    

if __name__ == "__main__":
    args = Args().ff_args()
    SCRIPT_NAME = "ffxiv_data_getter.py"
    tables = Tables()
    ID = "45292506" if args.id is None else args.id
    data_file = f"{ID}.json" if args.id else "45292506.json"
    if not data_file.endswith(".json"):
        data_file = f"{data_file}.json"
    if not args.offline:
        URL = f"https://xivapi.com/character/{ID}?data=AC,FR,FC,FCM,PVP,MIMO"
        request_data = requests.get(URL, timeout=5).json()
    elif args.offline:
        data_dump_file_path, request_data = check_local_file_date()
    if not args.no_local: check_for_local_small_changes(args.update)

    if args.dump_path and "--dump" in argv or args.dump_path is None and "--dump" in argv:
        dump(data_dump_file_path=args.dump_path)

    character_details()
    if args.jobs:
        job_stats()
    if args.debug:
        debug()