"""
Synfirechain-like example
"""
#!/usr/bin/python
import os
import spynnaker.pyNN as p
import spynnaker_external_devices_plugin.pyNN as q
import numpy, pylab

p.setup(timestep=1.0, min_delay = 1.0, max_delay = 144.0)
nNeurons = 3 # number of neurons in each population
max_delay = 50



cell_params_lif = {'cm'        : 0.25, # nF
                     'i_offset'  : 0.0,
                     'tau_m'     : 20.0,
                     'tau_refrac': 2.0,
                     'tau_syn_E' : 5.0,
                     'tau_syn_I' : 5.0,
                     'v_reset'   : -70.0,
                     'v_rest'    : -65.0,
                     'v_thresh'  : -50.0
                     }

populations = list()
projections = list()

weight_to_spike = 2.0
delay = 3
delays = list()

loopConnections = list()
for i in range(0, nNeurons):
    delays.append(float(delay))
    singleConnection = (i, ((i + 1) % nNeurons), weight_to_spike, delay)
    loopConnections.append(singleConnection)

injectionConnection = [(0, 0, weight_to_spike, 1)]
spikeArray = {'spike_times': [[0]]}

populations.append(p.Population(nNeurons, p.IF_curr_exp, cell_params_lif, label='spikes_out'))

populations.append(p.Population(1, p.SpikeSourceArray, spikeArray, label='inputSpikes_1'))

projections.append(p.Projection(populations[0], populations[0], p.FromListConnector(loopConnections)))
projections.append(p.Projection(populations[1], populations[0], p.FromListConnector(injectionConnection)))

populations[0].record()
q.activate_live_output_for(populations[0])
#populations[0].set_constraint(p.PlacerChipAndCoreConstraint(0,0,2))
#populations[1].set_constraint(p.PlacerChipAndCoreConstraint(0,0,3))

run_time = 10
print "Running for {} ms".format(run_time)
p.run(run_time)

v = None
gsyn = None
spikes = None
spikes = populations[0].getSpikes(compatible_output=True)

print "The number of spikes in pop 0 is", len(spikes)

if spikes is not None:
    #print spikes
    pylab.figure()
    pylab.plot([i[1] for i in spikes], [i[0] for i in spikes], ".")
    pylab.ylabel('neuron id')
    pylab.xlabel('Time/ms')
    pylab.xlim(0,run_time)
    pylab.ylim(-1,2)
    pylab.title('spikes')
    pylab.show()
else:
    print "No spikes received"


p.end()
