def rangeFrameLocator(tickLocs, axisRange):
	"""
	Convert axis tick positions for a Tufte style range frame. Takes existing tick locations, places a tick at the min and max of the data, and drops exiting ticks that fall outside of this range or tooo colse to the margins.

	TODO: Convert to a true axis artist that also sets spines

	:param list tickLocs: List of current tick locations on the axis
	:param tuple axisRange: Tuple of (min, max) value on the axis
	:returns: List of tick locations
	:rtype: list 
	"""
	cadance = tickLocs[1] - tickLocs[0]
	newTicks = [axisRange[0]]

	for tick in tickLocs:
		if tick < axisRange[0]:
			pass
		elif (tick < (axisRange[0] + (cadance / 2.0))) & (tick < (axisRange[0] + cadance)):
			pass
		elif (tick > (axisRange[1] - (cadance / 2.0))) & (tick > (axisRange[1] - cadance)):
			pass
		elif tick > axisRange[1]:
			pass
		else:
			newTicks.append(tick)
	
	newTicks.append(axisRange[1])
	
	return newTicks
