from pox.core import core    # import core function
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from collections import defaultdict
from pox.openflow.discovery import Discovery
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer
import time

log = core.getLogger()

# Might be nice if we made this accessible on core...
#_adj = defaultdict(lambda:defaultdict(lambda:[]))

def _calc_spanning_tree ():   ## static method pass through class objects
  """
  Calculates the actual spanning tree

  Returns it as dictionary where the keys are DPID1, and the
  values are tuples of (DPID2, port-num), where port-num   ## DPID= KEY (DPID,PORT_NUMBER) = VALUES in port of (dpid,port-numn)
  
  is the port on DPID1 connecting to DPID2.
  """
  def flip (link):        # link parameters , variables 
    return Discovery.Link(link[2],link[3], link[0],link[1])  # values of parameter link pass to discovery.link list index =2 first
                                                             # here discovery is the class and link is class Lnk is tuple
  adj = defaultdict(lambda:defaultdict(lambda:[]))   # lambda = list we can modify list
  switches = set()         ## () tuples list cannot change through out the program set values 
  # Add all links and switches
  for l in core.openflow_discovery.adjacency:      # 
    adj[l.dpid1][l.dpid2].append(l)  # add at the end of append
    switches.add(l.dpid1)  # add value in switches  
    switches.add(l.dpid2)

  # Cull links -- we want a single symmetric link connecting nodes
  for s1 in switches:
    for s2 in switches:
      if s2 not in adj[s1]:
        continue
      if not isinstance(adj[s1][s2], list):
        continue
      assert s1 is not s2
      good = False
      for l in adj[s1][s2]:
        if flip(l) in core.openflow_discovery.adjacency:
          # This is a good one
          adj[s1][s2] = l.port1
          adj[s2][s1] = l.port2
          good = True
          break
      if not good:
        del adj[s1][s2]
        if s1 in adj[s2]:
          # Delete the other way too
          del adj[s2][s1]

  q = []
  more = set(switches)

  done = set()

  tree = defaultdict(set)

  while True:   ## infine loop keep running this forever
    q = sorted(list(more)) + q
    more.clear()
    if len(q) == 0: break   ## come out of while loop if len(q)==0
    v = q.pop(False)
    if v in done: continue
    done.add(v)
    for w,p in adj[v].iteritems():
      if w in tree: continue
      more.add(w)
      tree[v].add((w,p))
      tree[w].add((v,adj[w][v]))

  if False:
    log.debug("*** SPANNING TREE ***")
    for sw,ports in tree.iteritems():
      #print " ", dpidToStr(sw), ":", sorted(list(ports))
      #print " ", sw, ":", [l[0] for l in sorted(list(ports))]
      log.debug((" %i : " % sw) + " ".join([str(l[0]) for l in
                                           sorted(list(ports))]))
    log.debug("*********************")

  return tree


# Keep a list of previous port states so that we can skip some port mods
# If other things mess with port states, these may not be correct.  We
# could also refer to Connection.ports, but those are not guaranteed to
# be up to date.
_prev = defaultdict(lambda : defaultdict(lambda : None))

# If True, we set ports down when a switch connects
_noflood_by_default = False

# If True, don't allow turning off flood bits until a complete discovery
# cycle should have completed (mostly makes sense with _noflood_by_default).
_hold_down = False


def _handle_ConnectionUp (event):
  # When a switch connects, forget about previous port states
  _prev[event.dpid].clear()

  if _noflood_by_default:
    con = event.connection
    log.debug("Disabling flooding for %i ports", len(con.ports))
    for p in con.ports.itervalues():
      if p.port_no >= of.OFPP_MAX: continue
      _prev[con.dpid][p.port_no] = False
      pm = of.ofp_port_mod(port_no=p.port_no,
                          hw_addr=p.hw_addr,
                          config = of.OFPPC_NO_FLOOD,
                          mask = of.OFPPC_NO_FLOOD)
      con.send(pm)
    _invalidate_ports(con.dpid)

  if _hold_down:
    t = Timer(core.openflow_discovery.send_cycle_time + 1, _update_tree,
              kw={'force_dpid':event.dpid})


def _handle_LinkEvent (event):
  # When links change, update spanning tree

  (dp1,p1),(dp2,p2) = event.link.end
  if _prev[dp1][p1] is False:
    if _prev[dp2][p2] is False:
      # We're disabling this link; who cares if it's up or down?
      #log.debug("Ignoring link status for %s", event.link)
      return

  _update_tree()


def _update_tree (force_dpid = None):
  """
  Update spanning tree

  force_dpid specifies a switch we want to update even if we are supposed
  to be holding down changes.
  """

  # Get a spanning tree
  tree = _calc_spanning_tree()
  log.debug("Spanning tree updated")

  # Connections born before this time are old enough that a complete
  # discovery cycle should have completed (and, thus, all of their
  # links should have been discovered).
  enable_time = time.time() - core.openflow_discovery.send_cycle_time - 1

  # Now modify ports as needed
  try:
    change_count = 0
    for sw, ports in tree.iteritems():
      con = core.openflow.getConnection(sw)
      if con is None: continue # Must have disconnected
      if con.connect_time is None: continue # Not fully connected

      if _hold_down:
        if con.connect_time > enable_time:
          # Too young -- we should hold down changes.
          if force_dpid is not None and sw == force_dpid:
            # .. but we'll allow it anyway
            pass   # dont do anythin just move out
          else:
            continue

      tree_ports = [p[1] for p in ports]
      for p in con.ports.itervalues():
        if p.port_no < of.OFPP_MAX:
          flood = p.port_no in tree_ports
          if not flood:
            if core.openflow_discovery.is_edge_port(sw, p.port_no):
              flood = True
          if _prev[sw][p.port_no] is flood:
            #print sw,p.port_no,"skip","(",flood,")"
            continue # Skip
          change_count += 1
          _prev[sw][p.port_no] = flood
          #print sw,p.port_no,flood
          #TODO: Check results

          pm = of.ofp_port_mod(port_no=p.port_no,
                               hw_addr=p.hw_addr,
                               config = 0 if flood else of.OFPPC_NO_FLOOD,
                               mask = of.OFPPC_NO_FLOOD)
          con.send(pm)

          _invalidate_ports(con.dpid)
    if change_count:
      log.info("%i ports changed", change_count)
  except:
    _prev.clear()
    log.exception("Couldn't push spanning tree")


_dirty_switches = {} # A map dpid_with_dirty_ports->Timer
_coalesce_period = 2 # Seconds to wait between features requests

def _invalidate_ports (dpid):
  """
  Registers the fact that port info for dpid may be out of date

  When the spanning tree adjusts the port flags, the port config bits
  we keep in the Connection become out of date.  We don't want to just
  set them locally because an in-flight port status message could
  overwrite them.  We also might not want to assume they get set the
  way we want them.  SO, we do send a features request, but we wait a
  moment before sending it so that we can potentially coalesce several.

  TLDR: Port information for this switch may be out of date for around
        _coalesce_period seconds.
  """
  if dpid in _dirty_switches:
    # We're already planning to check
    return
  t = Timer(_coalesce_period, _check_ports, args=(dpid,))
  _dirty_switches[dpid] = t

def _check_ports (dpid):
  """
  Sends a features request to the given dpid
  """
  _dirty_switches.pop(dpid,None)
  con = core.openflow.getConnection(dpid)
  if con is None: return
  con.send(of.ofp_barrier_request())
  con.send(of.ofp_features_request())
  log.debug("Requested switch features for %s", str(con))


def launch (no_flood = False, hold_down = False):
  global _noflood_by_default, _hold_down
  if no_flood is True:
    _noflood_by_default = True
  if hold_down is True:
    _hold_down = True

  def start_spanning_tree ():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow_discovery.addListenerByName("LinkEvent", _handle_LinkEvent)
    log.debug("Spanning tree component ready")
  core.call_when_ready(start_spanning_tree, "openflow_discovery")
