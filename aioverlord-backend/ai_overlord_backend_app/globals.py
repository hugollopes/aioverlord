import json

with open("./static/referenceData/referenceData.json", encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

TOPOLOGIES = data["topologies"]

COST_PER_NEURON = data["costPerNeuron"]
