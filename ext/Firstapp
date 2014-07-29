import logging
import json
from ryu.topology.switches import Switches
from ryu.topology import api
from ryu.topology.api import get_switch
from ryu.topology.api import get_all_switch
from ryu.topology.api import get_all_link
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER , CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.controller.controller import Datapath
from ryu.lib.packet import packet, ethernet, arp
from ryu.ofproto import ether
from ryu.lib import ofctl_v1_3
from ryu.app.ofctl import service
from ryu.lib import mac as mac_lib
from ryu.lib import addrconv
from ryu.topology import event
from ryu.lib.port_no import port_no_to_str
from ryu.controller import handler

ARP = arp.arp.__name__
LOG = logging.getLogger(__name__)

class configuration(app_manager.RyuApp):
 OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(configuration, self).__init__(*args, **kwargs)
        self.mac_table={}
        self.mac_to_port= {}
        #self.port_state = {}
        #self.dps={}


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def features_handler(self, ev):

        msg=ev.msg
        datapath = msg.datapath
        print ( 'Features_Handler ' )
        ofproto = datapath.ofproto
        of_parser = datapath.ofproto_parser
        priority_        priority_mac = 4
        cookie = 1
        dpid = datapath.id

        if dpid == 2:

           match = of_parser.OFPMatch( in_port =1 , arp_op = 1, eth_type = 0x0806, eth_dst='ff:ff:ff:ff:ff:ff', arp_tpa = '10.0.0.2')
           out_port = 2
           actions = []
           actions.append (of_parser.OFPActionSetField(eth_src='00:00:00:00:00:01'))
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)


           match = of_parser.OFPMatch ( in_port = 1, eth_type = 0x0800 ,ip_proto=1,icmpv4_type = 8, ipv4_src='10.0.0.1', ipv4_dst='10.0.0.2')
           out_port = 2
           actions = []
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)


           match = of_parser.OFPMatch ( in_port = 1, eth_type = 0x0800 ,ip_proto=1,icmpv4_type = 8, ipv4_src='10.0.0.1', ipv4_dst='10.0.0.2')
           out_port = 2
           actions = []
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)


          ########################################################################
           match = of_parser.OFPMatch ( eth_type = 0x0806 ,arp_op = 2, eth_dst='00:00:00:00:00:01' )
           out_port = 1
           actions=[]
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch ( eth_type = 0x0800 ,ip_proto=1,icmpv4_type = 0 , ipv4_dst='10.0.0.1')
           out_port = 1
           actions=[]
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)
            ########################################################################
           match = of_parser.OFPMatch ( eth_type = 0x0806 ,arp_op = 2, eth_dst='00:00:00:00:00:01' )
           out_port = 1
           actions=[]
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch ( eth_type = 0x0800 ,ip_proto=1,icmpv4_type = 0 , ipv4_dst='10.0.0.1')
           out_port = 1
           actions=[]
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_mac, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch( in_port =1 , arp_op = 1, eth_type = 0x0806, eth_dst='ff:ff:ff:ff:ff:ff')

           out_port = 3
           actions=[]
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=3, match=match,instructions=inst)
           datapath.send_msg(out)



           #######################################################################

           match = of_parser.OFPMatch ( in_port = 1, eth_type = 0x0800 ,ip_proto=1,icmpv4_type = 8, ipv4_src='10.0.0.1')
           out_port = 3
           actions = []
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           
           match = of_parser.OFPMatch( in_port =1 , arp_op = 1, eth_type = 0x0806, eth_dst='ff:ff:ff:ff:ff:ff')

           out_port = 3
           actions=[]
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=3, match=match,instructions=inst)
           datapath.send_msg(out)



           #######################################################################

           match = of_parser.OFPMatch ( in_port = 1, eth_type = 0x0800 ,ip_proto=1,icmpv4_type = 8, ipv4_src='10.0.0.1')
           out_port = 3
           actions = []
           actions.append (of_parser.OFPActionOutput(out_port))
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=2, match=match,instructions=inst)
           datapath.send_msg(out)
           #########################################################################

        if dpid == 1:
           match = of_parser.OFPMatch( in_port =1 , arp_op = 1, eth_type = 0x0806, eth_dst='ff:ff:ff:ff:ff:ff')
           out_port = 2
           actions = [of_parser.OFPActionOutput(out_port)]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch( in_port =1 , eth_type = 0x0800,ip_proto=1,icmpv4_type = 8)
           out_port = 2
           actions = [of_parser.OFPActionOutput(out_port )]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)
            match = of_parser.OFPMatch( in_port =2 )
           out_port = 1
           actions = [of_parser.OFPActionOutput(out_port )]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)

        if dpid == 3:
           match = of_parser.OFPMatch( in_port = 3 ,  arp_op = 1, eth_type = 0x0806, eth_dst='ff:ff:ff:ff:ff:ff', arp_tpa='10.0.0.3')
           actions = [of_parser.OFPActionOutput(1) ]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch( in_port = 3 ,  arp_op = 1, eth_type = 0x0806, eth_dst='ff:ff:ff:ff:ff:ff', arp_tpa='10.0.0.4')
           actions = [of_parser.OFPActionOutput(2) ]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)
            match = of_parser.OFPMatch( arp_op = 2, eth_type = 0x0806 )
           actions = [of_parser.OFPActionOutput(3) ]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch( in_port =3 , eth_type = 0x0800,ip_proto=1,icmpv4_type = 8)
           actions = [of_parser.OFPActionOutput(1) ]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)

           match = of_parser.OFPMatch( eth_type = 0x0800,ip_proto=1,icmpv4_type = 0)
           actions = [of_parser.OFPActionOutput(3) ]
           inst = [of_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
           out = of_parser.OFPFlowMod(datapath=datapath, priority=priority_arp, match=match,instructions=inst)
           datapath.send_msg(out)
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

       #sw_list  = get_switch(self, 1)
       sw_list = api.get_all_switch(self)
       sw_list_body =json.dumps([ switch.to_dict() for switch in sw_list])
       print('sw_list_body {}'.format(sw_list_body))

       #link_list = api.get_all_link(self)
       #link_list_body = json.dumps([ link.to_dict() for link in link_list ])
       #print('link_list_body {}'.format(link_list_body))

       link_self = api.get_link(self,1)  ## dpid
       link_body = json.dumps([ link.to_dict() for link in link_self ])
       print('link_body {}'.format(link_body))

       link_self = api.get_link(self,2)  ## dpid
       link_body = json.dumps([ link.to_dict() for link in link_self ])
       print('link_body {}'.format(link_body))

       #link_self = api.get_link(self,3)  ## dpid
       #link_body = json.dumps([ link.to_dict() for link in link_self ])
       #print('link_body {}'.format(link_body))
            msg = ev.msg                     # object which describes the openflow messages must
       datapath = msg.datapath          # instance that describes and openflowswitch datapath must
       print ('Coming from')            # how can i know about the datapath?
       ofproto = datapath.ofproto       # of proto is an instance of the function inhereted by datapath it basically export openflow modules
       parser = datapath.ofproto_parser # encoding and decoding of openflow messages version ?
       in_port = msg.match['in_port']
       out_port = ofproto.OFPP_FLOOD
                                        # always used for Openflow protocols
       data=msg.data                                 #buffer_id=msg.buffer_id
       actions = [parser.OFPActionOutput(out_port,0)] # prepare openflow messages ofproto_parser OFPxxx (xxx is message)

       out = parser.OFPPacketOut(datapath=datapath,buffer_id = ofproto.OFP_NO_BUFFER, in_port=in_port, actions=actions, data=data)
       datapath.send_msg(out)




    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def port_status_handler(self,ev):
       msg=ev.msg
       reason=msg.reason
       dp=msg.datapath
       ofpport = msg.desc

       Switches.port_status_handler
       print('yes')

    @handler.set_ev_cls(event.EventPortModify)
    def port_modify_handler(self, ev):
        LOG.debug(ev)

       #if reason == dp.ofproto.OFPPR_MODIFY:
          #self.port_state[dp.id].modify(ofpport.port_no, ofpport)
          #self.send_event_to_observers(
          #event.EventPortModify(Port(dp.id, dp.ofproto, ofpport)))


