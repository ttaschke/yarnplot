#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import requests
import time
import math

from datetime import datetime, timedelta
from threading import Timer
from Queue import Queue

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""
YarnPlot - Tool to collect timeline-based YARN application statistics
"""

def main():
    yp = YarnPlot()
    yp.main()

class YarnPlot(object):

    def main(self):
        parser = argparse.ArgumentParser(description='YarnPlot - Tool to collect timeline-based YARN application statistics')
        parser.add_argument('host', type=str, nargs='?',
                            help='Resourcemanager hostname')
        parser.add_argument('mode', type=str, nargs='?',
                            help='mode: list (displays running applications), app (tracks ')
        parser.add_argument('-app_id', type=str, nargs='?',
                            help='YARN application id. Required for app mode')
        parser.add_argument('-attributes', type=str, nargs='+', default=["allocatedVCores", "allocatedMB"],
                            help='YARN application attributes to track (e.g. -attributes allocatedVCores progress). See Yarn REST API documentation for full list')
        parser.add_argument('-sample_rate', type=int, nargs='?', default=1,
                            help='Sample rate in seconds (default: 1). High sample rates are recommend to ensure accuracy)')
        parser.add_argument('-output', type=str, nargs='?', default=".",
                            help='output mode (plot, csv')
        parser.add_argument('-output_folder', type=str, nargs='?', default=".",
                            help='Existing folder in which to save the output (default: current working directory)')
        self.args = parser.parse_args()

        self.base_url = "http://" + self.args.host + ":8088/ws/v1/"

        if(self.args.mode == 'list'):
            self.list_apps()
        elif(self.args.mode == 'app'):
            if not self.args.app_id:
                print("Application id is mandatory for mode app")
                sys.exit(1)
            self.q = Queue()
            self.track_history()
            self.save_output(self.q.get())

        return

    def list_apps(self):
        apps = self.get_apps()

        print("")
        if not apps:
            return
        for app in apps:
            print(app['id'] + " " + app['name'])

    def show_app(self):
        app = self.get_app(self.args.app_id)
        print(app['name'] + " " + str(app['progress']) + " " + str(app['runningContainers']))

    def get_app(self):
        r = requests.get(self.base_url + "cluster/apps/" + self.args.app_id)
        return r.json()['app']

    def get_apps(self, states="RUNNING"):
        r = requests.get(self.base_url + "cluster/apps/?states=" + states)
        if r.json()['apps'] is None:
            return None
        else:
            return r.json()['apps']['app']

    def save_output(self, data):
        df = pd.DataFrame(data)
        df.index = df['datetime']
        df = df.drop('datetime', 1)

        if(self.args.output == 'plot'):
            sns.set_style("darkgrid")
            df.plot(title=self.args.attributes, subplots=True, legend=False)
            plt.tight_layout()
            plt.savefig(self.args.output_folder + "/" + self.args.app_id + ".png", dpi=200)
            plt.close()

            print("")
            print("Saved plot to " + self.args.output_folder + "/" + self.args.app_id + ".png")

        elif(self.args.output == 'csv'):
            df.to_csv(self.args.output_folder + "/" + self.args.app_id + ".csv")
            print("")
            print("Saved csv to " + self.args.output_folder + "/" + self.args.app_id + ".csv")

    def trigger(self, data):
        app = self.get_app()

        data.setdefault('datetime',[]).append(datetime.now())

        for attr in self.args.attributes:
            data.setdefault(attr, []).append(app[attr])

        print(app['name'] + ", progress: " + str(app['progress']))

        if(app['state'] == 'FINISHED' or app['state'] == 'FAILED' or app['state'] == 'KILLED'):
            print("Application finished with state: " + app['state'])
            self.q.put(data)
            return

        self.track_history()

    def track_history(self, data={}):
        seconds = 0 if not data else self.args.sample_rate
        t = Timer(seconds, self.trigger, [data])
        t.start()
