#! /usr/bin/env bash

env=/path/to/env/settings
exe=/path/to/executable

source $env

mpirun -np {{nproc}} \
	$exe \
	--options \
	1> executable.stdout \
	2> executable.stderr
