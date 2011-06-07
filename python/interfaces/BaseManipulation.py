# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import with_statement # for python 2.5
__author__ = 'Rosen Diankov'
__copyright__ = 'Copyright (C) 2009-2010 Rosen Diankov (rosen.diankov@gmail.com)'
__license__ = 'Apache License, Version 2.0'
import openravepy
import numpy
from copy import copy as shallowcopy
class BaseManipulation:
    """Interface wrapper for :ref:`probleminstance-basemanipulation`
    """
    def __init__(self,robot,plannername=None,maxvelmult=None):
        env = robot.GetEnv()
        self.prob = openravepy.RaveCreateProblem(env,'BaseManipulation')
        self.robot = robot
        self.args = self.robot.GetName()
        if plannername is not None:
            self.args += ' planner ' + plannername
        if maxvelmult is not None:
            self.args += ' maxvelmult %f '%maxvelmult
        if env.LoadProblem(self.prob,self.args) != 0:
            raise ValueError('problem failed to initialize')
    def  __del__(self):
        self.prob.GetEnv().Remove(self.prob)
    def clone(self,envother):
        """Clones the interface into another environment
        """
        clone = shallowcopy(self)
        clone.prob = openravepy.RaveCreateProblem(envother,'BaseManipulation')
        clone.robot = envother.GetRobot(self.robot.GetName())
        if envother.LoadProblem(clone.prob,clone.args) != 0:
            raise ValueError('problem failed to initialize')
        return clone
    def TrajFromData(self,data,resettrans=False,resettiming=False):
        """See :ref:`probleminstance-basemanipulation-traj`
        """
        return self.prob.SendCommand('traj stream ' + data + ' %d %d '%(resettiming,resettiming))
    def MoveHandStraight(self,direction,minsteps=None,maxsteps=None,stepsize=None,ignorefirstcollision=None,starteematrix=None,greedysearch=True,execute=None,outputtraj=None,maxdeviationangle=None):
        """See :ref:`probleminstance-basemanipulation-movehandstraight`
        """
        cmd = 'MoveHandStraight direction %f %f %f '%(direction[0],direction[1],direction[2])
        if minsteps is not None:
            cmd += 'minsteps %d '%minsteps
        if maxsteps is not None:
            cmd += 'maxsteps %d '%maxsteps
        if stepsize is not None:
            cmd += 'stepsize %f '%stepsize
        if execute is not None:
            cmd += 'execute %d '%execute
        if starteematrix is not None:
            cmd += 'starteematrix ' + openravepy.matrixSerialization(starteematrix) + ' '
        if greedysearch is not None:
            cmd += 'greedysearch %d '%greedysearch
        if outputtraj is not None and outputtraj:
            cmd += 'outputtraj '
        if ignorefirstcollision is not None:
            cmd += 'ignorefirstcollision %f '%ignorefirstcollision
        if maxdeviationangle is not None:
            cmd += 'maxdeviationangle %f '%maxdeviationangle
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('MoveHandStraight')
        return res
    def MoveManipulator(self,goal,maxiter=None,execute=None,outputtraj=None,maxtries=None):
        """See :ref:`probleminstance-basemanipulation-movemanipulator`
        """
        assert(len(goal) == len(self.robot.GetActiveManipulator().GetArmIndices()) and len(goal) > 0)
        cmd = 'MoveManipulator goal ' + ' '.join(str(f) for f in goal) + ' '
        if execute is not None:
            cmd += 'execute %d '%execute
        if outputtraj is not None and outputtraj:
            cmd += 'outputtraj '
        if maxiter is not None:
            cmd += 'maxiter %d '%maxiter
        if maxtries is not None:
            cmd += 'maxtries %d '%maxtries
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('MoveManipulator')
        return res
    def MoveActiveJoints(self,goal,steplength=None,maxiter=None,maxtries=None,execute=None,outputtraj=None):
        """See :ref:`probleminstance-basemanipulation-moveactivejoints`
        """
        assert(len(goal) == self.robot.GetActiveDOF() and len(goal) > 0)
        cmd = 'MoveActiveJoints goal ' + ' '.join(str(f) for f in goal)+' '
        if steplength is not None:
            cmd += 'steplength %f '%steplength
        if execute is not None:
            cmd += 'execute %d '%execute
        if outputtraj is not None and outputtraj:
            cmd += 'outputtraj '
        if maxiter is not None:
            cmd += 'maxiter %d '%maxiter
        if maxtries is not None:
            cmd += 'maxtries %d '%maxtries
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('MoveActiveJoints')
        return res
    def MoveToHandPosition(self,matrices=None,affinedofs=None,maxiter=None,maxtries=None,translation=None,rotation=None,seedik=None,constraintfreedoms=None,constraintmatrix=None,constrainterrorthresh=None,execute=None,outputtraj=None):
        """See :ref:`probleminstance-basemanipulation-movetohandposition`
        """
        cmd = 'MoveToHandPosition '
        if matrices is not None:
            cmd += 'matrices %d '%len(matrices)
            for m in matrices:
                cmd += openravepy.matrixSerialization(m) + ' '
        if maxiter is not None:
            cmd += 'maxiter %d '%maxiter
        if maxtries is not None:
            cmd += 'maxtries %d '%maxtries
        if translation is not None:
            cmd += 'translation %f %f %f '%(translation[0],translation[1],translation[2])
        if rotation is not None:
            cmd += 'rotation %f %f %f %f '%(rotation[0],rotation[1],rotation[2],rotation[3])
        if seedik is not None:
            cmd += 'seedik %d '%seedik
        if constraintfreedoms is not None:
            cmd += 'constraintfreedoms %s '%(' '.join(str(constraintfreedoms[i]) for i in range(6)))
        if constraintmatrix is not None:
            cmd += 'constraintmatrix %s '%openravepy.matrixSerialization(constraintmatrix)
        if constrainterrorthresh is not None:
            cmd += 'constrainterrorthresh %s '%constrainterrorthresh
        if execute is not None:
            cmd += 'execute %d '%execute
        if outputtraj is not None and outputtraj:
            cmd += 'outputtraj '
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('MoveToHandPosition')
        return res
    def MoveUnsyncJoints(self,jointvalues,jointinds,maxtries=None,planner=None,maxdivision=None,execute=None,outputtraj=None):
        """See :ref:`probleminstance-basemanipulation-moveunsyncjoints`
        """
        assert(len(jointinds)==len(jointvalues) and len(jointinds)>0)
        cmd = 'MoveUnsyncJoints handjoints %d %s %s '%(len(jointinds),' '.join(str(f) for f in jointvalues), ' '.join(str(f) for f in jointinds))
        if planner is not None:
            cmd += 'planner %s '%planner
        if execute is not None:
            cmd += 'execute %d '%execute
        if outputtraj is not None and outputtraj:
            cmd += 'outputtraj '
        if maxtries is not None:
            cmd += 'maxtries %d '%maxtries
        if maxdivision is not None:
            cmd += 'maxdivision %d '%maxdivision
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('MoveUnsyncJoints')
        return res
    def JitterActive(self,maxiter=None,jitter=None,execute=None,outputtraj=None,outputfinal=None):
        """See :ref:`probleminstance-basemanipulation-jitteractive`
        """
        cmd = 'JitterActive '
        if maxiter is not None:
            cmd += 'maxiter %d '%maxiter
        if jitter is not None:
            cmd += 'jitter %f '%jitter
        if execute is not None:
            cmd += 'execute %d '%execute
        if outputtraj is not None and outputtraj:
            cmd += 'outputtraj '
        if outputfinal:
            cmd += 'outputfinal'
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('JitterActive')
        resvalues = res.split()
        if outputfinal:
            final = numpy.array([numpy.float64(resvalues[i]) for i in range(self.robot.GetActiveDOF())])
            resvalues=resvalues[len(final):]
        else:
            final=None
        if outputtraj is not None and outputtraj:
            traj = ' '.join(resvalues)
        else:
            traj = None
        return final,traj
    def FindIKWithFilters(self,ikparam,cone=None,solveall=None,filteroptions=None):
        """See :ref:`probleminstance-basemanipulation-findikwithfilters`
        """
        cmd = 'FindIKWithFilters ikparam %s '%str(ikparam)
        if cone is not None:            
            cmd += 'cone %s '%(' '.join(str(f) for f in cone))
        if solveall is not None and solveall:
            cmd += 'solveall '
        if filteroptions is not None:
            cmd += 'filteroptions %d '%filteroptions        
        res = self.prob.SendCommand(cmd)
        if res is None:
            raise openravepy.planning_error('FindIKWithFilters')
        resvalues = res.split()
        num = int(resvalues[0])
        dim = (len(resvalues)-1)/num
        solutions = numpy.reshape([numpy.float64(s) for s in resvalues[1:]],(num,dim))
        return solutions
