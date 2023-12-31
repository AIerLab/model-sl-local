import socket

from data import CifarData
from expose import Server
from splitlearn import SplitClient
import torch.nn as nn

from model import SplitClientModel, IdentityMappingModule
from splitlearn import SplitSocket

layer_num = 28

if __name__ == '__main__':
    # run in separate terminal
    # CLIENT_DIR = "../tmp/client/c01"
    CLIENT_DIR = "../tmp/client/c02"
    # CLIENT_DIR = "../tmp/client/c01"

    # model_layers = nn.ModuleList([])
    # model_layers = nn.ModuleList([nn.Identity() for layer_id in range(0)]) # TODO change the number of split layers
    model_layers = nn.ModuleList([IdentityMappingModule(
        4096, 4096) for layer_id in range(5)])  # TODO change the number of split layers
    # model_layers = nn.ModuleList([nn.Linear(in_features=4096, out_features=4096, bias=True) for layer_id in range(4)])

    # Init data, socket and model.
    client = SplitSocket(socket.gethostbyname("localhost"), 10086)
    model = SplitClientModel(model_layers, client, CLIENT_DIR).half()

    print("Welcome to the ChatGLM-6B model. Type your message.")
    while True:
        try:
            query = input("\nUser: ").strip()
            if query == "stop":
                model.stop()  # TODO
                break
            elif query == "clear":
                model.clear()  # TODO
                print("Chat history cleared.")
            else:
                response = model.process(query)
                print(response)
        except:
            print("Error")

    # # FIXME for server use
    # server = Server(model.process)
    # server.run("localhost", 8080)
