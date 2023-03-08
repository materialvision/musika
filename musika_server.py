import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from parse.parse_generate import parse_args
from models import Models_functions
from utils import Utils_functions
import math
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

if __name__ == "__main__":

    # parse args
    args = parse_args()

    # initialize networks
    M = Models_functions(args)
    M.download_networks()
    models_ls = M.get_networks()

    # test musika
    U = Utils_functions(args)
    #U.OSC_server(models_ls)


    def generate_handler(unused_addr, args, generate):
        print("generating from OSC...")
        U.generate(models_ls)
        print("finished to OSC")


    def print_compute_handler(unused_addr, args, volume):
        try:
            print("[{0}] ~ {1}".format(args[0], args[1](volume)))
        except ValueError:
            pass


    dispatcher = Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/generate", generate_handler, "Generate")
    dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 7400), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
