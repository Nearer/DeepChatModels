#!/usr/bin/env python3
"""This shows how to run the new dynamic models (work in progress)."""
from chatbot import DynamicBot, ChatBot, SimpleBot
from data import Cornell, Ubuntu, WMT, Reddit, TestData
from utils import io_utils
import sys, getopt
from pydoc import locate


def start_training(dataset, bot):
    """Train bot. Will expand this function later to aid interactivity/updates. Maybe."""
    print("Training bot. CTRL-C to stop training.")
    bot.train(dataset)


def start_chatting(bot):
    """Talk to bot. Will add teacher mode soon. Old implementation in _decode.py."""
    print("Initiating chat session.")
    print("Your bot has a temperature of %.2f." % bot.temperature, end=" ")
    if bot.temperature < 0.1:
        print("Not very adventurous, are we?")
    elif bot.temperature < 0.7:
        print("This should be interesting . . . ")
    else:
        print("Enjoy your gibberish!")
    bot.chat()


def main(argv):

    config_path = None

    # Extract config dictionaries from file path.
    try:
        opts, args = getopt.getopt(argv, "h:c:", ["config="])
    except getopt.GetoptError:
        print("ERROR: Please pass in the config file path. "
              "For example: ./main.py -c configs/my_config.yml")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('./main.py [options], where\n'
                  'Options:\n'
                  '\t-c [--config] <path-to-config-file>')
            sys.exit()
        elif opt in ("-c", "--config"):
            config_path = arg
    assert config_path is not None, "Config path not found."

    configs = io_utils.parse_config(config_path)
    # TODO: none of these checks should be in main,
    # and default params should be set if not found.
    model_name      = configs['model']
    dataset_name    = configs['dataset']
    dataset_params  = configs['dataset_params']
    model_params    = configs['model_params']

    print("Setting up %s dataset." % dataset_name)
    dataset = locate(dataset_name)(dataset_params)
    print("Creating", model_name, ". . . ")
    bot = locate(model_name)(dataset, model_params)

    if not model_params['decode']:
        start_training(dataset, bot)
    else:
        start_chatting(bot)

if __name__ == "__main__":
    main(sys.argv[1:])

