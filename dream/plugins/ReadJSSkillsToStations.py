from copy import copy
import json
import time
import random
import operator
from datetime import datetime
import copy
from datetime import datetime

from dream.plugins import plugin
from dream.plugins import UpdateStationList

class ReadJSSkillsToStations(UpdateStationList.UpdateStationList):
  """ Input preparation 
      reads the operators and turns the technology-skills to the corresponding station-skills
  """

  def preprocess(self, data):
    """ turns the technology-skills to the corresponding station-skills
    """
    self.data = data
    nodes=data['graph']['node']
    # if there are nodes defined
    if nodes:
      # scan the nodes available
      for ID, node_data in nodes.iteritems():
        # if the node class is operator (if it has skillDict)
        skillDict = node_data.get("skillDict", {})
        if skillDict:
          for operation, technologyList in skillDict.iteritems():
            stationList = []
            for technology in technologyList:
              tech = technology.split("-")[0]
              for station in data["graph"]["node"]:
                if station.startswith(self.getStationInitials(tech))\
                    and data["graph"]["node"][station]["_class"] in self.STATION_CLASS_SET:
                  stationList.append(station)
            skillDict[operation] = stationList
          nodes[ID]["skillDict"] = skillDict
        
    return data

