import subprocess, os, platform
from datetime import datetime

from enum import Enum

import tkinter as tk
from PIL import ImageTk, Image

from implementacni_ukol.rw_samplers.rws_metropolis_hasting import RWSMetropolisHasting
from implementacni_ukol.rw_samplers.rws_with_random_jumps import RWSRandomJumps
from implementacni_ukol.rw_samplers.rws_with_restarts import RWSRestarts
from implementacni_ukol.rw_samplers.rwsampler import RWSampler
from implementacni_ukol.rws_original_graph.random_walk_sampling_original_graph import OriginalGraph


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


loaded_original_filename = None
loaded_original_graph = None
insides = {}

def generate_form():
    fields = *(i.value for i in MenuFieldsEnum), "break"

    def run_sampling(entries):
        filename = str(insides["filename"].get())
        method = str(insides["method"].get())
        size = int(entries[MenuFieldsEnum.SIZE.value].get())
        probability = float(entries[MenuFieldsEnum.RANDOM_PROBABILITY.value].get())

        global loaded_original_filename, loaded_original_graph
        if filename == loaded_original_filename and isinstance(loaded_original_graph, OriginalGraph):
            original_graph = loaded_original_graph
        else:
            loaded_original_filename = filename
            original_graph = loaded_original_graph = OriginalGraph(filename=f"data/{filename}")

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

        end = datetime.now()
        seconds = (end-start).total_seconds()

        text.delete('1.0', tk.END)
        text.insert("end", f"Took {seconds} sec. to complete.\n")
        for graph in (original_graph, sampler):
            component_sizes = graph.get_component_sizes()
            number_of_components = len(list(filter(lambda x: x >= 2, component_sizes)))
            text.insert("end", f"{graph.name}:\n{number_of_components} component{'s' if number_of_components>1 else ''}\nbiggest component size: {max(component_sizes)}\n{len(list(filter(lambda x: x == 2, component_sizes)))} isolated nodes.\n{graph.nodes_count} nodes and {graph.edges_count} edges\n\n")

        open_file("images\\cumulative_degree_distribution.png")
        open_file("images\\degree_distribution.png")

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
    text = tk.Text(root, width=45, height=10)
    text.pack(side=tk.LEFT, padx=5, pady=5)
    b1 = tk.Button(root, text='Run',
                command=(lambda e=ents: run_sampling(e)))
    b1.pack(side=tk.LEFT, padx=0, pady=0)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=0, pady=0)

    return root