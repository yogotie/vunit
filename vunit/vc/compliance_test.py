# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2020, Lars Asplund lars.anders.asplund@gmail.com

"""
Module for generating a compliance test for a VUnit verification component
"""

import argparse
import sys
import logging
from os import makedirs
from os.path import exists, join, dirname, isdir, abspath
from vunit.vc.verification_component import VerificationComponent
from vunit.vc.verification_component_interface import VerificationComponentInterface


def _create_vc_template(args):
    """Creates VC testbench template from args."""
    template_code, vc_name = VerificationComponent.create_vhdl_testbench_template(
        args.vc_lib_name, args.vc_path, args.vci_path
    )
    if not template_code or not vc_name:
        sys.exit(1)

    if not args.output_path:
        output_dir = join(dirname(args.vc_path), ".vc")
        if not exists(output_dir):
            makedirs(output_dir)

        output_path = join(output_dir, "tb_%s_compliance_template.vhd" % vc_name)
    elif isdir(args.output_path):
        output_path = join(args.output_path, "tb_%s_compliance_template.vhd" % vc_name)
    else:
        output_path = args.output_path

    with open(output_path, "w") as output_file:
        output_file.write(template_code)
        print(
            "Open %s and read the TODOs to complete the template."
            % abspath(output_path)
        )


def _create_vci_template(args):
    """Creates VCI testbench template from args."""
    (
        template_code,
        vci_name,
    ) = VerificationComponentInterface.create_vhdl_testbench_template(
        args.vc_lib_name, args.vci_path, args.vc_handle_t
    )
    if not template_code or not vci_name:
        sys.exit(1)

    if not args.output_path:
        output_dir = join(dirname(args.vc_path), ".vc", vci_name)
        if not exists(output_dir):
            makedirs(output_dir, exist_ok=True)

        output_path = join(
            output_dir, "tb_%s_compliance_template.vhd" % args.vc_handle_t,
        )
    elif isdir(args.output_path):
        output_dir = join(args.output_path, vci_name)
        makedirs(output_dir, exist_ok=True)
        output_path = join(
            output_dir, "tb_%s_compliance_template.vhd" % args.vc_handle_t,
        )
    else:
        output_path = args.output_path

    with open(output_path, "w") as output_file:
        output_file.write(template_code)
        print(
            "Open %s and read the TODOs to complete the template."
            % abspath(output_path)
        )


def main():
    """Parses the command line arguments and acts accordingly."""

    def create_vc_parser(subparsers):
        parser = subparsers.add_parser(
            "create-vc", help="Creates a VC compliance test template"
        )
        parser.add_argument(
            "-l",
            "--vc-lib-name",
            help="Name of library hosting the VC and the VCI (default: vc_lib)",
            default="vc_lib",
        )
        parser.add_argument(
            "-o",
            "--output-path",
            help="Path to the template  (default: ./compliance_test/tb_<VC name>_compliance_template.vhd)",
        )
        parser.add_argument("vc_path", help="Path to file containing the VC entity")
        parser.add_argument("vci_path", help="Path to file containing the VCI package")

    def create_vci_parser(subparsers):
        parser = subparsers.add_parser(
            "create-vci", help="Creates a VCI compliance test template"
        )
        parser.add_argument(
            "-l",
            "--vc-lib-name",
            help="Name of library hosting the VC and the VCI (default: vc_lib)",
            default="vc_lib",
        )
        parser.add_argument(
            "-o",
            "--output-path",
            help="Path to the template  (default: ./compliance_test/tb_<VCI name>_compliance_template.vhd)",
        )
        parser.add_argument("vci_path", help="Path to file containing the VCI package")
        parser.add_argument("vc_handle_t", help="VC handle type")

    parser = argparse.ArgumentParser(description="Compliance test tool")
    subparsers = parser.add_subparsers(dest="subparser_name", help="sub-command help")

    create_vc_parser(subparsers)
    create_vci_parser(subparsers)

    args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(format="%(levelname)s: %(message)s")

    if args.subparser_name == "create-vc":
        _create_vc_template(args)
    elif args.subparser_name == "create-vci":
        _create_vci_template(args)


if __name__ == "__main__":
    main()
