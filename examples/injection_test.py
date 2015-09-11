import spynnaker.pyNN as Frontend
import spynnaker_external_devices_plugin.pyNN as ExternalDevices
import pylab

Frontend.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)

nNeurons = 256
run_time = 5000

cell_params_lif = {'cm'        : 0.25,  # nF
                   'i_offset'  : 0.0,
                   'tau_m'     : 20.0,
                   'tau_refrac': 2.0,
                   'tau_syn_E' : 5.0,
                   'tau_syn_I' : 5.0,
                   'v_reset'   : -70.0,
                   'v_rest'    : -65.0,
                   'v_thresh'  : -50.0
                  }


cell_params_spike_injector = {

    # The port on which the spiNNaker machine should listen for packets.
    # Packets to be injected should be sent to this port on the spiNNaker
    # machine
    'port': 12346
}



populations = list()
projections = list()

weight_to_spike = 2.0

populations.append(Frontend.Population(nNeurons, Frontend.IF_curr_exp,
                                       cell_params_lif, label='spikes_out'))

populations.append(Frontend.Population(nNeurons,
                            ExternalDevices.SpikeInjector,
                            cell_params_spike_injector,
                            label='spikes_in'))

populations[0].record()
ExternalDevices.activate_live_output_for(populations[0])

projections.append(
    Frontend.Projection(populations[1], populations[0],
                        Frontend.OneToOneConnector(weights=weight_to_spike)))

loopConnections = list()
for i in range(0, nNeurons - 1):
    singleConnection = (i, ((i + 1) % nNeurons), weight_to_spike, 3)
    loopConnections.append(singleConnection)

projections.append(Frontend.Projection(populations[0], populations[0],
                   Frontend.FromListConnector(loopConnections)))


Frontend.run(run_time)

spikes = populations[0].getSpikes(compatible_output=True)


if len(spikes) != 0:
    #print spikes
    pylab.figure()
    pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], ".")
    pylab.xlabel('neuron id')
    pylab.ylabel('Time/ms')
    pylab.title('spikes')
    pylab.show()
else:
    print "No spikes received"


Frontend.end()
