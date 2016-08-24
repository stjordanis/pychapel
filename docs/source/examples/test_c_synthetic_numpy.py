#!/usr/bin/env python
from __future__ import print_function
import argparse
import numpy as np
from pych.extern import FromC

@FromC()
def simulation(tsteps=int, spin=np.ndarray, decay=np.ndarray, velocity=np.ndarray):
    """
    double* spin_ptr = (double*)spin->ptr_d;
    double* decay_ptr = (double*)decay->ptr_d;
    double* velocity_ptr = (double*)velocity->ptr_d;
    double result = 0.0;
    
    int particles = spin->shape[0];
    double* delta_ptr = (double*)malloc(particles*sizeof(double));
    
    for(int i=0; i<particles; i++) {
        delta_ptr[i] = velocity_ptr[i];
    }
    for(int timestep=0; timestep<tsteps; timestep++) {
        for(int i=0; i<particles; i++) {
            delta_ptr[i] = (spin_ptr[i] * decay_ptr[i] + velocity_ptr[i]) /
            delta_ptr[i];
        }
    }
    for(int i=0; i<particles; i++) {
        result += delta_ptr[i];
    }
    free(delta_ptr);

    return result;
    """
    return float

def main(tsteps, particles):
    """Load data, run simulation, visualize results."""

    spin = np.ones(particles)               # Load data
    decay = np.ones(particles)
    velocity = np.ones(particles)

    res = simulation(                       # Run simulation
        tsteps,
        spin,
        decay,
        velocity
    )
                                            # Visualize result
    print("Phenomenon after %d tsteps = %d." % (tsteps, res))

if __name__ == "__main__":                  # Argument parsing
    parser = argparse.ArgumentParser(
        description='Example illustrating simulation code.'
    )
    parser.add_argument(
        '--tsteps', help="# of tsteps in 'simulation'",
        type=int,
        required=True
    )
    parser.add_argument(
        '--particles', help="# of elements in arrays '",
        type=int,
        required=True
    )
    args = parser.parse_args()

    main(args.tsteps, args.particles)

import testcase
# contains the general testing method, which allows us to gather output
import os.path


def test_example():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 50 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 50 tsteps = 50000000.\n')

def test_example49():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 49 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 49 tsteps = 100000000.\n')

def test_example51():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 51 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 51 tsteps = 100000000.\n')

def test_example48():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 48 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 48 tsteps = 50000000.\n')

def test_example52():
    out = testcase.runpy(os.path.realpath(__file__) + ' --tsteps 52 --particles 50000000')
    # The first time this test is run, it may contain output notifying that
    # a temporary file has been created. The important part is that this
    # expected output follows it (enabling the test to work for all runs, as
    # the temporary file message won't occur in the second run) But that means
    # we can't use ==
    assert out.endswith('Phenomenon after 52 tsteps = 50000000.\n')
