import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from parse.parse_generate import parse_args
from models import Models_functions
from utils import Utils_functions
import math
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

if __name__ == "__main__":

    # parse args
    args = parse_args()

    # initialize networks
    M = Models_functions(args)
    #M.download_networks()
    models_ls = M.get_networks()

    # test musika
    U = Utils_functions(args)
    #U.OSC_server(models_ls)

    sendip = "127.0.0.1"
    sendport = 1337

    client = SimpleUDPClient(sendip, sendport)  # Create client
    
    print(args)

    #args.update({'num_samples':2})
    #l_path= args["load_path"]
    generated_sample_name = "generated_sample.wav"

    def generate_handler(unused_addr, hargs, generate):
        print("generating from OSC...")
        #args.num_samples = generate

        #make loop with generate as variable
        for i in range(0, generate):
            print(i)
            # initialize networks
            M = Models_functions(args)
            models_ls = M.get_networks()
            U = Utils_functions(args)
            print(args)
            generated_sample_name=U.generate(models_ls)
            client.send_message("/finished", generated_sample_name)      

    def model_handler(unused_addr, hargs, model):
        print("changing model from OSC...")
        args.load_path = model
        # initialize networks
        #M = Models_functions(args)
        #models_ls = M.get_networks()
        #U = Utils_functions(args)
        print(args)
        client.send_message("/modelchanged", model)

    def trunc_handler(unused_addr, hargs, trunc):
        print("changing trunc from OSC...")
        args.truncation = trunc
        # initialize networks
        #M = Models_functions(args)
        #models_ls = M.get_networks()
        #U = Utils_functions(args)
        print(args)
        client.send_message("/truncchanged", trunc)

    dispatcher = Dispatcher()

    dispatcher.map("/generate", generate_handler, "Generate")
    dispatcher.map("/model", model_handler, "Model")
    dispatcher.map("/trunc", trunc_handler, "Trunc")
 
    server = osc_server.ThreadingOSCUDPServer(
        ("127.0.0.1", 7400), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
    
    #python musika_server.py --load_path /Users/espensommereide/Dropbox/Projects/BEK/DEEP_LEARNING_AUDIO/musika/models/oakdefault --num_samples 1 --seconds 120 --save_path /Users/espensommereide/Dropbox/Projects/BEK/DEEP_LEARNING_AUDIO/musika/generate_default

