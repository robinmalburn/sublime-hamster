#!/usr/bin/env python
# Copyright (c) 2013 Robin Malburn
# See the file license.txt for copying permission.

import dbus
import json
import calendar
import time

HAMSTER_DBUS_PATH = "/org/gnome/Hamster"
HAMSTER_DBUS_IFACE = "org.gnome.Hamster"

if __name__ == "__main__":
	bus = dbus.SessionBus()
	obj = bus.get_object(HAMSTER_DBUS_IFACE, HAMSTER_DBUS_PATH)
	hamster = dbus.Interface(obj, HAMSTER_DBUS_IFACE)

	facts = []
	for fact in hamster.GetTodaysFacts():
		currentFact = {}
		currentFact["activity"] = str(fact[4])
		currentFact["category"] = str(fact[6])
		currentFact["description"] = str(fact[3])
		currentFact["tags"] = []
		for tag in fact[7]:
			currentFact["tags"].append(str(tag))
		currentFact["startTime"] = int(fact[1])
		currentFact["endTime"] = int(fact[2])
		currentFact["elapsedTime"] = 0

		if currentFact["endTime"] == 0:
			currentFact["elapsedTime"] = calendar.timegm(time.localtime()) - currentFact["startTime"]
		else:
			currentFact["elapsedTime"] = currentFact["endTime"] - currentFact["startTime"]

		facts.append(currentFact)

	#reverse our facts so that the newest activities are first
	facts.reverse()
		
	print json.dumps(facts)
