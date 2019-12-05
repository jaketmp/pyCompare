def rangeFrameLocator(tickLocs, axisRange):
	"""
	Convert axis tick positions for a Tufte style range frame. Takes existing tick locations, places a tick at the min and max of the data, and drops existing ticks that fall outside of this range or too close to the margins.

	TODO: Convert to a true axis artist that also sets spines

	:param list tickLocs: List of current tick locations on the axis
	:param tuple axisRange: Tuple of (min, max) value on the axis
	:returns: List of tick locations
	:rtype: list 
	"""
	newTicks = [axisRange[0]]

	for tick in tickLocs:
		if tick <= axisRange[0]:
			pass
		elif tick >= axisRange[1]:
			pass
		else:
			newTicks.append(tick)

	newTicks.append(axisRange[1])

	return newTicks


def rangeFrameLabler(tickLocs, tickLabels, cadence):
	"""
	Takes lists of tick positions and labels and drops the marginal text label where the gap between ticks is less than half the cadence value
	
	:param list tickLocs: List of current tick locations on the axis
	:param list tickLabels: List of tick labels
	:param float cadence: Gap between major tick positions
	:returns: List of tick labels
	:rtype: list 
	"""
	labels = []

	for i, tick in enumerate(tickLocs):
		if tick == tickLocs[0]:
			labels.append(tickLabels[i])

		elif tick == tickLocs[-1]:
			labels.append(tickLabels[i])

		elif (tick < (tickLocs[0] + (cadence / 2.0))) & (tick < (tickLocs[0] + cadence)):
			labels.append('')

		elif (tick > (tickLocs[-1] - (cadence / 2.0))) & (tick > (tickLocs[-1] - cadence)):
			labels.append('')

		else:
			labels.append(tickLabels[i])

	return labels
