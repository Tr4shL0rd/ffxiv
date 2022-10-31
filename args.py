import argparse

class Args:
    def __init__(self) -> None:
        pass

    def ff_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-v","--verbose",
            dest="verbose",
            action="store_true",
            help="verbose output"
        )
        parser.add_argument(
            "-j","--jobs",
            dest="jobs",
            action="store_true",
            help="shows jobs"
        )
        parser.add_argument(
            "--dump",
            dest="dump",
            default="data.json",
            nargs="?",
            help="dumps a json file containing all request data"
        )
        parser.add_argument(
            "--offline",
            dest="offline",
            action="store_true",
            help="uses local data"
        )
        parser.add_argument(
            "--update","-u",
            dest="update",
            action="store_true",
            help="updates local data file"
        )
        parser.add_argument(
            "--id",
            dest="id",
            action="store",
            help="Your lodestone character ID"
        )
        parser.add_argument(
            "--no-local",
            dest="no_local",
            action="store_true",
            help="flag for not creating the data file"
        )
        args = parser.parse_args()
        return args