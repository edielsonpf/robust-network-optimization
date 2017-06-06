from NetworkOptimization.SA_Model import *


label = 'test';
datafile = '../examples/nsfnetFail.dat';
probLinkFail = 0.0005;
epsilon = 1e-5;

design(datafile, label,probLinkFail,epsilon)
