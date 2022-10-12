import json
import argparse
import sys
import os
from pathlib import Path
import logging.config

from src.data.data_loader import DataLoader
from src.models.model_manager import ModelManager


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = Path(default_path)
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    # first set up the logging of the system
    setup_logging()
    parser = argparse.ArgumentParser(prog='StockPredictor',
                                     description='allows users to predict the stock market 5 days in advance.')
    parser.add_argument('command', help='the action you wish to perform (download, add, remove, predict)')
    parser.add_argument('--stock', help='the ticker of the stock you wish to use')
    args = parser.parse_args()

    if args.command == 'download':
        print('updating the database!')
        downloader = DataLoader()
        downloader.update()

    elif args.command == 'add':
        if args.stock == '':
            print('Wrong usage: enter a stock to add')
            return
        downloader = DataLoader()
        downloader.add_ticker(args.stock.upper())

    elif args.command == 'remove':
        if args.stock == '':
            print('Wrong usage: enter a stock to remove')
            return
        downloader = DataLoader()
        downloader.remove_ticker(args.stock.upper())

    elif args.command == 'predict':
        if args.stock == '':
            print('Wrong usage: enter a stock to predict on')
            return
        model_man = ModelManager(args.stock.upper())
        # create or load a model
        model_man.create_or_load_model()
        # save the model we created
        model_man.save_model()
        prediction, threshold = model_man.predict()
        with open('result.txt', 'w') as f:
            if prediction:
                f.write('%s will rise in five days!' % args.stock.upper())
            else:
                f.write('%s will fall in five days!' % args.stock.upper())


if __name__ == '__main__':
    main()


