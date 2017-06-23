#Author: Chris T.
#Editor: Dalisha R.
#Date recieved: 06/21/2017
#miner.py

#Invokes parser.py to grab stack traces 
#from the specified source

import argparse
import csv
import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from logger import *
from parser1 import Parser

def parse(service, url, start, stop, browser):
    results = list()

    if '{}' not in url:
        warning('URL does not have a placeholder for Crash_ID number.')

    try:
        parser = Parser(service, browser)
        parser.setup()

        header = parser.get_header()
        if header:
            results.append(header)

        index = 0
        with open('test.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter = ',')
            for row in readCSV:
                CrashID = row[0]
                print("CrashID: ")
                print(CrashID)
                results += parser.parse(CrashID, url.format(CrashID))
                #print(results)


    except KeyboardInterrupt:
        sys.stdout.write('\r')
        info('Exiting...')
    finally:
        parser.teardown()

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=(
                'Script to collect crash dump stack traces.'
            )
        )
    parser.add_argument(
            '-b', dest='browser', default='chrome',
            choices=['chrome'],
            help='The browser to use when retrieving the search results.'
        )
    parser.add_argument(
            '--start', dest='start', type=int, default=1,
            help='Index of the page of results to start parsing from.'
        )
    parser.add_argument(
            '--stop', dest='stop', type=int, default=1,
            help='Index of the page of results to stop parsing to.'
        )
    parser.add_argument(
            'service',
            choices=['fedora'],
            help=(
                'The crash dump stack trace source from which the results are to be parsed.'
            )
        )
    parser.add_argument(
            'url',
            help=(
                'The URL of the search results. Use {} as the placeholder for '
                'Crash_ID number.'
            )
        )
    parser.add_argument(
            'output', help=(
                'Path to the file to which the parse results should be '
                'written.'
            )
        )
    args = parser.parse_args()

    info('Parsing {}'.format(args.url))
    results = parse(
            args.service, args.url, args.start, args.stop, args.browser
        )
    if results:
        with open(args.output, 'w', newline='') as file_:
            writer = csv.writer(file_)
            # print("Writing new line...")
            # for row in results:
            #     print(row)
            #     writer.writerow(row)
            writer.writerows(results)
    info('Results written to {}'.format(args.output))
