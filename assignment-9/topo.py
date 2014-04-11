#!/usr/bin/env python
from mininet.topo import Topo


class TwoHostNInterfaceTopo(Topo):
    "Two hosts connected by N interfaces"

    def __init__(self, n, **opts):
        "n is the number of interfaces connecting the hosts."
        super(TwoHostNInterfaceTopo, self).__init__(**opts)

        # Note: switches are not strictly necessary, but they do give
        # visibility into traffic from the root namespace.
        SWITCHES = ['s%i' % i for i in range(1, n + 1)]
        for sw in SWITCHES:
            self.addSwitch(sw)

        HOSTS = ['h1', 'h2']
        for h in HOSTS:
            self.addHost(h)
            for sw in SWITCHES:
                self.addLink(h, sw)


topos = {'2hostNintf': lambda n: TwoHostNInterfaceTopo(n)}

#-----------------------------------------------

'''@package dctopo

Data center network topology creation and drawing.

@author Brandon Heller (brandonh@stanford.edu)

This package includes code to create and draw networks with a regular,
repeated structure.  The main class is StructuredTopo, which augments the
standard Mininet Topo object with layer metadata plus convenience functions to
enumerate up, down, and layer edges.
'''



PORT_BASE = 1  # starting index for OpenFlow switch ports


class NodeID(object):
    '''Topo node identifier.'''

    def __init__(self, dpid = None):
        '''Init.

        @param dpid dpid
        '''
        # DPID-compatible hashable identifier: opaque 64-bit unsigned int
        self.dpid = dpid

    def __str__(self):
        '''String conversion.

        @return str dpid as string
        '''
        return str(self.dpid)

    def name_str(self):
        '''Name conversion.

        @return name name as string
        '''
        return str(self.dpid)

    def ip_str(self):
        '''Name conversion.

        @return ip ip as string
        '''
        hi = (self.dpid & 0xff0000) >> 16
        mid = (self.dpid & 0xff00) >> 8
        lo = self.dpid & 0xff
        return "10.%i.%i.%i" % (hi, mid, lo)


class StructuredNodeSpec(object):
    '''Layer-specific vertex metadata for a StructuredTopo graph.'''

    def __init__(self, up_total, down_total, up_speed, down_speed,
                 type_str = None):
        '''Init.

        @param up_total number of up links
        @param down_total number of down links
        @param up_speed speed in Gbps of up links
        @param down_speed speed in Gbps of down links
        @param type_str string; model of switch or server
        '''
        self.up_total = up_total
        self.down_total = down_total
        self.up_speed = up_speed
        self.down_speed = down_speed
        self.type_str = type_str


class StructuredEdgeSpec(object):
    '''Static edge metadata for a StructuredTopo graph.'''

    def __init__(self, speed = 1.0):
        '''Init.

        @param speed bandwidth in Gbps
        '''
        self.speed = speed


class StructuredTopo(Topo):
    '''Data center network representation for structured multi-trees.'''

    def __init__(self, node_specs, edge_specs):
        '''Create StructuredTopo object.

        @param node_specs list of StructuredNodeSpec objects, one per layer
        @param edge_specs list of StructuredEdgeSpec objects for down-links,
            one per layer
        '''
        super(StructuredTopo, self).__init__()
        self.node_specs = node_specs
        self.edge_specs = edge_specs

    def def_nopts(self, layer):
        '''Return default dict for a structured topo.

        @param layer layer of node
        @return d dict with layer key/val pair, plus anything else (later)
        '''
        return {'layer': layer}

    def layer(self, name):
        '''Return layer of a node

        @param name name of switch
        @return layer layer of switch
        '''
        return self.node_info[name]['layer']

    def isPortUp(self, port):
        ''' Returns whether port is facing up or down

        @param port port number
        @return portUp boolean is port facing up?
        '''
        return port % 2 == PORT_BASE

    def layer_nodes(self, layer):
        '''Return nodes at a provided layer.

        @param layer layer
        @return names list of names
        '''
        def is_layer(n):
            '''Returns true if node is at layer.'''
            return self.layer(n) == layer

        nodes = [n for n in self.g.nodes() if is_layer(n)]
        return nodes

    def up_nodes(self, name):
        '''Return edges one layer higher (closer to core).

        @param name name

        @return names list of names
        '''
        layer = self.layer(name) - 1
        nodes = [n for n in self.g[name] if self.layer(n) == layer]
        return nodes

    def down_nodes(self, name):
        '''Return edges one layer higher (closer to hosts).

        @param name name
        @return names list of names
        '''
        layer = self.layer(name) + 1
        nodes = [n for n in self.g[name] if self.layer(n) == layer]
        return nodes

    def up_edges(self, name):
        '''Return edges one layer higher (closer to core).

        @param name name
        @return up_edges list of name pairs
        '''
        edges = [(name, n) for n in self.up_nodes(name)]
        return edges

    def down_edges(self, name):
        '''Return edges one layer lower (closer to hosts).

        @param name name
        @return down_edges list of name pairs
        '''
        edges = [(name, n) for n in self.down_nodes(name)]
        return edges

#    def draw(self, filename = None, edge_width = 1, node_size = 1,
#             node_color = 'g', edge_color = 'b'):
#        '''Generate image of RipL network.
#
#        @param filename filename w/ext to write; if None, show topo on screen
#        @param edge_width edge width in pixels
#        @param node_size node size in pixels
#        @param node_color node color (ex 'b' , 'green', or '#0000ff')
#        @param edge_color edge color
#        '''
#        import matplotlib.pyplot as plt
#
#        pos = {} # pos[vertex] = (x, y), where x, y in [0, 1]
#        for layer in range(len(self.node_specs)):
#            v_boxes = len(self.node_specs)
#            height = 1 - ((layer + 0.5) / v_boxes)
#
#            layer_nodes = sorted(self.layer_nodes(layer, False))
#            h_boxes = len(layer_nodes)
#            for j, dpid in enumerate(layer_nodes):
#                pos[dpid] = ((j + 0.5) / h_boxes, height)
#
#        fig = plt.figure(1)
#        fig.clf()
#        ax = fig.add_axes([0, 0, 1, 1], frameon = False)
#
#        draw_networkx_nodes(self.g, pos, ax = ax, node_size = node_size,
#                               node_color = node_color, with_labels = False)
#        # Work around networkx bug; does not handle color arrays properly
#        for edge in self.edges(False):
#            draw_networkx_edges(self.g, pos, [edge], ax = ax,
#                                edge_color = edge_color, width = edge_width)
#
#        # Work around networkx modifying axis limits
#        ax.set_xlim(0, 1.0)
#        ax.set_ylim(0, 1.0)
#        ax.set_axis_off()
#
#        if filename:
#            plt.savefig(filename)
#        else:
#            plt.show()


class FatTreeTopo(StructuredTopo):
    '''Three-layer homogeneous Fat Tree.

    From "A scalable, commodity data center network architecture, M. Fares et
    al. SIGCOMM 2008."
    '''
    LAYER_CORE = 0
    LAYER_AGG = 1
    LAYER_EDGE = 2
    LAYER_HOST = 3

    class FatTreeNodeID(NodeID):
        '''Fat Tree-specific node.'''

        def __init__(self, pod = 0, sw = 0, host = 0, dpid = None, name = None):
            '''Create FatTreeNodeID object from custom params.

            Either (pod, sw, host) or dpid must be passed in.

            @param pod pod ID
            @param sw switch ID
            @param host host ID
            @param dpid optional dpid
            @param name optional name
            '''
            if dpid:
                self.pod = (dpid & 0xff0000) >> 16
                self.sw = (dpid & 0xff00) >> 8
                self.host = (dpid & 0xff)
                self.dpid = dpid
            elif name:
                pod, sw, host = [int(s) for s in name.split('_')]
                self.pod = pod
                self.sw = sw
                self.host = host
                self.dpid = (pod << 16) + (sw << 8) + host
            else:
                self.pod = pod
                self.sw = sw
                self.host = host
                self.dpid = (pod << 16) + (sw << 8) + host

        def __str__(self):
            return "(%i, %i, %i)" % (self.pod, self.sw, self.host)

        def name_str(self):
            '''Return name string'''
            return "%i_%i_%i" % (self.pod, self.sw, self.host)

        def mac_str(self):
            '''Return MAC string'''
            return "00:00:00:%02x:%02x:%02x" % (self.pod, self.sw, self.host)

        def ip_str(self):
            '''Return IP string'''
            return "10.%i.%i.%i" % (self.pod, self.sw, self.host)
    """
    def _add_port(self, src, dst):
        '''Generate port mapping for new edge.

        Since Node IDs are assumed hierarchical and unique, we don't need to
        maintain a port mapping.  Instead, compute port values directly from
        node IDs and topology knowledge, statelessly, for calls to self.port.

        @param src source switch DPID
        @param dst destination switch DPID
        '''
        pass
    """
    def def_nopts(self, layer, name = None):
        '''Return default dict for a FatTree topo.

        @param layer layer of node
        @param name name of node
        @return d dict with layer key/val pair, plus anything else (later)
        '''
        d = {'layer': layer}
        if name:
            id = self.id_gen(name = name)
            # For hosts only, set the IP
            if layer == self.LAYER_HOST:
              d.update({'ip': id.ip_str()})
              d.update({'mac': id.mac_str()})
            d.update({'dpid': "%016x" % id.dpid})
        return d


    def __init__(self, k = 4, speed = 1.0):
        '''Init.

        @param k switch degree
        @param speed bandwidth in Gbps
        '''
        core = StructuredNodeSpec(0, k, None, speed, type_str = 'core')
        agg = StructuredNodeSpec(k / 2, k / 2, speed, speed, type_str = 'agg')
        edge = StructuredNodeSpec(k / 2, k / 2, speed, speed,
                                  type_str = 'edge')
        host = StructuredNodeSpec(1, 0, speed, None, type_str = 'host')
        node_specs = [core, agg, edge, host]
        edge_specs = [StructuredEdgeSpec(speed)] * 3
        super(FatTreeTopo, self).__init__(node_specs, edge_specs)

        self.k = k
        self.id_gen = FatTreeTopo.FatTreeNodeID
        self.numPods = k
        self.aggPerPod = k / 2

        pods = range(0, k)
        core_sws = range(1, k / 2 + 1)
        agg_sws = range(k / 2, k)
        edge_sws = range(0, k / 2)
        hosts = range(2, k / 2 + 2)

        for p in pods:
            for e in edge_sws:
                edge_id = self.id_gen(p, e, 1).name_str()
                edge_opts = self.def_nopts(self.LAYER_EDGE, edge_id)
                self.addSwitch(edge_id, **edge_opts)

                for h in hosts:
                    host_id = self.id_gen(p, e, h).name_str()
                    host_opts = self.def_nopts(self.LAYER_HOST, host_id)
                    self.addHost(host_id, **host_opts)
                    self.addLink(host_id, edge_id)

                for a in agg_sws:
                    agg_id = self.id_gen(p, a, 1).name_str()
                    agg_opts = self.def_nopts(self.LAYER_AGG, agg_id)
                    self.addSwitch(agg_id, **agg_opts)
                    self.addLink(edge_id, agg_id)

            for a in agg_sws:
                agg_id = self.id_gen(p, a, 1).name_str()
                c_index = a - k / 2 + 1
                for c in core_sws:
                    core_id = self.id_gen(k, c_index, c).name_str()
                    core_opts = self.def_nopts(self.LAYER_CORE, core_id)
                    self.addSwitch(core_id, **core_opts)
                    self.addLink(core_id, agg_id)


    def port(self, src, dst):
        '''Get port number (optional)

        Note that the topological significance of DPIDs in FatTreeTopo enables
        this function to be implemented statelessly.

        @param src source switch DPID
        @param dst destination switch DPID
        @return tuple (src_port, dst_port):
            src_port: port on source switch leading to the destination switch
            dst_port: port on destination switch leading to the source switch
        '''
        src_layer = self.layer(src)
        dst_layer = self.layer(dst)

        src_id = self.id_gen(name = src)
        dst_id = self.id_gen(name = dst)

        LAYER_CORE = 0
        LAYER_AGG = 1
        LAYER_EDGE = 2
        LAYER_HOST = 3

        if src_layer == LAYER_HOST and dst_layer == LAYER_EDGE:
            src_port = 0
            dst_port = (src_id.host - 2) * 2 + 1
        elif src_layer == LAYER_EDGE and dst_layer == LAYER_CORE:
            src_port = (dst_id.sw - 2) * 2
            dst_port = src_id.pod
        elif src_layer == LAYER_EDGE and dst_layer == LAYER_AGG:
            src_port = (dst_id.sw - self.k / 2) * 2
            dst_port = src_id.sw * 2 + 1
        elif src_layer == LAYER_AGG and dst_layer == LAYER_CORE:
            src_port = (dst_id.host - 1) * 2
            dst_port = src_id.pod
        elif src_layer == LAYER_CORE and dst_layer == LAYER_AGG:
            src_port = dst_id.pod
            dst_port = (src_id.host - 1) * 2
        elif src_layer == LAYER_AGG and dst_layer == LAYER_EDGE:
            src_port = dst_id.sw * 2 + 1
            dst_port = (src_id.sw - self.k / 2) * 2
        elif src_layer == LAYER_CORE and dst_layer == LAYER_EDGE:
            src_port = dst_id.pod
            dst_port = (src_id.sw - 2) * 2
        elif src_layer == LAYER_EDGE and dst_layer == LAYER_HOST:
            src_port = (dst_id.host - 2) * 2 + 1
            dst_port = 0
        else:
            raise Exception("Could not find port leading to given dst switch")

        # Shift by one; as of v0.9, OpenFlow ports are 1-indexed.
        if src_layer != LAYER_HOST:
            src_port += 1
        if dst_layer != LAYER_HOST:
            dst_port += 1

        return (src_port, dst_port)
  
