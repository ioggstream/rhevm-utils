#!/usr/bin/env python
#
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@redhat.com)
#
# Description: Basic common set of functions for usage in other scripts
#
# Requires rhevm-sdk to work
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.

import sys
import getopt
import optparse
import os
import time
import operator

from ovirtsdk.api import API
from ovirtsdk.xml import params


#FUNCTIONS
def check_tags(api, options):
    """Checks if required tags have been already defined and creates them if missing"""
    if options.verbosity >= 1:
        print "Looking for tags prior to start..."

    if not api.tags.get(name="elas_manage"):
        if options.verbosity >= 2:
            print "Creating tag elas_manage..."
        api.tags.add(params.Tag(name="elas_manage"))

    if not api.tags.get(name="elas_start"):
        if options.verbosity >= 2:
            print "Creating tag elas_start..."
        api.tags.add(params.Tag(name="elas_start"))

    return


def migra(api, options, vm, action=None):
    """Initiates migration action of the vm to specified host or automatically if None"""
    if not action:
        try:
            vm.migrate()
        except:
            if options.verbosity > 4:
                print "Problem migrating auto %s" % vm.name
    else:
        try:
            vm.migrate(action)
        except:
            if options.verbosity > 4:
                print "Problem migrating fixed %s" % vm.name

    loop = True
    counter = 0
    while loop:
        if vm.status.state == "up":
            loop = False
        if options.verbosity > 8:
            print "VM migration loop %s" % counter
        time.sleep(10)
        counter = counter + 1

        if counter > 12:
            loop = False
            if options.verbosity > 8:
                print "Exiting on max loop retries"
    return


def vmused(api, vm):
    """Returns amount of memory used by the VM from Agent if installed or configured if not"""
    # Get memory usage from agent
    used = vm.statistics.get("memory.used").values.value[0].datum
    if    used == 0:
        #If no value received, return installed memory
        used = vm.statistics.get("memory.installed").values.value[0].datum

    return used


def listvms(api, oquery=""):
    """Returns a list of VM's based on query"""
    vms = []
    page = 0
    length = 100
    while (length > 0):
        page = page + 1
        query = "%s page %s" % (oquery, page)
        tanda = api.vms.list(query=query)
        length = len(tanda)
        for vm in tanda:
            yield vm


def listhosts(api, oquery=""):
    """Returns a list of Hosts based on query"""
    hosts = []
    page = 0
    length = 100
    while (length > 0):
        page = page + 1
        query = "%s page %s" % (oquery, page)
        tanda = api.hosts.list(query=query)
        length = len(tanda)
        for host in tanda:
            yield host


if __name__ == "__main__":
    print """This file is intented to be used as a library of functions and it's not expected to be executed directly"""
