“flock1”
This is my main flocking script in which we get and set the position of the transform nodes, apply the wander, cohesion and collision with audio interaction.

	
def wander(velocity, bass, prev):
	circleDist = 2.0
	circleRadius =30.0
	circleCenter = velocity.copy()
	circleCenter.normalize()
	circleCenter = circleCenter * circleDist
	

	print('circlecenter', circleCenter.x, circleCenter.y, circleCenter.z)
	
	displacement = tdu.Vector(0,-1,0)
	displacement = displacement * circleRadius
	print('displacement', displacement.x, displacement.y, displacement.z)
	
#	angleChange = 360
#	set how often want the angle to change
	time = int(me.time.seconds*6)
	print('time', time)
	

	frameNum = me.time.frame
	print('frame', frameNum)

	
	wanderAngle = angle(bass,prev)
	print('wanderAngle', wanderAngle)
	setAngle(displacement, wanderAngle)
	print('setangle displace', displacement.x, displacement.y, displacement.z)
			
	wanderForce = tdu.Vector()
	wanderForce = circleCenter + displacement

	print('wadnerforce', wanderForce.x, wanderForce.y, wanderForce.z)
	
	return wanderForce
		
def wallMargin(position, velocity):	

#	set to return position and equal to position and add forces to that					
	if position.x < 1000:
		position.x = position.x
	elif position.x > 1000:
		position.x = 0
		position.y = 0

	if position.x > -1000:
		position.x = position.x
	elif position.x < -1000:
		position.x = 0
		position.y = 0
						
	if position.y < 1000:
		position.y = position.y
	elif position.y > 1000:
		position.y = 0
		position.x = 0	
			
	if position.y > -1000:
		position.y = position.y
	elif position.y < -1000:
		position.y = 0
		position.x = 0
			
	return position
	
def cohesion(objects, velocity):
	distance = 15
	sum = tdu.Vector()
	count =0
	for i in objects:
		for j in objects:
			
			d = math.sqrt(math.pow((j.x - i.x), 2) +
						  math.pow((j.y - i.y), 2) +
						  math.pow((j.z - i.z), 2))
			if 0 < d < distance:
				sum = sum + j
				count += 1
	for i in objects:
		if count >0:
			sum = sum/count
		
			desired = tdu.Vector()
			desired = sum - i
			desired.normalize()
			desired = desired * 4
			steer = tdu.Vector()
			steer = desired - velocity
	
			return steer
		else:
	 		return velocity
import numpy as numpy
import random as rand
import math as math


def fish(transformOp):
	position = tdu.Vector()
	position.x = transformOp.par.tx.eval() 
	position.y = transformOp.par.ty.eval() 
	position.z = transformOp.par.tz.eval()
	
	return position
	
	
def transformFish(transformOp, position):
#	set the positions in the table
	table = op('positions')
	table[transformOp, 'tx'] = position.x
	table[transformOp, 'ty'] = position.y
	table[transformOp, 'tz'] = position.z
	return 
	
def steer(target, position, velocity, maxspeed):
	desired = tdu.Vector()
	desired = target - position
	desired.normalize()
	desired = desired * maxspeed
	steer = tdu.Vector()
	steer = desired - velocity
	return steer
		
		
def setAngle(vector, value):
	len = vector.length()
	vector.x = numpy.cos(value) * len
	vector.y = numpy.sin(value) * len

	return vector


def angle(bass, prev):
	angleChange = 360
	wanderAngle = float(op('values')['angle',1])
	print('wanderAnglefromtable', wanderAngle)
	if bass >= 0.65:	
		if bass < prev:
			if wanderAngle == wanderAngle :
				wanderAngle = rand.random() * angleChange - angleChange * 0.5
				wanderAngle += wanderAngle
				op('values')['angle',1] = wanderAngle
				print('wanderAngle', wanderAngle)
				return wanderAngle
			else:
				return wanderAngle 
		else:
			return wanderAngle
	else:
		return wanderAngle
	











Script input from ‘merge’ nodes. This script runs every frame, imports and calls from the flocking script.


import flock2 as flock



def cook(scriptOP):



	a = flock.fish(op('/project1/geo1/transform1'))
	b = flock.fish(op('/project1/geo1/transform2'))
	c = flock.fish(op('/project1/geo1/transform3'))
	d = flock.fish(op('/project1/geo1/transform4'))
	
	objects = [a,b,c,d]
			
#	add in audio nodes
	bass = op('/project1/geo1/bass')['chan1'].eval()
	prev = op('/project1/geo1/delay1')['chan1'].eval()

	x =0 
	for i in objects:
		velocity = tdu.Vector(i/me.time.frame)
		print('i', i)
		print('i', i.x, i.y, i.z)

		wanderer = tdu.Vector()
		wanderer = flock.wander(velocity, bass, prev)	
	
		collision = tdu.Vector()
			
		collision = flock.wallMargin(i, wanderer)
	
		cohesion = tdu.Vector()
		cohesion = flock.cohesion(objects, wanderer)
		position = tdu.Vector(i.x, i.y, i.z)
		collision = flock.wallMargin(i, cohesion)
		position = collision
		position = position + cohesion
		
		x += 1
		print('x', x)
#	need to get this to do for all 1-4 transforms string formatting/escape thing

		flock.transformFish(x, position)
			
		
	scriptOP.clear()
	return


Script to reset position parameters

def cook(scriptOP):
#	call to null that is the output from the button on top level
	select = float(op('/project1/null3')[0])	
	rows = op('/project1/geo1/positions').numRows	
	columns = op('/project1/geo1/positions').numCols
	
	if select == 1.0:
		for x in range(1,rows):
			for y in range(1,columns):
				op('positions')[x,y] = 0
				print('reset')
		
	scriptOP.clear()
	return

