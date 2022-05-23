import subprocess, os, platform
from datetime import datetime

from enum import Enum

import tkinter as tk
from tkinter import ttk
from PIL import Image

from implementacni_ukol.samplers.rws_metropolis_hasting import RWSMetropolisHasting
from implementacni_ukol.samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.samplers.rws_with_restarts import RWSRestarts
from implementacni_ukol.samplers.rwsampler import RWSampler
from implementacni_ukol.graph.original import OriginalGraph


def open_file(filepath):
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


class MenuFieldsEnum(Enum):
    ORIGINAL_GRAPH_FILENAME = "Original graph filename"
    SIZE = "Sample size"
    METHOD = "Sample method"
    RANDOM_PROBABILITY = "Random probability"


class MethodNames(Enum):
    RWS = "Random Walk Sampling"
    RWJ = "Random Walk Sampling With Random Jump"
    RWR = "Random Walk Sampling With Restarts"
    MHRW = "Metropolis-Hasting Random Walk Sampling"


original_graph_data = {}
insides = {}


def generate_form():
    fields = *(i.value for i in MenuFieldsEnum), "break"

    def run_sampling(entries):
        global original_graph_data
        filename = str(insides["filename"].get())
        method = str(insides["method"].get())
        size = int(entries[MenuFieldsEnum.SIZE.value].get())
        probability = float(entries[MenuFieldsEnum.RANDOM_PROBABILITY.value].get())

        if filename == original_graph_data.get("filename") and isinstance(original_graph_data.get("graph"),
                                                                          OriginalGraph):
            original_graph = original_graph_data.get("graph")
        else:
            original_graph_data["filename"] = filename
            start = datetime.now()
            original_graph_data["graph"] = original_graph = OriginalGraph(filename=f"data/{filename}")
            end = datetime.now()
            original_graph_data["time"] = end - start

        start = datetime.now()
        sampler = None
        if method == MethodNames.RWS.value:
            sampler = RWSampler(original_graph)
        elif method == MethodNames.RWJ.value:
            sampler = RWSRandomJumps(original_graph, random_scenario_probability=probability)
        elif method == MethodNames.RWR.value:
            sampler = RWSRestarts(original_graph, random_scenario_probability=probability)
        elif method == MethodNames.MHRW.value:
            sampler = RWSMetropolisHasting(original_graph)

        sampler.random_walk(size)
        sampler.compare_distributions(original_graph, parameter="degree")
        sampler.compare_distributions(original_graph, parameter="degree", type_="cumulative")

        end = datetime.now()
        duration = end - start
        times = [original_graph_data["time"], duration]

        for index, graph in enumerate((original_graph, sampler)):
            component_sizes = graph.get_component_sizes()
            number_of_components = len(list(filter(lambda x: x >= 2, component_sizes)))
            number_of_isolated = len(list(filter(lambda x: x == 1, component_sizes)))

            for index2, data in enumerate((
                    graph.nodes_count,
                    graph.edges_count,
                    graph.average_degree,
                    graph.max_degree,
                    number_of_components,
                    number_of_isolated,
                    max(component_sizes),
                    "",
                    times[index].total_seconds()
            )):
                table.set(index2, index + 1, round(data, 4) if not isinstance(data, str) else "")

        image1 = Image.open(r"images/degree_distribution.png")
        image2 = Image.open(r"images/cumulative_degree_distribution.png")
        new_image = Image.new('RGB', (2 * image1.size[0], image1.size[1]), (255, 255, 255))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1.size[0], 0))
        new_image.show()


    def makeform(root, fields):
        entries = {}
        for field in fields:
            if field == "break":
                row = tk.Frame(root)
                lab = tk.Label(row, width=60, text="_" * 100, anchor='w')
                lab.pack(side=tk.LEFT)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                continue
            row = tk.Frame(root)
            lab = tk.Label(row, width=20, text=field, anchor='w')
            if field == MenuFieldsEnum.ORIGINAL_GRAPH_FILENAME.value:
                value_inside = tk.StringVar(row)
                options = os.listdir("data")
                value_inside.set(options[0])
                ent = tk.OptionMenu(row, value_inside, *options)
                insides["filename"] = value_inside
            elif field == MenuFieldsEnum.SIZE.value:
                ent = tk.Entry(row)
                ent.insert(0, "2000")
            elif field == MenuFieldsEnum.METHOD.value:
                value_inside = tk.StringVar(row)
                options = [
                    MethodNames.RWS.value,
                    MethodNames.RWJ.value,
                    MethodNames.RWR.value,
                    MethodNames.MHRW.value,
                ]
                value_inside.set(options[0])
                ent = tk.OptionMenu(row, value_inside, *options)
                insides["method"] = value_inside
            elif field == MenuFieldsEnum.RANDOM_PROBABILITY.value:
                ent = tk.Entry(row)
                ent.insert(0, "0.15")
            else:
                ent = tk.Entry(row)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field] = ent
        return entries

    root = tk.Tk()
    ents = makeform(root, fields)
    frame = tk.Frame(root)
    frame.pack()
    table = ttk.Treeview(frame)
    table["columns"] = ["Parameter", "Original", "Sample"]
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Parameter", anchor=tk.W, width=170)
    table.column("Original", anchor=tk.W, width=100)
    table.column("Sample", anchor=tk.W, width=100)
    table.heading("Parameter", text="Parameter", anchor=tk.W)
    table.heading("Original", text="Original", anchor=tk.W)
    table.heading("Sample", text="Sample", anchor=tk.W)
    table.insert(parent='', index='end', iid=0, text='',
                 values=('Number of nodes', '', ''))
    table.insert(parent='', index='end', iid=1, text='',
                 values=('Number of edges', '', ''))
    table.insert(parent='', index='end', iid=2, text='',
                 values=('Average degree', '', ''))
    table.insert(parent='', index='end', iid=3, text='',
                 values=('Maximm degree', '', ''))
    table.insert(parent='', index='end', iid=4, text='',
                 values=('Number of components', '', ''))
    table.insert(parent='', index='end', iid=5, text='',
                 values=('Number of isolated nodes', '', ''))
    table.insert(parent='', index='end', iid=6, text='',
                 values=('Biggest component size', '', ''))
    table.insert(parent='', index='end', iid=7, text='',
                 values=('', '', ''))
    table.insert(parent='', index='end', iid=8, text='',
                 values=('Processing time (s)', '', ''))

    table.pack()

    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.RIGHT, padx=5, pady=5)

    b1 = tk.Button(root, text='Run',
                   command=(lambda e=ents: run_sampling(e)))
    b1.pack(side=tk.RIGHT, padx=5, pady=5)

    return root
